import cv2
import datetime

def get_duration(filename):
    video = cv2.VideoCapture(filename)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT) 
    fps = video.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    duration = str(datetime.timedelta(seconds=seconds))
    hrs = duration.split(':')[0]
    mnt = duration.split(':')[1]
    scd = duration.split(':')[2]
    if seconds < 60:
        rntm = '{} စက္ကန့်'.format(scd)
    elif 3600 > seconds >= 60:
        rntm = '{} မိနစ် {} စက္ကန့်'.format(mnt,scd)
    elif seconds >= 3600:
        rntm = '{} နာရီ {} မိနစ် {} စက္ကန့်'.format(hrs,mnt,scd)
    return rntm
