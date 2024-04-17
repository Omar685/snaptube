import config.config as cc
from pytube import YouTube

def Read(file):
  with open(file, 'r') as file_read:
    code = file_read.read()
  return code


def download_video_youtube(url: str, save_path: str): 
  yt = YouTube(url=url)