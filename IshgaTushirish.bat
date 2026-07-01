@echo off
chcp 65001 >nul
title DMed Ishga Tushirish

set ROOT=%~dp0
cd /d "%ROOT%"

if exist "dist\DMedRelease\DMed\DMed.exe" (
    echo DMed (yangi build) topildi, ishga tushirilmoqda...
    start "" "dist\DMedRelease\DMed\DMed.exe"
    exit /b 0
)

if exist "dist\DMed\DMed.exe" (
    echo DMed.exe topildi, ishga tushirilmoqda...
    start "" "dist\DMed\DMed.exe"
    exit /b 0
)

if exist "DMed.bat" (
    call DMed.bat
    exit /b 0
)

echo DMed topilmadi. Avval build_release.bat ni ishga tushiring.
pause
