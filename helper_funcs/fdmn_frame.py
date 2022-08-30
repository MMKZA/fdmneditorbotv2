from PIL import Image
import shutil
import requests
from trnl import Trnl
from plugins.transloader import transloader

import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    
def fdmn_frame(vlink):
    if os.path.exists('myback.png'):
        pass
    elif not os.path.exists('myback.png'):
        base = Trnl.sh2.acell('K2').value
        url = 'https://drive.google.com/file/d/1LPX16iYs4mE6fd5lfqtz5lWJxZpPV6Bc/view?usp=sharing'
        frame_link = transloader(base, url)
        response = requests.get(frame_link, stream=True)
        with open('myback.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    
    response = requests.get(vlink, stream=True)
    with open('mv_poster.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    
    poster1 = Image.open('mv_poster.png', 'r')
    pst_w, pst_h = poster1.size
    background = Image.open('myback.png', 'r')
    bg_w, bg_h = background.size
    posterbot = poster1.resize((bg_w, bg_h))
    postertop = poster1.resize((1465, 2160))
    posterbot.paste(background, (0,0),mask=background)
    posterbot.save('paste1.png')
    paste1 = Image.open('paste1.png', 'r')
    paste1.paste(postertop,(1188,0))
    save_path = Config.DOWNLOAD_LOCATION + "/1700943365/fdmn_thumb.png"
    paste1.save(save_path)
