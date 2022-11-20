from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from viewmodels import MainWindowViewModel
from constants import Monsoon
from utils import LayoutFactory

from dependency_injector.wiring import Provide, inject
from PySide6 import QtWidgets, QtCore
import os
import traceback


class MainWindowView(QtWidgets.QMainWindow):
  @inject
  def __init__(
    self,
    main_window_viewmodel: MainWindowViewModel = Provide["main_window_viewmodel"]
    ):

    super().__init__()
    self.viewmodel = main_window_viewmodel
    self.setObjectName(self.viewmodel.object_name)

    # Set instance variables
    (self.hbox, self.hbox_layout) = LayoutFactory.create_horizontal()
    (self.left_vbox, self.left_vbox_layout) = LayoutFactory.create_vertical()
    (self.left_sub_hbox, self.left_sub_hbox_layout) = LayoutFactory.create_horizontal()
    (self.middle_vbox, self.middle_vbox_layout) = LayoutFactory.create_vertical()
    (self.right_vbox, self.right_vbox_layout) = LayoutFactory.create_vertical()
    (self.team_damages_vbox, self.team_damages_vbox_layout) = LayoutFactory.create_vertical()
    (self.team_others_vbox, self.team_others_vbox_layout) = LayoutFactory.create_vertical()
    (self.bench_info_grid, self.bench_info_grid_layout) = LayoutFactory.create_grid()
    (self.app_info_hbox, self.app_info_hbox_layout) = LayoutFactory.create_horizontal()
    self.team_damages_rows = [LayoutFactory.create_label_with_text_shadow() for i in range(5)]
    self.team_others_rows = [LayoutFactory.create_label_with_text_shadow() for i in range(5)]
    self.bench_info_cells = [LayoutFactory.create_label_with_text_shadow() for i in range(10)]

    # Set horizontal box columns
    self.hbox_layout.addWidget(self.left_vbox, 35)
    self.hbox_layout.addWidget(self.middle_vbox, 58)
    self.hbox_layout.addWidget(self.right_vbox, 35)

    # Set left box rows
    self.left_vbox_layout.addWidget(self.app_info_hbox, 2)
    self.left_vbox_layout.addWidget(self.left_sub_hbox, 8)
    self.left_vbox_layout.addWidget(QtWidgets.QLabel(""), 3)

    # Set left sub horizontal box columns
    self.left_sub_hbox_layout.addWidget(QtWidgets.QLabel(""), 3)
    self.left_sub_hbox_layout.addWidget(self.team_damages_vbox, 2)
    self.left_sub_hbox_layout.addWidget(self.team_others_vbox, 2)

    # Set middle box rows
    self.middle_vbox_layout.addWidget(self.bench_info_grid, 1)
    self.middle_vbox_layout.addWidget(QtWidgets.QLabel(""), 13)

    # Set team damages rows
    for row in self.team_damages_rows:
      self.team_damages_vbox_layout.addWidget(row)
    
    # Set team others rows
    for row in self.team_others_rows:
      self.team_others_vbox_layout.addWidget(row)

    # Set bench info cells
    self.bench_info_grid.setContentsMargins(0, 0, 0, 0)
    self.bench_info_grid_layout.setHorizontalSpacing(10)
    for i, cell in enumerate(self.bench_info_cells):
      self.bench_info_grid_layout.addWidget(cell, 1, i, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

    # Set application info columns
    wordmark_label = QtWidgets.QLabel("")
    wordmark_label.setPixmap(self.viewmodel.wordmark)
    wordmark_label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
    wordmark_label.setScaledContents(True)
    self.app_info_hbox_layout.addWidget(wordmark_label)
    

    # Set window properties
    self.resize(Monsoon.WIDTH.value, Monsoon.HEIGHT.value)
    self.setWindowTitle(Monsoon.TITLE.value)
    self.setWindowFlags(
      QtCore.Qt.FramelessWindowHint 
      | QtCore.Qt.WindowStaysOnTopHint
      | QtCore.Qt.Tool
      )
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)

    self.setCentralWidget(self.hbox)

    # Set event subscriptions
    self.viewmodel.property_changed += self.refresh

  def _clear_bench_info_labels(self):
    for label in self.bench_info_cells:
      label.setText("")
      label.setToolTip("")

  def hide_window(self):
    self.hide()

  def show_window(self):
    self.show()
    
  def refresh(self, sender, event_args):
    # Adjust view based on League client (lock onto it)
    self.setGeometry(self.viewmodel.left, self.viewmodel.top, self.viewmodel.width, self.viewmodel.height)
    if not self.viewmodel.is_league_client_active:
      self.hide_window()
      return
    try:
      if not self.viewmodel.is_session_active:
        self.hide_window()
        return

      # Process team balances
      for i, balance in enumerate(self.viewmodel.team_balances):
        self.team_damages_rows[i].setText(balance)
        if len(balance) > 0 and "Other changes" in self.viewmodel.team_other_balances[i]:
          self.team_others_rows[i].setText("ℹ️")
          self.team_others_rows[i].setToolTip(self.viewmodel.team_other_balances[i])
        else:
          self.team_others_rows[i].setText("")
          self.team_others_rows[i].setToolTip("")
        
      # Process bench balances
      self._clear_bench_info_labels()
      for i, balance in enumerate(self.viewmodel.bench_balances):
        if len(balance) > 0:  
          self.bench_info_cells[i].setText("ℹ️")
          self.bench_info_cells[i].setToolTip(balance)
        else:
          self.bench_info_cells[i].setText("")
          self.bench_info_cells[i].setToolTip("")
      # Hide overlay if client window is not in foreground
      if self.viewmodel.is_client_foreground or self.viewmodel.is_client_overlayed:
        self.show_window()
      else:
        self.hide_window()

    except Exception:
      msg = QtWidgets.QMessageBox()
      msg.setIcon(QtWidgets.QMessageBox.Critical)
      msg.setText("Error")
      msg.setInformativeText(traceback.format_exc())
      msg.setWindowTitle(":bee_sad:")
      msg.exec_()
      os._exit(-1)

