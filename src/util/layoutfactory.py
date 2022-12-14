from typing import Tuple
from PySide6 import QtWidgets, QtGui

class LayoutFactory():
    """Represents a static factory that creates layout widgets in tuple formats.
    """
    @staticmethod
    def create_grid() -> Tuple[QtWidgets.QGroupBox, QtWidgets.QGridLayout]:
      grid = QtWidgets.QGroupBox()
      grid_layout = QtWidgets.QGridLayout()
      grid_layout.setSpacing(0)
      grid.setLayout(grid_layout)

      return (grid, grid_layout)

    @staticmethod
    def create_horizontal() -> Tuple[QtWidgets.QGroupBox, QtWidgets.QHBoxLayout]:
      hbox = QtWidgets.QGroupBox()
      hbox_layout = QtWidgets.QHBoxLayout()
      hbox_layout.setSpacing(0)
      hbox.setLayout(hbox_layout)

      return (hbox, hbox_layout)
    
    @staticmethod
    def create_vertical() -> Tuple[QtWidgets.QGroupBox, QtWidgets.QVBoxLayout]:
      vbox = QtWidgets.QGroupBox()
      vbox_layout = QtWidgets.QVBoxLayout()
      vbox_layout.setSpacing(0)
      vbox.setLayout(vbox_layout)

      return (vbox, vbox_layout)

    @staticmethod
    def create_label_with_text_shadow(text="", color="black", blur_radius=4.0, offset=(1, 1)) -> QtWidgets.QLabel:
      label = QtWidgets.QLabel(text)
      effect = QtWidgets.QGraphicsDropShadowEffect(label)
      effect.setBlurRadius(blur_radius)
      effect.setColor(QtGui.QColor(color))
      effect.setOffset(*offset)
      label.setGraphicsEffect(effect)

      return label