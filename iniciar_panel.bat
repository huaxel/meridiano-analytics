@echo off
setlocal
title Banco Meridiano Analytics - Launcher

echo ==========================================
echo 🦁 Iniciando Banco Meridiano Analytics...
echo ==========================================

REM 1. Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no encontrado.
    echo Por favor, instalalo desde Microsoft Store o python.org
    pause
    exit /b 1
)

REM 2. Verificar Node.js
cmd /c npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Node.js no encontrado.
    echo Por favor, instalalo desde nodejs.org
    pause
    exit /b 1
)

REM 3. Configurar Entorno Virtual
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
)

echo 🔌 Activando entorno...
call .venv\Scripts\activate.bat

REM 4. Instalar Dependencias Python
if exist "requirements.txt" (
    echo ⬇️  Actualizando librerias de datos...
    pip install -q -r requirements.txt
    pip install -q duckdb==0.9.2
)

REM 5. Instalar Dependencias Web
echo ⬇️  Preparando dashboard web...
cd reports
if not exist "node_modules" (
    call npm ci --silent
)

REM 6. Generar Datos
echo ⚙️  Procesando datos actualizados...
cd ..
python -m tia_elena.cli etl --rows 10000

REM 7. Generar Fuentes de Evidence
cd reports
echo 📊 Optimizando tablas...
call npm run sources

REM 8. Arrancar
echo ==========================================
echo ✅ TODO LISTO. Abriendo panel de control...
echo ==========================================
call npm run dev -- --open
