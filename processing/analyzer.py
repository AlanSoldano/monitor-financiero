import pandas as pd

class Analyzer:
    def __init__(self, df: pd.DataFrame, ingreso_configurado: float = 0.0):
        self.df = df.copy()
        self.ingreso_configurado = ingreso_configurado

    def compute_metrics(self) -> dict:

        ingresos = self.df[self.df["Tipo"] == "Ingreso"]["Monto"].sum()
        gastos = self.df[self.df["Tipo"] == "Gasto"]["Monto"].sum()
        balance = ingresos - gastos

        promedio_diario = (
            self.df[self.df["Tipo"] == "Gasto"]
            .groupby(self.df["Fecha"].dt.date)["Monto"]
            .sum()
            .mean()
        )

        if pd.isna(promedio_diario):
            promedio_diario = 0

        # calculos con ingreso configurado
        disponible = 0
        porcentaje_gastado = 0

        if self.ingreso_configurado > 0:
            disponible = self.ingreso_configurado - gastos
            porcentaje_gastado = (gastos / self.ingreso_configurado) * 100

        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance,
            "promedio_diario": promedio_diario,
            "ingreso_configurado": self.ingreso_configurado,
            "disponible": disponible,
            "porcentaje_gastado": porcentaje_gastado,
        }

    def gasto_por_categoria(self) -> pd.DataFrame:

        return (
            self.df[self.df["Tipo"] == "Gasto"]
            .groupby("Categoria")["Monto"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    def evolucion_mensual(self):

        df = self.df.copy()

        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)

        evolucion = (
            df.groupby(["Mes", "Tipo"])["Monto"]
            .sum()
            .reset_index()
            .sort_values("Mes")
        )

        return evolucion

    def top_gastos(self) -> pd.DataFrame:

        return (
            self.df[self.df["Tipo"] == "Gasto"]
            .sort_values("Monto", ascending=False)
            .head(10)
        )