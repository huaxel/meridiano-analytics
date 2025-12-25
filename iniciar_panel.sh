#!/bin/bash

# Banco Meridiano Analytics - "Zero Config" Launcher
# Este script prepara todo el entorno automáticamente.

set -e # Salir si hay errores

echo "🦁 Iniciando Banco Meridiano Analytics..."
echo "=========================================="

# 1. Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado."
    echo "Por favor, instálalo desde: https://www.python.org/downloads/"
    exit 1
fi

# 2. Configurar Entorno Virtual (Python)
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

echo "🔌 Activando entorno..."
source .venv/bin/activate

# 3. Instalar Dependencias Python
if [ -f "requirements.txt" ]; then
    echo "⬇️  Actualizando librerías de datos..."
    pip install -q -r requirements.txt
    pip install -q duckdb==0.9.2 # Asegurar compatibilidad
fi

# 4. Verificar Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ Error: Node.js no encontrado."
    echo "Instálalo desde: https://nodejs.org/"
    exit 1
fi

# 5. Instalar Dependencias Web
echo "⬇️  Preparando dashboard web..."
cd reports
if [ ! -d "node_modules" ]; then
    npm ci --silent
fi

# 6. Generar Datos (ETL)
echo "⚙️  Procesando datos actualizados..."
cd .. # Volver a raiz para ejecutar modulo
# Asegurar que el modulo existe
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
if [ -d "src/meridiano_analysis" ]; then
    # Ejecutar ETL silenciosamente (o mostrar output si falla)
    python -m meridiano_analysis.cli etl --rows 10000 || echo "⚠️  Aviso: ETL reportó warning, continuando..."
else
    echo "⚠️  No se encontró módulo ETL (meridiano_analysis), usando datos cacheados."
fi

# 7. Generar Fuentes de Evidence
cd reports
echo "📊 Optimizando tablas..."
npm run sources

# 8. Arrancar
echo "=========================================="
echo "✅ TODO LISTO. Abriendo panel de control..."
echo "=========================================="
npm run dev -- --open
