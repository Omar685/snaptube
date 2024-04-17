from PyQt5.QtWidgets import QApplication

from API.mainwindow import SnapTube

import sys

def run():
  app = QApplication(sys.argv)
  window = SnapTube()
  window.show()
  sys.exit(app.exec_())