import sys
from PySide6 import QtWidgets
from constant import Embedded, Monsoon
from util import b64_to_qicon

class SystemTray(QtWidgets.QSystemTrayIcon):
  def __init__(self):
    super().__init__()
    
    # Setup system tray icon
    self.setIcon(b64_to_qicon(Embedded.icon()))
    self.setToolTip(Monsoon.TITLE.value)

    # Set context menu
    menu = QtWidgets.QMenu()

    # Setup context menu items
    title = menu.addAction(f"{Monsoon.TITLE.value}")
    title.setEnabled(False)
    menu.addSeparator()
    github = menu.addAction("GitHub")
    menu.addSeparator()
    exit = menu.addAction("Exit")
    exit.triggered.connect(self.__exit_application)

    self.setContextMenu(menu)
  
  def __exit_application(self):
    sys.exit()