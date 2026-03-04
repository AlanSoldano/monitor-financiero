import pandas as pd
import numpy as np
from config import *

class Projections:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def monthly_projection(self) -> float:
        df = self.df.copy()
        df["Mes"] = df[DATE_COLUMN].dt.to_period("M")
        monthly_avg = df.groupby("Mes")[AMOUNT_COLUMN].sum().mean()
        return monthly_avg