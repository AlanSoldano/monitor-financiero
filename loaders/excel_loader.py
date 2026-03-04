import pandas as pd
from config import DEFAULT_EXCEL_FILE

class ExcelLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):

        if hasattr(self.filepath, "read"):
            df_mov = pd.read_excel(
                self.filepath,
                sheet_name="movimientos",
                engine="openpyxl"
            )
        else:
            df_mov = pd.read_excel(
                self.filepath,
                sheet_name="movimientos",
                engine="openpyxl"
            )

        df_mov.columns = df_mov.columns.str.strip()

        required_columns = [
            "Fecha",
            "Tipo",
            "Categoria",
            "Monto",
            "Descripcion"
        ]

        for col in required_columns:
            if col not in df_mov.columns:
                raise ValueError(f"Falta columna obligatoria: {col}")

        df_mov["Fecha"] = pd.to_datetime(df_mov["Fecha"], errors="coerce")
        df_mov["Monto"] = pd.to_numeric(df_mov["Monto"], errors="coerce")

        df_mov.dropna(subset=["Fecha", "Monto"], inplace=True)
        df_mov.sort_values("Fecha", inplace=True)

        df_cat = pd.DataFrame()

        return df_mov, df_cat