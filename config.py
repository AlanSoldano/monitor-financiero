from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Archivo Excel por defecto
DEFAULT_EXCEL_FILE = DATA_DIR / "gastos.xlsx"

# Categoría por defecto
DEFAULT_CATEGORY = "Otros"

# Columnas hoja movimientos
DATE_COLUMN = "Fecha"
DESCRIPTION_COLUMN = "Descripción"
AMOUNT_COLUMN = "Monto"
ACCOUNT_COLUMN = "Cuenta"

# Columnas hoja categorias
KEYWORD_COLUMN = "Keyword"
CATEGORY_COLUMN = "Categoria"

# Nombres de hojas
MOVEMENTS_SHEET = "movimientos"
CATEGORIES_SHEET = "categorias"

# Logging
LOG_LEVEL = "INFO"