from PyQt5.QtWidgets import (
  QMainWindow,
  QMessageBox,
  QFileDialog,
)
from PyQt5.QtCore import pyqtSlot
from pytube import YouTube

# API Package
from API.ui.mainwindow import Ui_MainWindow
from API.models.functions import Read
import config.config as cc
import icon_rc

import json
import os


class SnapTube(QMainWindow):
  def __init__(self):
    super().__init__()

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.resize(cc.WIDTH, cc.HEIGHT)
    self.move(cc.X, cc.Y)
    self.setStyleSheet(Read(cc.THEME))
    
    self.PATH_EXISTS = f"C:/Users/{os.getlogin()}/Videos/SnapTube"
    if os.path.exists(self.PATH_EXISTS):
      pass
    else:
      os.mkdir(self.PATH_EXISTS)

    self.readDump()
    self.check_path()

    self.ui.homeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.homePage))
    self.ui.youtubeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.youtubePage))
    self.ui.moreBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.morePage))
    self.ui.watchBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.watchPage))
    self.ui.aboutBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.aboutPage))
    self.ui.settingsBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settingsPage))
    
    self.ui.Get_streamBtn.clicked.connect(self.get_availbale_resolutions)
    self.ui.browseBtn.clicked.connect(self.selectFileWork)
    self.ui.download_youtube_videoBtn.clicked.connect(self.download_from_youtube)

    self.ui.statusBar.showMessage('Ready.')
  
  # https://youtu.be/_Td7JjCTfyc?si=oNvpchJCwbXGaFCi

  def get_availbale_resolutions(self):
    self.ui.statusBar.showMessage("Loading resolutions...")
    url = self.ui.inputUrlVideo_youtube.text()
    lists = []
    if url == "":
      QMessageBox.about(self, "Error", "Please interyour link")
    else:
      video = YouTube(url)
      streams = video.streams.all()
      for stream in streams:
        self.ui.comboBox.addItem(stream.resolution)
      
  
  def readDump(self):
    with open(os.path.join("data", "data.json"), "r") as readdump:
      code = json.load(readdump)

    self.ui.lineEdit.setText(code["path_save_video"])

    
  def selectFileWork(self) :
    folder_dialog = QFileDialog()
    folder_path = folder_dialog.getExistingDirectory(self, "Choose a Folder of save")

    with open(os.path.join("data", "data.json"), "r") as readdump:
      code = json.load(readdump)
    code["path_save_video"] = folder_path + "/"

    with open(os.path.join("data", "data.json"), "w") as writedump:
      json.dump(code, writedump)
    self.readDump()

  def check_path(self):
    with open(os.path.join("data", "data.json"), "r") as readdump:
      code = json.load(readdump)
    if code["path_save_video"] == "":
      code["path_save_video"] = self.PATH_EXISTS + "/"
    else: pass
    with open(os.path.join("data", "data.json"), "w") as writedump:
      json.dump(code, writedump)
    self.readDump()

  @pyqtSlot()
  def download_from_youtube(self):
    self.ui.statusBar.showMessage("Downloading...")
    with open(os.path.join("data", "data.json"), "r") as readdump:
      code = json.load(readdump)
    url_youtube = self.ui.inputUrlVideo_youtube.text()
    resolution = self.ui.comboBox.currentText()
    print(resolution)
    yt = YouTube(str(url_youtube))
    stream = yt.streams.get_by_resolution(resolution=resolution)
    _title = yt.title
    stream.download(output_path=code["path_save_video"], filename=str(_title + ".mp4"))