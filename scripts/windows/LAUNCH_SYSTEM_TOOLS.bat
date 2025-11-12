@echo off
REM ============================================================
REM PhiGEN System Tools Quick Launcher
REM Launches the Master System Tools menu from root directory
REM ============================================================

color 0B
title Launching PhiGEN System Tools

REM Launch the master tools from SystemTools folder
call "%~dp0SystemTools\MASTER_SYSTEM_TOOLS.bat"
