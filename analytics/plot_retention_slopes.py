# analytics/plot_retention_slopes.py
from analytics.retention_data import get_retention_json
from analytics.retention_regression import compute_retention_slopes
import pandas as pd
import plotly.express as px
import plotly.io as pio


def render_retention_slopes_html():
    """
    Generates the Plotly bar chart HTML for retention decay slopes.
    Returns:
        str: A div containing the chart's HTML
    """
    # 1) Fetch and model data
    raw_data = get_retention_json()
    modeled  = compute_retention_slopes(raw_data)

    # 2) DataFrame
    df = pd.DataFrame(modeled)

    # 3) Build figure
    fig = px.bar(
        df,
        x='wholesaler',
        y='slope',
        color='is_outlier',
        labels={'wholesaler':'Wholesaler', 'slope':'Retention Decay Slope'},
        title='Retention Decay Slopes by Wholesaler'
    )
    mean_slope = df['slope'].mean()
    fig.add_hline(
        y=mean_slope,
        line_dash='dash',
        line_color='black',
        annotation_text=f"Mean slope = {mean_slope:.3f}",
        annotation_position='top left'
    )

    # 4) Return HTML snippet
    return pio.to_html(fig, full_html=False)
