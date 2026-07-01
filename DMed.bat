@echo off
chcp 65001 >nul
title DMed - Aqlli Shifoxona
cd /d "%~dp0"

echo DMed ishga tushirilmoqda...
py -3.11 launcher\dmed_launcher.py
if errorlevel 1 pause
