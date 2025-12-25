# Banco Meridiano Analytics 

**Sistema de Análisis de Retribución Variable**

Plataforma de inteligencia de negocio para el procesamiento y visualización de datos salariales en contexto bancario global. Transformado de ETL Python puro a un dashboard analítico moderno con **Evidence.dev**.

![Badge](https://img.shields.io/badge/Status-Deployed-success) ![Stack](https://img.shields.io/badge/Stack-Evidence%20%7C%20DuckDB%20%7C%20Polars-blue)

##  Características Clave

- **Modern Dashboard**: Construido con [Evidence.dev](https://evidence.dev/) (Markdown + SQL + Svelte).
- **Interactive**: Filtros por filial, gráficos de correlación y KPIs reactivos pre-agregados.
- **Branding corporativo**: Identidad visual "Red/Gray" de Banco Meridiano de Inversión.
- **High Performance**:
    - **Backend**: ETL en Python con Polars (0.13s para 300k registros).
    - **Frontend**: DuckDB-WASM en navegador con pre-agregación para filtrado instantáneo.

## 🚀 Guía de Inicio Rápido (Para No Técnicos)

Hemos creado scripts automáticos para que no tengas que usar la terminal.

### 🍎 Mac / Linux
1. Asegúrate de tener **Python** y **Node.js** instalados.
2. Haz doble clic (o ejecuta en terminal) el archivo:
   `./iniciar_panel.sh`

### 🪟 Windows
1. Asegúrate de tener **Python** y **Node.js** instalados.
2. Haz doble clic en el archivo:
   `iniciar_panel.bat`

El sistema instalará todo automáticamente y abrirá el panel en tu navegador.

## 🛠️ Arquitectura Técnica

1.  **ETL (Python)**: Genera datos sintéticos complejos (MRTs, diferidos, FX) y los exporta a Parquet.
2.  **Modelado (DuckDB)**: Ingesta los archivos Parquet como fuente de datos.
3.  **Visualización (Evidence)**:
    - `index.md`: Panel Ejecutivo con filtros globales.
    - `analisis-salarial.md`: Desglose detallado por niveles y distribuciones.

##  Instalación

### Requisitos
- Python 3.11+ (con `uv` recomendado)
- Node.js 20+

### Setup

```bash
# 1. Instalar backend y dependencias
uv sync
pip install -e .

# 2. Generar datos (Pipeline ETL)
tia-elena generate
meridiano-analysis etl  # Crea los archivos Parquet en reports/sources/meridiano_analysis/

# 3. Instalar frontend
cd reports
npm install
```

## 🖥️ Ejecución Local

```bash
cd reports
npm run dev
# Dashboard disponible en http://localhost:3000/meridiano-analytics/
```

## 🌐 Despliegue

Configurado automáticamente vía **GitHub Actions** hacia **GitHub Pages**.
El flujo `deploy.yml`:
1.  Instala dependencias.
2.  Construye el sitio estático (`npm run build`).
3.  Sube los artefactos a la rama `gh-pages`.

---
*Powered by Huaxel Data Team*
