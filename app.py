import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit, QGroupBox, QDoubleSpinBox, QSpinBox, QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QFont, QFontDatabase

from elements import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cellWidth = 0
        self.cellHeight = 0
        self.selected = Element()

        self.setWindowTitle("Label Maker by Filip Pernea")
        # self.resize(1920, 1080)

        # print(QFontDatabase.families())

        main = QWidget()
        self.setCentralWidget(main)

        layout = QGridLayout(main)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(5, 1)

        #############
        # LEFT MENU #
        #############
        leftMenu = QVBoxLayout()
        layout.addLayout(leftMenu, 0, 0, 12, 1)

        leftMenu.addWidget(QLabel("All measurements are in millimeters"))

        # PAPER DIMENSIONS
        dimensions = QGroupBox()
        dimensions.setTitle("Paper dimensions")
        leftMenu.addWidget(dimensions)

        self.width = QDoubleSpinBox()
        self.height = QDoubleSpinBox()
        self.width.setMaximum(999)
        self.height.setMaximum(999)

        self.width.setValue(210)
        self.height.setValue(297)

        self.width.valueChanged.connect(self.reloadCell)
        self.height.valueChanged.connect(self.reloadCell)

        dimensionsLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Width: "))
        row1.addWidget(self.width)
        dimensionsLayout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Height:"))
        row2.addWidget(self.height)
        dimensionsLayout.addLayout(row2)

        dimensions.setLayout(dimensionsLayout)

        # PAPER MARGINS
        margins = QGroupBox()
        margins.setTitle("Paper margins")
        leftMenu.addWidget(margins)

        self.top = QDoubleSpinBox()
        self.bottom = QDoubleSpinBox()
        self.left = QDoubleSpinBox()
        self.right = QDoubleSpinBox()
        self.top.setMaximum(999)
        self.bottom.setMaximum(999)
        self.left.setMaximum(999)
        self.right.setMaximum(999)

        self.top.valueChanged.connect(self.reloadCell)
        self.bottom.valueChanged.connect(self.reloadCell)
        self.left.valueChanged.connect(self.reloadCell)
        self.right.valueChanged.connect(self.reloadCell)

        marginsLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Top: "))
        row1.addWidget(self.top)
        marginsLayout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Bottom:"))
        row2.addWidget(self.bottom)
        marginsLayout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Left: "))
        row3.addWidget(self.left)
        marginsLayout.addLayout(row3)
        
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Right:"))
        row4.addWidget(self.right)
        marginsLayout.addLayout(row4)

        margins.setLayout(marginsLayout)

        # CELLS NO.
        cellsNo = QGroupBox()
        cellsNo.setTitle("Labels no.")
        leftMenu.addWidget(cellsNo)

        self.horizontal = QSpinBox()
        self.vertical = QSpinBox()
        self.horizontal.setMaximum(999)
        self.vertical.setMaximum(999)

        self.horizontal.setValue(1)
        self.vertical.setValue(1)

        self.horizontal.valueChanged.connect(self.reloadCell)
        self.vertical.valueChanged.connect(self.reloadCell)

        cellsNoLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Labels no. horizontal: "))
        row1.addWidget(self.horizontal)
        cellsNoLayout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Labels no. vertical:"))
        row2.addWidget(self.vertical)
        cellsNoLayout.addLayout(row2)

        cellsNo.setLayout(cellsNoLayout)

        # CELLS
        cells = QGroupBox()
        cells.setTitle("Label dimensions")
        leftMenu.addWidget(cells)

        self.cellWidthLabel = QLabel("n/a")
        self.cellHeightLabel = QLabel("n/a")

        cellsLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Width: "))
        row1.addWidget(self.cellWidthLabel)
        cellsLayout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Height:"))
        row2.addWidget(self.cellHeightLabel)
        cellsLayout.addLayout(row2)

        cells.setLayout(cellsLayout)

        leftMenu.addStretch()

        ##########
        # CANVAS #
        ##########
        canvas = QGroupBox()
        canvas.setTitle("Design canvas")
        canvasLayout = QVBoxLayout()
        layout.addWidget(canvas, 1, 1, 11, 4)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setBackgroundBrush(Qt.transparent)

        self.scene.setSceneRect(0, 0, 160, 90)

        self.paper = self.scene.addRect(30, 30, 100, 50)
        self.paper.setBrush(QBrush(Qt.white))
        self.paper.setPen(QPen(Qt.black, 0))
        self.paper.setZValue(-1)

        self.zeroText = self.scene.addText("0", QFont("Cascadia Code"))
        self.zeroText.setPos(0, 0)

        self.xText = self.scene.addText("x: 100 mm", QFont("Cascadia Code"))
        self.xText.setPos(130, 0)

        self.yText = self.scene.addText("y: 50 mm", QFont("Cascadia Code"))
        self.yText.setPos(20, 90)
        self.yText.setRotation(90)

        canvasLayout.addWidget(self.view)

        canvas.setLayout(canvasLayout)

        ####################
        # CANVAS CONTROLLS #
        ####################

        controlls = QGroupBox()
        controlls.setTitle("Canvas controlls")
        controllsLayout = QHBoxLayout()
        layout.addWidget(controlls, 0, 1, 1, 4)

        self.zoomControlls = QDoubleSpinBox()
        self.zoomControlls.setMaximum(10)
        self.zoomControlls.setMinimum(0.1)
        self.zoomControlls.setSingleStep(0.1)

        self.zoomControlls.setValue(0.2)

        self.zoomControlls.valueChanged.connect(self.reloadElements)

        controllsLayout.addWidget(QLabel("Zoom level: "))
        controllsLayout.addWidget(self.zoomControlls)

        controlls.setLayout(controllsLayout)

        ##############
        # RIGHT MENU #
        ##############
        rightMenu = QVBoxLayout()
        layout.addLayout(rightMenu, 0, 5, 12, 1)

        # ITEM DATA
        data = QGroupBox()
        data.setTitle("Item data")
        rightMenu.addWidget(data)

        self.nameLabel = QLabel("no item selected!")
        self.idLabel = QLabel("")

        dataLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Name: "))
        row1.addWidget(self.nameLabel)
        dataLayout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("ID: "))
        row2.addWidget(self.idLabel)
        dataLayout.addLayout(row2)

        data.setLayout(dataLayout)

        # DIMENSIONS
        itemDimensions = QGroupBox()
        itemDimensions.setTitle("Item dimensions")
        rightMenu.addWidget(itemDimensions)
        
        self.positionX = QDoubleSpinBox()
        self.positionY = QDoubleSpinBox()
        self.scaleX = QDoubleSpinBox()
        self.scaleY = QDoubleSpinBox()
        self.positionX.setMaximum(999)
        self.positionY.setMaximum(999)
        self.scaleX.setMaximum(999)
        self.scaleY.setMaximum(999)

        self.positionX.valueChanged.connect(self.reloadCell)
        self.positionY.valueChanged.connect(self.reloadCell)
        self.scaleX.valueChanged.connect(self.reloadCell)
        self.scaleY.valueChanged.connect(self.reloadCell)

        itemDimensionsLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Position X: "))
        row1.addWidget(self.positionX)
        row1.addWidget(QLabel("mm"))
        itemDimensionsLayout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Position Y: "))
        row2.addWidget(self.positionY)
        row2.addWidget(QLabel("mm"))
        itemDimensionsLayout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Size X: "))
        row3.addWidget(self.scaleX)
        row3.addWidget(QLabel("mm"))
        itemDimensionsLayout.addLayout(row3)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Size Y: "))
        row4.addWidget(self.scaleY)
        row4.addWidget(QLabel("mm"))
        itemDimensionsLayout.addLayout(row4)

        itemDimensions.setLayout(itemDimensionsLayout)

        # SETTINGS
        settings = QGroupBox()
        settings.setTitle("Item settings")
        rightMenu.addWidget(settings)

        settingsLayout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Data: "))
        row1.addWidget(QLabel("data"))
        settingsLayout.addLayout(row1)

        settings.setLayout(settingsLayout)

        rightMenu.addStretch()

        self.reloadCell()

    def reloadCell(self):
        try:
            self.cellHeight = (self.height.value() - self.top.value() - self.bottom.value()) / self.vertical.value()
        except:
            self.cellHeight = "n/a"
        try:
            self.cellWidth = (self.width.value() - self.left.value() - self.right.value()) / self.horizontal.value()
        except:
            self.cellWidth = "n/a"

        self.cellWidthLabel.setText(f"{self.cellWidth}")
        self.cellHeightLabel.setText(f"{self.cellHeight}")

        try:
            SCALE = 10 * self.zoomControlls.value() # precision: turns 0.5 into 500 for precision and no drawing rects with 0.5 pixel width. 

            self.xText.setX(self.cellWidth * SCALE)
            self.xText.setPlainText(f"x: {self.cellWidth} mm")

            self.yText.setY(self.cellHeight * SCALE)
            self.yText.setPlainText(f"y: {self.cellHeight} mm")

            self.paper.setRect(30, 30, self.cellWidth * SCALE, self.cellHeight * SCALE)
            self.scene.setSceneRect(0, 0, self.cellWidth * SCALE + 60, self.cellHeight * SCALE + 60)
        except:
            pass

        # debug: print(f"{self.width.value() * SCALE} {self.height.value() * SCALE}")
    
    def reloadElement(self):
        pass

    def reloadElements(self):
        self.reloadCell()

app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

sys.exit(app.exec())
