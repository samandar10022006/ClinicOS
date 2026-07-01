"""
DMed Windows Launcher — bitta EXE orqali PostgreSQL + Backend + Frontend.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import traceback
import webbrowser
from pathlib import Path

APP_NAME = "DMed"
APP_PORT = 8080


def get_app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def setup_launcher_imports(app_root: Path) -> None:
    if getattr(sys, "frozen", False):
        launcher_dir = Path(sys._MEIPASS) / "launcher"
    else:
        launcher_dir = app_root / "launcher"
    if str(launcher_dir) not in sys.path:
        sys.path.insert(0, str(launcher_dir))


def log(msg: str) -> None:
    print(f"[{APP_NAME}] {msg}", flush=True)


def ensure_frontend_build(app_root: Path, log=print) -> None:
    build_dir = app_root / "frontend" / "build"
    fallback = app_root / "launcher" / "web"
    if (build_dir / "index.html").exists():
        return
    if fallback.exists():
        log("Frontend build topilmadi. Tayyor web interfeys nusxalanmoqda...")
        build_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        for item in fallback.iterdir():
            dest = build_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)


def setup_paths(app_root: Path) -> None:
    backend_dir = app_root / "backend"
    if not backend_dir.exists():
        raise FileNotFoundError(f"backend papkasi topilmadi: {backend_dir}")

    sys.path.insert(0, str(backend_dir))
    os.chdir(str(backend_dir))

    frontend_build = app_root / "frontend" / "build"
    os.environ["DMED_APP_ROOT"] = str(app_root)
    os.environ["DMED_FRONTEND_DIR"] = str(frontend_build)
    os.environ.setdefault("ENVIRONMENT", "development")


def setup_env(database_url: str) -> None:
    os.environ["DATABASE_URL"] = database_url
    os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")
    os.environ.setdefault("SECRET_KEY", "dmed-local-secret-key")
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    os.environ.setdefault("EMAIL_HOST", "smtp.gmail.com")
    os.environ.setdefault("EMAIL_PORT", "587")
    os.environ.setdefault("EMAIL_USER", "noreply@dmed.local")
    os.environ.setdefault("EMAIL_PASS", "")


def wait_for_server(port: int, timeout: int = 90) -> bool:
    import urllib.error
    import urllib.request

    url = f"http://127.0.0.1:{port}/api/health"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            time.sleep(0.5)
    return False


def run_server(port: int) -> None:
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
        access_log=False,
    )


def open_browser(port: int) -> None:
    webbrowser.open(f"http://127.0.0.1:{port}/")


def main() -> int:
    app_root = get_app_root()
    postgres = None

    print("=" * 50)
    print(f"  {APP_NAME} — Aqlli Shifoxona Tizimi")
    print("=" * 50)
    print()

    try:
        setup_launcher_imports(app_root)
        from postgres_manager import PostgresManager

        ensure_frontend_build(app_root, log=log)
        setup_paths(app_root)
        postgres = PostgresManager(app_root)
        database_url = postgres.setup(log=log)
        setup_env(database_url)

        log("Backend ishga tushirilmoqda...")
        server_thread = threading.Thread(target=run_server, args=(APP_PORT,), daemon=True)
        server_thread.start()

        if not wait_for_server(APP_PORT):
            raise RuntimeError("Backend ishga tushmadi. Port 8080 band bo'lishi mumkin.")

        log(f"Tizim tayyor: http://127.0.0.1:{APP_PORT}")
        log("Login: admin  |  Parol: admin123")
        log("To'xtatish uchun bu oynani yoping yoki Ctrl+C bosing.")
        print()

        open_browser(APP_PORT)

        while server_thread.is_alive():
            time.sleep(1)

        return 0

    except KeyboardInterrupt:
        log("To'xtatilmoqda...")
        return 0
    except Exception as exc:
        log(f"XATOLIK: {exc}")
        traceback.print_exc()
        input("\nDavom etish uchun Enter bosing...")
        return 1
    finally:
        if postgres:
            log("PostgreSQL to'xtatilmoqda...")
            postgres.stop()
        if getattr(sys, "frozen", False):
            input("\nChiqish uchun Enter bosing...")


if __name__ == "__main__":
    sys.exit(main())
