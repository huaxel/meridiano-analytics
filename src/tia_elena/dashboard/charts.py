"""
Chart factory functions.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from tia_elena.dashboard.theme import COLORS, CHART_COLORS


def create_pool_impact_chart(df: pd.DataFrame, title: str = "Top 10 Déficit") -> go.Figure:
    """Create a bar chart comparing theoretical vs actual payouts."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["subsidiary_code"].astype(str),
        y=df["theoretical_eur"],
        name="Teórico",
        marker_color=COLORS["neutral"]
    ))
    
    fig.add_trace(go.Bar(
        x=df["subsidiary_code"].astype(str),
        y=df["final_payout_eur"],
        name="Real",
        marker_color=COLORS["primary"]
    ))
    
    fig.update_layout(
        barmode="overlay",
        title=dict(text=title, font=dict(color=COLORS["text"])),
        xaxis=dict(title="Filial", color=COLORS["text"]),
        yaxis=dict(title="EUR", color=COLORS["text"]),
        legend=dict(orientation="h", y=1.02, font=dict(color=COLORS["text"])),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"])
    )
    return fig


def create_category_donut(df: pd.DataFrame) -> go.Figure:
    """Create a donut chart for category distribution."""
    fig = px.pie(
        df, values="final_payout_eur", names="category_normalized",
        hole=0.55, color_discrete_sequence=CHART_COLORS
    )
    fig.update_layout(
        legend=dict(orientation="h", y=-0.15, font=dict(color=COLORS["text"])),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"])
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    return fig


def create_salary_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create a histogram of salary distribution by job level."""
    fig = px.histogram(
        df, 
        x="final_payout_eur", 
        color="job_level",
        nbins=50,
        marginal="box",
        color_discrete_sequence=CHART_COLORS,
        labels={"final_payout_eur": "Pago Final (EUR)", "job_level": "Nivel", "count": "Frecuencia"},
        title="Distribución Salarial por Nivel"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
        bargap=0.1,
        xaxis=dict(title="Pago Final (EUR)", color=COLORS["text"]),
        yaxis=dict(title="Número de Empleados", color=COLORS["text"]),
        legend=dict(orientation="h", y=-0.2, font=dict(color=COLORS["text"])),
    )
    return fig


def create_box_plot_by_level(df: pd.DataFrame) -> go.Figure:
    """Create a box plot of compensation by job level."""
    # Order levels if possible
    levels_order = sorted(df["job_level"].unique())
    
    fig = px.box(
        df,
        x="job_level",
        y="final_payout_eur",
        color="job_level",
        category_orders={"job_level": levels_order},
        color_discrete_sequence=CHART_COLORS,
        points="outliers",
        title="Dispersión Salarial por Nivel"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
        showlegend=False,
        xaxis=dict(title="Nivel Jerárquico", color=COLORS["text"]),
        yaxis=dict(title="Pago Final (EUR)", color=COLORS["text"]),
    )
    return fig
