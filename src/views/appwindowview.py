from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from viewmodels import AppWindowViewModel
  from models import DynamicBalanceModel
from constants import Monsoon
from utils import LayoutFactory, StretchTypes
from views import QImage, QChampionTemplate

from dependency_injector.wiring import Provide, inject
from PySide6 import QtWidgets, QtCore, QtGui

class AppWindowView(QtWidgets.QMainWindow):
  @inject
  def __init__(
    self,
    app_window_viewmodel: AppWindowViewModel = Provide["app_window_viewmodel"]
  ):
    super().__init__()
    self.viewmodel = app_window_viewmodel
    self.setObjectName(self.viewmodel.object_name)

    # Setup the view
    self.vbox = LayoutFactory.create_vertical_proxy()
    self.title_bar = LayoutFactory.create_horizontal_proxy()
    self.content_area = LayoutFactory.create_horizontal_proxy()
    self.team_champions_panel = LayoutFactory.create_vertical_proxy()
    self.team_champions_list_box = LayoutFactory.create_vertical_proxy()
    self.available_champions_panel = LayoutFactory.create_vertical_proxy()
    self.available_champions_list_box = LayoutFactory.create_grid_proxy()

    self.title_bar.layout.addWidget(QImage(self.viewmodel.wordmark_qpixmap))
    self.title_bar.widget.setMaximumHeight(64)

    self.team_champions_panel_label = QtWidgets.QLabel("Team Champions")
    self.team_champions_panel_label.setStyleSheet("""
    QWidget {
      font-size: 15pt;
      font-weight: 600;
    }
    """)
    self.team_champions_panel.layout.addWidget(self.team_champions_panel_label)
    self.team_champions_list_box_widgets: QChampionTemplate = []
    for i in range(5):
      widget = QChampionTemplate()
      widget.set_champion_image_text_stylesheet("""
      QWidget {
        font-size: 13pt;
        font-weight: light;
      }
      """)
      self.team_champions_list_box.layout.addWidget(widget)
      self.team_champions_list_box_widgets.append(widget)
    self.team_champions_list_box.widget.setSizePolicy(LayoutFactory.create_size_policy(StretchTypes.VERTICAL, 3))
    self.team_champions_panel.layout.addWidget(self.team_champions_list_box.widget)

    self.available_champions_panel_label = QtWidgets.QLabel("Available Champions")
    self.available_champions_panel_label.setStyleSheet("""
    QWidget {
      font-size: 15pt;
      font-weight: 600;
    }
    """)
    self.available_champions_panel.layout.addWidget(self.available_champions_panel_label)
    self.available_champions_list_box_widgets: QChampionTemplate = []
    for i in range(2):
      for j in range(5):
        widget = QChampionTemplate()
        widget.set_champion_image_text_stylesheet("""
        QWidget {
          font-size: 13pt;
          font-weight: light;
        }
        """)
        self.available_champions_list_box.layout.addWidget(widget, j+1, i+1)
        self.available_champions_list_box_widgets.append(widget)
    self.available_champions_list_box.widget.setSizePolicy(LayoutFactory.create_size_policy(StretchTypes.VERTICAL, 1))
    self.available_champions_panel.layout.addWidget(self.available_champions_list_box.widget)

    self.team_champions_panel.widget.setSizePolicy(LayoutFactory.create_size_policy(StretchTypes.HORIZONTAL, 1))
    self.content_area.layout.addWidget(self.team_champions_panel.widget)
    self.available_champions_panel.widget.setSizePolicy(LayoutFactory.create_size_policy(StretchTypes.HORIZONTAL, 2))
    self.content_area.layout.addWidget(self.available_champions_panel.widget)
    self.vbox.layout.addWidget(self.title_bar.widget)
    self.vbox.layout.addWidget(self.content_area.widget)

    # Subscribe to viewmodel events
    self.viewmodel.property_changed += self.on_property_changed

    # Set window properties
    self.resize(self.viewmodel.width, self.viewmodel.height)
    self.setWindowTitle(self.viewmodel.window_title)
    self.setCentralWidget(self.vbox.widget)
  
  def on_property_changed(self, event, args) -> None:
    for x in self.available_champions_list_box_widgets:
      widget: QChampionTemplate = x
      widget.clear_contents()
    for x in self.team_champions_list_box_widgets:
      widget: QChampionTemplate = x
      widget.clear_contents()
    
    for (i, x) in enumerate(self.viewmodel.available_champion_dynamic_balances):
      balance: DynamicBalanceModel = x
      widget: QChampionTemplate = self.available_champions_list_box_widgets[i]
      if balance.champion_icon is not None:
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(balance.champion_icon)
        widget.set_champion_image(pixmap)
      widget.set_champion_image_text(balance.champion_name)
      widget.set_champion_text(balance.format())
    
    for (i, x) in enumerate(self.viewmodel.team_champion_dynamic_balances):
      balance: DynamicBalanceModel = x
      widget: QChampionTemplate = self.team_champions_list_box_widgets[i]
      if balance.champion_icon is not None:
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(balance.champion_icon)
        widget.set_champion_image(pixmap)
      widget.set_champion_image_text(balance.champion_name)
      widget.set_champion_text(balance.format())
      
