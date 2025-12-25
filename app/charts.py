"""
Reusable chart components.

Factory functions for creating consistent, themed charts.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from .theme import COLORS, CHART_COLORS


def create_pool_impact_chart(
    df: pd.DataFrame,
    title: str = "Top 10 Budget Shortfalls"
) -> go.Figure:
    """
    Create a bar chart comparing theoretical vs actual payouts.
    
    Args:
        df: DataFrame with subsidiary_code, theoretical_eur, final_payout_eur columns
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["subsidiary_code"].astype(str),
        y=df["theoretical_eur"],
        name="Theoretical",
        marker_color=COLORS["neutral"]
    ))
    
    fig.add_trace(go.Bar(
        x=df["subsidiary_code"].astype(str),
        y=df["final_payout_eur"],
        name="Actual",
        marker_color=COLORS["primary"]
    ))
    
    fig.update_layout(
        barmode="overlay",
        title=dict(text=title, font=dict(color=COLORS["text"])),
        xaxis=dict(
            title="Subsidiary",
            color=COLORS["text"],
            gridcolor="rgba(139,0,0,0.2)"
        ),
        yaxis=dict(
            title="EUR",
            color=COLORS["text"],
            gridcolor="rgba(139,0,0,0.2)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLORS["text"])
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"])
    )
    
    return fig


def create_category_donut(
    df: pd.DataFrame,
    values_col: str = "final_payout_eur",
    names_col: str = "category_normalized"
) -> go.Figure:
    """
    Create a donut chart for category distribution.
    
    Args:
        df: DataFrame with category and value columns
        values_col: Column name for values
        names_col: Column name for categories
        
    Returns:
        Plotly Figure
    """
    fig = px.pie(
        df,
        values=values_col,
        names=names_col,
        hole=0.55,
        color_discrete_sequence=CHART_COLORS
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            y=-0.15,
            font=dict(color=COLORS["text"])
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
        margin=dict(t=20, b=20)
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color=COLORS["background"], width=2))
    )
    
    return fig
