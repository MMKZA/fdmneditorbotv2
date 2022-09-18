from trnl import Trnl
from translation import Translation
import time
import imdb as imdbpy
import datetime
import math
from si_prefix import si_format
import re

def imdb_data(imdb_id):
    imdb_id = re.findall(r'\b\d+\b', str(imdb_id))[0]
    ia = imdbpy.Cinemagoer()
    movie = ia.get_movie(imdb_id)
    return movie

def imdb_info(imdb_id):
    imdb_id = re.findall(r'\b\d+\b', str(imdb_id))[0]
    ia = imdbpy.Cinemagoer()
    movie = ia.get_movie(imdb_id)
    title = movie.data['title']
    kind = movie.data['kind']
    if 'series' in kind:
        year = movie.data['series years']
        if str(year)[-1] == '-':
            year = '{}{}'.format(year,datetime.date.today().year)
    else:
        year = movie.data['year']
    vcap = '{} ({})'.format(title,year)
    vcap_hsh = ''.join(e for e in vcap if e.isalnum())
    mv_gnr = '⁉️'
    if 'genres' in movie.data.keys():
        mv_gnr = ', '.join(movie.data['genres'])
    rntm = '⁉️'
    if 'runtimes' in movie.data.keys():
        seconds = int(movie.data['runtimes'][0])*60
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
    imdb = '⁉️'
    if 'rating' in movie.data.keys() and 'votes' in movie.data.keys():
        imdb_rt = movie.data['rating']
        imdb_vt = si_format(movie.data['votes'],0)
        imdb = '{}/10 ({} Votes)'.format(imdb_rt,imdb_vt)
    ctry = '⁉️'
    if 'countries' in movie.data.keys():
        ctry = ', '.join(movie.data['countries'])
    phto_url = '⁉️'
    if 'cover url' in movie.data.keys():
        phto_lst = movie.data['cover url'].split('.')
        phto_lst[-2] = '_V1_FMjpg_UX1000_'
        phto_url = '.'.join(phto_lst)
    web_url = Trnl.sh2.acell('M2').value
    credit = '⁉️'
    credit_lst = {'channelmyanmar':'Channel Myanmar','goldchannel':'Gold Channel Movies','burmesesubtitles':'Burmese Subtitles','shweflix':'ShweFlix'}
    for c in credit_lst:
        if c in web_url:
            credit = str(credit_lst[c])        
    if Trnl.sh2.acell('M4').value == '⁉️' and rntm != '⁉️':
        Trnl.sh2.update('M4', rntm)
    if Trnl.sh2.acell('M3').value == '⁉️' and mv_gnr != '⁉️':
        Trnl.sh2.update('M3', mv_gnr)
    if Trnl.sh2.acell('M6').value == '⁉️' and ctry != '⁉️':
        Trnl.sh2.update('M6', ctry)
    Trnl.sh2.update('D2', vcap)
    Trnl.sh2.update('P4', kind)
    Trnl.sh2.update('E2', vcap_hsh)
    Trnl.sh2.update('M5', year)
    Trnl.sh2.update('C2', phto_url)
    Trnl.sh2.update('C4',phto_url)
    Trnl.sh2.update('M8', imdb)
    Trnl.sh2.update('F2', credit)
