"""
Streamlit Dashboard Entry Point.

Run with: streamlit run src/meridiano_analysis/dashboard/app.py
Or via CLI: tia-elena dashboard
"""
import sys
from pathlib import Path

# Add src to path for standalone running
_src = Path(__file__).parent.parent.parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import streamlit as st
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

from meridiano_analysis.dashboard.theme import PAGE_CSS, HEADER_HTML, COLORS, CHART_COLORS, SUBSIDIARY_NAMES
from meridiano_analysis.dashboard.charts import create_pool_impact_chart, create_category_donut
from meridiano_analysis.dashboard.data import load_processed_data, load_audit_data


def get_region(sub_code: str) -> str:
    """Get region from subsidiary code."""
    mapping = {
        "ES": "🇪🇸 España", "PT": "🇵🇹 Europa", "DE": "🇩🇪 Europa", "PL": "🇵🇱 Europa",
        "UK": "🇬🇧 Europa", "US": "🇺🇸 Norteamérica",
        "BR": "🇧🇷 LATAM", "MX": "🇲🇽 LATAM", "AR": "🇦🇷 LATAM", "CL": "🇨🇱 LATAM",
        "CO": "🇨🇴 LATAM", "PE": "🇵🇪 LATAM", "UY": "🇺🇾 LATAM",
        "CN": "🇨🇳 Asia", "SG": "🇸🇬 Asia", "JP": "🇯🇵 Asia",
    }
    country = sub_code.split("-")[0] if "-" in sub_code else sub_code
    return mapping.get(country, "🌍 Otros")


def format_eur(value: float) -> str:
    """Format as EUR."""
    if abs(value) >= 1e9:
        return f"€{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"€{value/1e6:.1f}M"
    return f"€{value:,.0f}"


def main():
    """Main dashboard entry point."""
    st.set_page_config(
        page_title="Banco Meridiano | C-Suite",
        page_icon="🦁",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(PAGE_CSS, unsafe_allow_html=True)
    st.markdown(HEADER_HTML, unsafe_allow_html=True)
    
    try:
        with st.spinner("Cargando datos..."):
            df = load_processed_data()
            audit = load_audit_data()
        
        df = df.with_columns(
            pl.col("subsidiary_code").map_elements(get_region, return_dtype=pl.Utf8).alias("region")
        )
        
        # Sidebar
        st.sidebar.markdown("### 🎯 Filtros")
        regions = ["Global"] + sorted(df["region"].unique().to_list())
        selected_region = st.sidebar.selectbox("📍 Región", regions)
        
        df_display = df if selected_region == "Global" else df.filter(pl.col("region") == selected_region)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Visión General", "📉 Análisis Salarial", "📋 Detalle Operativo"])
        
        with tab1:
            # KPIS
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 Demanda", format_eur(total_demand))
            c2.metric("✅ Pago Real", format_eur(total_paid), delta=f"-{haircut:.1%}" if haircut > 0 else None, delta_color="inverse")
            c3.metric("📉 Recorte", f"{haircut:.1%}")
            c4.metric("📋 Registros", f"{len(df_display):,}")
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Empacto por Filial")
                df_sub = (
                    df_display
                    .group_by("subsidiary_code")
                    .agg([pl.col("theoretical_eur").sum(), pl.col("final_payout_eur").sum()])
                    .with_columns((pl.col("theoretical_eur") - pl.col("final_payout_eur")).alias("gap"))
                    .sort("gap", descending=True)
                    .head(10)
                )
                fig = create_pool_impact_chart(df_sub.to_pandas())
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🍩 Por Categoría")
                df_cat = (
                    df_display
                    .filter(pl.col("category_normalized").is_not_null())
                    .group_by("category_normalized")
                    .agg(pl.col("final_payout_eur").sum())
                    .sort("final_payout_eur", descending=True)
                )
                fig = create_category_donut(df_cat.to_pandas())
                st.plotly_chart(fig, use_container_width=True)
            
            # Pool Coverage
            if audit is not None:
                st.subheader("📊 Cobertura de Pool")
                audit_viz = audit.with_columns(
                    pl.col("subsidiary_code").replace(SUBSIDIARY_NAMES).alias("filial")
                ).sort("funding_ratio")
                
                colors = ["#C41E3A" if r < 1.0 else "#00A86B" for r in audit_viz["funding_ratio"].to_list()]
                
                fig = go.Figure(go.Bar(
                    x=audit_viz["filial"].to_list(),
                    y=audit_viz["funding_ratio"].to_list(),
                    marker_color=colors,
                    text=[f"{r:.0%}" for r in audit_viz["funding_ratio"].to_list()],
                    textposition="outside"
                ))
                fig.add_hline(y=1.0, line_dash="dash", line_color="#FFB800")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=COLORS["text"]),
                    yaxis=dict(title="Ratio", range=[0, 1.2]),
                    xaxis=dict(tickangle=45), margin=dict(b=100)
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("📈 Distribución Salarial")
            from meridiano_analysis.dashboard.charts import create_salary_distribution_chart, create_box_plot_by_level
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hist = create_salary_distribution_chart(df_display.to_pandas())
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                fig_box = create_box_plot_by_level(df_display.to_pandas())
                st.plotly_chart(fig_box, use_container_width=True)

        with tab3:
            st.subheader("📋 Detalle de Registros")
            
            # Filters for table
            cols = st.columns(3)
            with cols[0]:
                search = st.text_input("🔍 Buscar Empleado (ID)")
            with cols[1]:
                level_filter = st.multiselect("Nivel", sorted(df["job_level"].unique().to_list()))
            with cols[2]:
                cat_filter = st.multiselect("Categoría", sorted(df["category_normalized"].unique().to_list()))
            
            df_table = df_display
            if search:
                df_table = df_table.filter(pl.col("employee_id").str.contains(search))
            if level_filter:
                df_table = df_table.filter(pl.col("job_level").is_in(level_filter))
            if cat_filter:
                df_table = df_table.filter(pl.col("category_normalized").is_in(cat_filter))
            
            # Display
            st.dataframe(
                df_table.head(1000).to_pandas(),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "final_payout_eur": st.column_config.NumberColumn(format="€%.2f"),
                    "theoretical_eur": st.column_config.NumberColumn(format="€%.2f"),
                    "funding_ratio": st.column_config.NumberColumn(format="%.2f%%"),
                }
            )
            
            # Download
            st.download_button(
                "📥 Descargar CSV",
                df_table.write_csv(),
                "retribucion_variable.csv",
                "text/csv"
            )

        # Data Quality
        
        # Data Quality
        with st.expander("⚠️ Calidad de Datos"):
            unmapped = df_display.filter(
                (pl.col("category_normalized").is_null()) |
                (pl.col("category_normalized") == "UNMAPPED")
            ).height
            if unmapped > 0:
                st.warning(f"🔴 {unmapped:,} registros sin categoría mapeada")
            else:
                st.success("✅ Todos los registros están mapeados")
    
    except FileNotFoundError as e:
        st.error(f"⚠️ {e}")
        st.code("tia-elena generate\ntia-elena etl")


if __name__ == "__main__":
    main()
