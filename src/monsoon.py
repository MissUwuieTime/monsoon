from constant import Embedded, Stylesheet
from controller import EventDataController, LeagueClientController
from service import ExecutorService, TimerService
from template import SystemTray
from util import b64_to_qicon
from view import MainView

import asyncio
import logging
from PySide6 import QtWidgets

def milliseconds_from_fps(fps: int) -> int:
  """Calculate milliseconds from the rate of frames per second.

  Args:
      fps (int): Frames per second

  Returns:
      int: Milliseconds
  """
  return (1 / fps) * 1000

def create_app() -> QtWidgets.QApplication:
  """Create our main Qt application with settings applied.

  Returns:
      QtWidgets.QApplication: Main application
  """
  app = QtWidgets.QApplication([])
  app.setStyleSheet(Stylesheet.value())
  app.setWindowIcon(b64_to_qicon(Embedded.icon()))

  return app

def create_tray() -> SystemTray:
  """Create our system tray with actions.

  Returns:
      SystemTray: System tray
  """
  tray = SystemTray()
  tray.show()

  return tray

async def main(
  client_controller: LeagueClientController,
  event_data_controller: EventDataController,
  executor: ExecutorService):
  """Asynchronously run the main application.
  """
  view = MainView(
    event_data_controller=event_data_controller,
    client_controller=client_controller
  )

  # Refresh view based on update tick rate (20fps)
  update_timer = TimerService(milliseconds_from_fps(20))
  update_timer.add_slot(view.refresh)

  await executor.exec_event_loop()

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  app = create_app()
  tray = create_tray()
  client_controller = LeagueClientController()
  event_data_controller = EventDataController()
  executor = ExecutorService(
    app=app, 
    client_controller=client_controller,
    event_data_controller=event_data_controller,
    ui_event_loop=loop
    )
  try:
    loop.run_until_complete(
      main(
        client_controller=client_controller,
        event_data_controller=event_data_controller,
        executor=executor
      )
    )
  except KeyboardInterrupt:
    executor.is_program_exiting = True
    loop.run_until_complete(executor._kill_willump())
    print()