"""Portable PostgreSQL manager for DMed Windows launcher."""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

POSTGRES_VERSION = "15.8-1"
POSTGRES_URL = (
    f"https://get.enterprisedb.com/postgresql/"
    f"postgresql-{POSTGRES_VERSION}-windows-x64-binaries.zip"
)
DEFAULT_PORT = 55432
DB_NAME = "dmed"
DB_USER = "dmed"
DB_PASSWORD = "dmed123"


def _local_data_root(app_root: Path) -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "DMed"
    return app_root / "runtime" / "local"


class PostgresManager:
    def __init__(self, app_root: Path, port: int = DEFAULT_PORT):
        self.app_root = app_root
        self.port = port
        self.runtime_dir = app_root / "runtime"
        self.postgres_home = self.runtime_dir / "postgres" / "pgsql"
        self.bin_dir = self.postgres_home / "bin"
        self.data_dir = _local_data_root(app_root) / "postgres-data"
        self.log_file = _local_data_root(app_root) / "logs" / "postgres.log"
        self.process: subprocess.Popen | None = None

    @property
    def database_url(self) -> str:
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:{self.port}/{DB_NAME}"

    def _bin(self, name: str) -> Path:
        exe = name + (".exe" if os.name == "nt" else "")
        return self.bin_dir / exe

    def is_installed(self) -> bool:
        return self._bin("initdb").exists() and self._bin("pg_ctl").exists()

    def download_and_install(self, log=print) -> None:
        if self.is_installed():
            return

        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        archive = self.runtime_dir / "postgres.zip"
        extract_dir = self.runtime_dir / "postgres"

        log("PostgreSQL yuklanmoqda (birinchi marta, 1-2 daqiqa)...")
        urllib.request.urlretrieve(POSTGRES_URL, archive)

        log("PostgreSQL o'rnatilmoqda...")
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "r") as zf:
            zf.extractall(extract_dir)

        archive.unlink(missing_ok=True)

        if not self.is_installed():
            raise RuntimeError("PostgreSQL o'rnatilmadi. runtime/postgres/pgsql/bin tekshiring.")

        log("PostgreSQL muvaffaqiyatli o'rnatildi.")

    def _configure_hba(self) -> None:
        hba = self.data_dir / "pg_hba.conf"
        if not hba.exists():
            return
        content = hba.read_text(encoding="utf-8")
        if "DMed trust" in content:
            return
        content += (
            "\n# DMed trust\n"
            "host    all             all             127.0.0.1/32            trust\n"
            "host    all             all             ::1/128                 trust\n"
        )
        hba.write_text(content, encoding="utf-8")

    def _configure_port(self) -> None:
        conf = self.data_dir / "postgresql.conf"
        if not conf.exists():
            return
        lines = conf.read_text(encoding="utf-8").splitlines()
        updated = []
        found = False
        for line in lines:
            if line.startswith("port"):
                updated.append(f"port = {self.port}")
                found = True
            else:
                updated.append(line)
        if not found:
            updated.append(f"port = {self.port}")
        conf.write_text("\n".join(updated) + "\n", encoding="utf-8")

    def initialize(self, log=print) -> None:
        if (self.data_dir / "PG_VERSION").exists():
            self._configure_port()
            self._configure_hba()
            return

        log("PostgreSQL ma'lumotlar bazasi yaratilmoqda...")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        if self.data_dir.exists():
            shutil.rmtree(self.data_dir, ignore_errors=True)

        result = subprocess.run(
            [str(self._bin("initdb")), "-D", str(self.data_dir), "-U", "postgres", "-E", "UTF8", "-A", "trust"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"initdb xatolik: {result.stderr.strip() or result.stdout.strip()}"
            )

        self._configure_port()
        self._configure_hba()
        log(f"PostgreSQL data papkasi tayyor: {self.data_dir}")

    def _wait_for_port(self, timeout: int = 60) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._port_open():
                return True
            time.sleep(0.5)
        return False

    def _port_open(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            return sock.connect_ex(("127.0.0.1", self.port)) == 0

    def start(self, log=print) -> None:
        if self._port_open():
            log(f"PostgreSQL allaqachon ishlayapti (port {self.port})")
            return

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            str(self._bin("pg_ctl")),
            "-D", str(self.data_dir),
            "-l", str(self.log_file),
            "start",
            "-o", f"-p {self.port}",
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if not self._wait_for_port():
            raise RuntimeError(f"PostgreSQL {self.port} portda ishga tushmadi. Log: {self.log_file}")
        log(f"PostgreSQL ishga tushdi (port {self.port})")

    def ensure_database(self, log=print) -> None:
        env = os.environ.copy()
        psql_base = [
            str(self._bin("psql")),
            "-h", "127.0.0.1",
            "-p", str(self.port),
            "-U", "postgres",
            "-v", "ON_ERROR_STOP=1",
        ]

        def run_sql(sql: str, ignore_errors: bool = False) -> None:
            result = subprocess.run(
                psql_base + ["-c", sql],
                capture_output=True,
                text=True,
                env=env,
                timeout=30,
            )
            if result.returncode != 0 and not ignore_errors:
                err = (result.stderr or result.stdout or "").lower()
                if "already exists" in err:
                    return
                raise RuntimeError(result.stderr.strip() or result.stdout.strip())

        db_exists = subprocess.run(
            psql_base + ["-tAc", f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )
        if db_exists.stdout.strip() != "1":
            run_sql(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';", ignore_errors=True)
            run_sql(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};", ignore_errors=True)
            log(f"'{DB_NAME}' bazasi yaratildi.")
        else:
            log(f"'{DB_NAME}' bazasi mavjud.")

        run_sql(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};", ignore_errors=True)

    def stop(self) -> None:
        if not self._bin("pg_ctl").exists() or not (self.data_dir / "PG_VERSION").exists():
            return
        try:
            subprocess.run(
                [str(self._bin("pg_ctl")), "-D", str(self.data_dir), "stop", "fast"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except Exception:
            pass

    def setup(self, log=print) -> str:
        self.download_and_install(log=log)
        self.initialize(log=log)
        self.start(log=log)
        self.ensure_database(log=log)
        return self.database_url
