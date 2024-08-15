from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class StatisticsView(QMainWindow):
    def __init__(self, product_service):
        super().__init__()
        self.product_service = product_service
        self.setWindowTitle("Statistics")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.label = QLabel("Sales Statistics")
        self.layout.addWidget(self.label)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.update_statistics()

    def update_statistics(self):
        products = self.product_service.get_all_products()
        # Example: Plotting product quantities
        names = [p[1] for p in products]
        quantities = [p[2] for p in products]

        self.ax.clear()
        self.ax.bar(names, quantities)
        self.canvas.draw()
