from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox
from services.excel_service import ExcelService


class ProductManagement(QMainWindow):
    def __init__(self, product_service):
        super().__init__()
        self.product_service = product_service
        self.setWindowTitle("Product Management")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.import_button = QPushButton("Import Products from Excel")
        self.export_button = QPushButton("Export Products to Excel")

        self.layout.addWidget(self.import_button)
        self.layout.addWidget(self.export_button)

        self.import_button.clicked.connect(self.import_products)
        self.export_button.clicked.connect(self.export_products)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def import_products(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            products = ExcelService.import_products_from_excel(file_path)
            for product in products:
                self.product_service.add_product(product['name'], product['quantity'], product['price'])
            QMessageBox.information(self, "Import Successful", "Products imported successfully!")

    def export_products(self):
        products = self.product_service.get_all_products()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            ExcelService.export_products_to_excel(products, file_path)
            QMessageBox.information(self, "Export Successful", "Products exported successfully!")
