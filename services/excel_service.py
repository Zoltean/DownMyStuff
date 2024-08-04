import pandas as pd

class ExcelService:
    @staticmethod
    def import_products_from_excel(file_path):
        df = pd.read_excel(file_path)
        products = df.to_dict(orient='records')
        return products

    @staticmethod
    def export_products_to_excel(products, file_path):
        df = pd.DataFrame(products)
        df.to_excel(file_path, index=False)
