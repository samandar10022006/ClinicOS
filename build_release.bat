@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================
echo   DMed - Release Build (EXE yaratish)
echo ============================================
echo.

set ROOT=%~dp0
cd /d "%ROOT%"

where node >nul 2>&1
if errorlevel 1 (
    echo [XATOLIK] Node.js topilmadi. https://nodejs.org dan o'rnating.
    pause
    exit /b 1
)

set PYTHON=py -3.11

echo [1/5] Frontend yig'ilmoqda...
cd frontend
if not exist node_modules (
    call npm install --legacy-peer-deps
    if errorlevel 1 goto :error
)
set REACT_APP_API_URL=http://127.0.0.1:8080
call npm run build
if errorlevel 1 (
    echo [OGOHLANTIRISH] React build xato. Tayyor web interfeys ishlatiladi...
    if not exist frontend\build mkdir frontend\build
    xcopy /E /I /Y launcher\web frontend\build >nul
)
cd ..

echo [2/5] Python kutubxonalari o'rnatilmoqda...
%PYTHON% -m pip install --upgrade pip >nul
%PYTHON% -m pip install -r backend\requirements.txt pyinstaller >nul
if errorlevel 1 goto :error

echo [3/5] AI model tekshirilmoqda...
if not exist ai-model\model.pkl (
    cd ai-model
    %PYTHON% train.py
    cd ..
)

echo [4/5] DMed.exe yaratilmoqda...
%PYTHON% -m PyInstaller launcher\DMed.spec --noconfirm --distpath dist --workpath build\pyinstaller
if errorlevel 1 goto :error

echo [5/5] Fayllar nusxalanmoqda...
if not exist dist\DMed mkdir dist\DMed
xcopy /E /I /Y backend dist\DMed\backend >nul
xcopy /E /I /Y frontend\build dist\DMed\frontend\build >nul
xcopy /E /I /Y ai-model dist\DMed\ai-model >nul
xcopy /E /I /Y launcher\web dist\DMed\launcher\web >nul

echo.
echo ============================================
echo   TAYYOR!
echo   dist\DMed\DMed.exe ni ishga tushiring
echo   Login: admin  Parol: admin123
echo ============================================
echo.
pause
exit /b 0

:error
echo.
echo [XATOLIK] Build muvaffaqiyatsiz tugadi.
pause
exit /b 1
