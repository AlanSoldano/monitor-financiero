from config import *
from utils.helpers import normalize_text


class Categorizer:
    def __init__(self, df_categories):

        self.rules = {
            normalize_text(row[KEYWORD_COLUMN]): row[CATEGORY_COLUMN]
            for _, row in df_categories.iterrows()
        }

    def categorize(self, df):

        def match_category(description):
            description = normalize_text(description)

            for keyword, category in self.rules.items():
                if keyword in description:
                    return category

            return DEFAULT_CATEGORY

        df["Categoria"] = df[DESCRIPTION_COLUMN].apply(match_category)

        return df