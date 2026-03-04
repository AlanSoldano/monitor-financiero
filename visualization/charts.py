import plotly.express as px
import pandas as pd

def pie_categories(df: pd.DataFrame):
    return px.pie(df, names="Categoria", values="Monto")

def line_evolution(df: pd.DataFrame):
    return px.line(df, x="Mes", y="Monto")