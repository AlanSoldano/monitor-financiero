import pandas as pd


class ReportGenerator:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def generate(self, metrics: dict, cat_df: pd.DataFrame, alerts: list[str]):
        with pd.ExcelWriter(self.filepath, engine="xlsxwriter") as writer:
            pd.DataFrame([metrics]).to_excel(
                writer, sheet_name="Resumen", index=False
            )

            cat_df.to_excel(
                writer, sheet_name="Categorias", index=False
            )

            pd.DataFrame(alerts, columns=["Alertas"]).to_excel(
                writer, sheet_name="Alertas", index=False
            )