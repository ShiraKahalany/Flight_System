from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class PurchaseSummaryView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)
        layout.addWidget(self.back_button)

        # Create a matplotlib figure and canvas for the graph
        self.figure, self.ax = plt.subplots()  # Create a figure and axes
        self.canvas = FigureCanvas(self.figure)  # Create a canvas widget

        # Add the matplotlib toolbar (optional)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add the toolbar and canvas to the layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plot_graph(self, months, purchases):
        """Plots the graph of purchases over the last 12 months."""
        self.ax.clear()  # Clear the previous plot if any
        self.ax.plot(months, purchases, marker='o', linestyle='-', color='b')
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Number of Purchases')
        self.ax.set_title('Ticket Purchases in the Last 12 Months')

        self.canvas.draw()  # Render the plot on the canvas
