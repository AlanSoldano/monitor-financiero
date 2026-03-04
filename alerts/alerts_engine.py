class AlertsEngine:
    def __init__(self, df):
        self.df = df

    def generate_alerts(self):

        alerts = []

        gastos = self.df[self.df["Tipo"] == "Gasto"]["Monto"].sum()
        ingresos = self.df[self.df["Tipo"] == "Ingreso"]["Monto"].sum()

        if gastos > ingresos:
            alerts.append("Tus gastos superan tus ingresos.")

        if ingresos > 0:
            porcentaje = (gastos / ingresos) * 100
            if porcentaje > 80:
                alerts.append("Estás gastando más del 80% de tus ingresos.")

        if gastos == 0 and ingresos == 0:
            alerts.append("No hay movimientos registrados.")

        return alerts