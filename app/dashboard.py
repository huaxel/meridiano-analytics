"""
Streamlit Dashboard - Panel Ejecutivo de Retribución Variable.

Dashboard profesional para C-Suite con KPIs regulatorios (CRD IV/V).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

from app.theme import PAGE_CSS, HEADER_HTML, COLORS, CHART_COLORS, SUBSIDIARY_NAMES
from src.config import settings


# --- Page Configuration ---
st.set_page_config(
    page_title="Retribución Variable | C-Suite",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(PAGE_CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load processed data."""
    if not settings.output_path.exists():
        raise FileNotFoundError("Ejecuta primero: python scripts/generate_data.py && python scripts/run_etl.py")
    return pl.read_parquet(settings.output_path)


@st.cache_data
def load_audit():
    """Load audit data."""
    if settings.audit_path.exists():
        return pl.read_parquet(settings.audit_path)
    return None


def format_eur(value: float) -> str:
    """Format as EUR."""
    if abs(value) >= 1e9:
        return f"€{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"€{value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"€{value/1e3:.0f}K"
    return f"€{value:,.0f}"


def get_region(sub_code: str) -> str:
    """Get region from subsidiary code."""
    mapping = {
        "ES": "🇪🇸 España", "PT": "🇵🇹 Portugal", "DE": "🇩🇪 Alemania", "PL": "🇵🇱 Polonia",
        "UK": "🇬🇧 UK", "US": "🇺🇸 USA",
        "BR": "🇧🇷 Brasil", "MX": "🇲🇽 México", "AR": "🇦🇷 Argentina", "CL": "🇨🇱 Chile",
        "CO": "🇨🇴 Colombia", "PE": "🇵🇪 Perú", "UY": "🇺🇾 Uruguay",
        "CN": "🇨🇳 China", "SG": "🇸🇬 Singapur", "JP": "🇯🇵 Japón",
    }
    country = sub_code.split("-")[0] if "-" in sub_code else sub_code
    return mapping.get(country, "🌍 Otros")


try:
    df = load_data()
    audit = load_audit()
    
    # Add region
    df = df.with_columns(
        pl.col("subsidiary_code").map_elements(get_region, return_dtype=pl.Utf8).alias("region")
    )
    
    # --- Sidebar ---
    st.sidebar.markdown("### 🎯 Filtros")
    
    regions = ["Global"] + sorted(df["region"].unique().to_list())
    selected_region = st.sidebar.selectbox("📍 Región", regions)
    
    if selected_region != "Global":
        df_display = df.filter(pl.col("region") == selected_region)
    else:
        df_display = df
    
    # Category filter
    categories = ["Todas"] + sorted(df_display["category_normalized"].unique().drop_nulls().to_list())
    selected_cat = st.sidebar.selectbox("📊 Categoría", categories)
    
    if selected_cat != "Todas":
        df_display = df_display.filter(pl.col("category_normalized") == selected_cat)
    
    # === EXECUTIVE KPIs ===
    st.markdown("### 📊 KPIs Ejecutivos")
    
    total_demand = df_display["theoretical_eur"].sum()
    total_paid = df_display["final_payout_eur"].sum()
    haircut = 1 - (total_paid / total_demand) if total_demand > 0 else 0
    
    # Data quality indicator
    null_categories = df_display.filter(pl.col("category_normalized").is_null()).height
    total_records = df_display.height
    data_quality = (1 - null_categories / total_records) * 100 if total_records > 0 else 0
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Demanda", format_eur(total_demand))
    c2.metric("✅ Pago Real", format_eur(total_paid), delta=f"-{haircut:.1%}" if haircut > 0 else None, delta_color="inverse")
    c3.metric("📉 Recorte", f"{haircut:.1%}")
    c4.metric("📋 Registros", f"{total_records:,}")
    c5.metric("🔍 Data Quality", f"{data_quality:.1f}%", delta="⚠️" if data_quality < 95 else "✓")
    
    st.markdown("---")
    
    # === REGULATORY METRICS (CRD IV/V) ===
    st.markdown("### 📜 Métricas Regulatorias (CRD IV/V)")
    
    # Check for deferred and equity columns
    has_deferred = "is_deferred" in df_display.columns
    has_equity = "is_equity" in df_display.columns
    
    r1, r2, r3, r4 = st.columns(4)
    
    if has_deferred:
        deferred = df_display.filter(pl.col("is_deferred") == True)["final_payout_eur"].sum()
        deferred_pct = (deferred / total_paid * 100) if total_paid > 0 else 0
        r1.metric("⏳ Diferido", format_eur(deferred), delta=f"{deferred_pct:.0f}% del total")
    else:
        r1.metric("⏳ Diferido", "N/A")
    
    if has_equity:
        equity = df_display.filter(pl.col("is_equity") == True)["final_payout_eur"].sum()
        equity_pct = (equity / total_paid * 100) if total_paid > 0 else 0
        r2.metric("📈 En Acciones", format_eur(equity), delta=f"{equity_pct:.0f}% del total")
    else:
        r2.metric("📈 En Acciones", "N/A")
    
    # Clawback/Malus detection
    negative_amounts = df_display.filter(pl.col("final_payout_eur") < 0)
    clawback_total = abs(negative_amounts["final_payout_eur"].sum()) if negative_amounts.height > 0 else 0
    r3.metric("🔄 Clawback/Malus", format_eur(clawback_total))
    
    # Affected subsidiaries
    if audit is not None:
        underfunded = audit.filter(pl.col("funding_ratio") < 1.0).height
        total_subs = audit.height
        r4.metric("⚠️ Filiales Bajo Pool", f"{underfunded} / {total_subs}")
    else:
        r4.metric("⚠️ Filiales Bajo Pool", "N/A")
    
    st.markdown("---")
    
    # === CHARTS ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌍 Distribución por Región")
        
        df_region = (
            df_display
            .group_by("region")
            .agg([
                pl.col("final_payout_eur").sum().alias("pago"),
                pl.col("theoretical_eur").sum().alias("demanda"),
            ])
            .with_columns(
                ((pl.col("pago") / pl.col("demanda")) * 100).alias("cobertura")
            )
            .sort("pago", descending=True)
        )
        
        fig = px.bar(
            df_region.to_pandas(),
            x="region",
            y=["demanda", "pago"],
            barmode="group",
            color_discrete_sequence=[COLORS["neutral"], COLORS["primary"]],
            labels={"value": "EUR", "variable": "Tipo", "region": "Región"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text"]),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🍩 Distribución por Categoría")
        
        df_cat = (
            df_display
            .filter(pl.col("category_normalized").is_not_null())
            .group_by("category_normalized")
            .agg(pl.col("final_payout_eur").sum())
            .sort("final_payout_eur", descending=True)
        )
        
        fig = px.pie(
            df_cat.to_pandas(),
            values="final_payout_eur",
            names="category_normalized",
            hole=0.5,
            color_discrete_sequence=CHART_COLORS
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text"]),
            legend=dict(orientation="h", y=-0.2)
        )
        fig.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig, use_container_width=True)
    
    # === POOL COVERAGE ===
    if audit is not None:
        st.markdown("#### 📊 Cobertura de Pool por Filial")
        
        audit_display = audit.with_columns(
            pl.col("subsidiary_code").replace(SUBSIDIARY_NAMES).alias("filial")
        ).sort("funding_ratio")
        
        fig = go.Figure()
        
        colors = ["#C41E3A" if r < 1.0 else "#00A86B" for r in audit_display["funding_ratio"].to_list()]
        
        fig.add_trace(go.Bar(
            x=audit_display["filial"].to_list(),
            y=audit_display["funding_ratio"].to_list(),
            marker_color=colors,
            text=[f"{r:.0%}" for r in audit_display["funding_ratio"].to_list()],
            textposition="outside"
        ))
        
        fig.add_hline(y=1.0, line_dash="dash", line_color="#FFB800", 
                      annotation_text="100% Cobertura")
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text"]),
            yaxis=dict(title="Ratio de Cobertura", range=[0, 1.2]),
            xaxis=dict(title="", tickangle=45),
            margin=dict(b=100)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # === DATA QUALITY ISSUES ===
    st.markdown("### ⚠️ Alertas de Calidad de Datos")
    
    with st.expander("Ver problemas detectados"):
        issues = []
        
        # Unmapped categories
        unmapped = df_display.filter(
            (pl.col("category_normalized").is_null()) |
            (pl.col("category_normalized") == "UNMAPPED")
        ).height
        if unmapped > 0:
            issues.append(f"🔴 **{unmapped:,}** registros sin categoría mapeada")
        
        # Negative amounts (unexpected)
        negatives = df_display.filter(pl.col("final_payout_eur") < 0).height
        if negatives > 0:
            issues.append(f"🟡 **{negatives:,}** registros con importes negativos (clawback/malus)")
        
        # Very large amounts (outliers)
        extreme = df_display.filter(pl.col("final_payout_eur") > 1_000_000).height
        if extreme > 0:
            issues.append(f"🟡 **{extreme:,}** pagos superiores a €1M (revisar)")
        
        if issues:
            for issue in issues:
                st.markdown(issue)
        else:
            st.success("✅ No se detectaron problemas críticos de calidad")
    
    # === DETAIL TABLE ===
    with st.expander("📋 Detalle por Categoría"):
        detail = (
            df_display
            .group_by("category_normalized")
            .agg([
                pl.col("theoretical_eur").sum().alias("demanda"),
                pl.col("final_payout_eur").sum().alias("pago"),
                pl.len().alias("registros")
            ])
            .with_columns(
                ((pl.col("pago") / pl.col("demanda")) * 100).alias("cobertura_pct")
            )
            .sort("pago", descending=True)
        )
        
        st.dataframe(
            detail.to_pandas().style.format({
                "demanda": "€{:,.0f}",
                "pago": "€{:,.0f}",
                "cobertura_pct": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

except FileNotFoundError as e:
    st.error(f"⚠️ {e}")
    st.code("python scripts/generate_data.py\npython scripts/run_etl.py")
except Exception as e:
    st.error(f"Error: {e}")
