from PIL import Image
import shutil
import requests
import random
from trnl import Trnl
from plugins.transloader import transloader
from plugins.gdrvclean import gdrvauth
import os
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
import logging
from googleapiclient.http import MediaFileUpload
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def gdrvupload(image):
    service = gdrvauth()
    file_metadata = {'name': image}
    media = MediaFileUpload(image,mimetype='image/jpg')
    file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
    image_id = file.get("id")
    service.permissions().create(fileId=image_id,
                                               body={"additionalRoles":[],"role":"reader","type":"anyone","withLink":"true"},
                                               fields='id').execute()
    gdrv_lk = 'https://drive.google.com/file/d/' + image_id + '/view?usp=sharing'
    base = Trnl.sh2.acell('K2').value
    poster_link = 'https://drive.google.com/uc?export=download&id=' + image_id
    Trnl.sh2.update('R2',poster_link)

def crop_height(enl_h,tf_h):
    top = random.randint(200,enl_h)
    while top + tf_h > enl_h:
        top = random.randint(100,enl_h)
    if top + tf_h < enl_h:
        return top

def fdmn_frame(vlink):
    if not os.path.exists('fdmn_post_frame.png'):
        base = Trnl.sh2.acell('K2').value
        post_url = 'https://drive.google.com/file/d/18UhVlm7g73wckU_QE52k-w8A2NjJlvaI/view?usp=sharing'
        post_link = transloader(base, post_url)
        post_response = requests.get(post_link, stream=True)
        with open('fdmn_post_frame.png', 'wb') as out_file:
            shutil.copyfileobj(post_response.raw, out_file)
        del post_response
        #
        thumb_url = 'https://drive.google.com/file/d/1h8w2szRyKP8EtDy1UF3ve-0-gEYvKBkf/view?usp=sharing'
        thumb_link = transloader(base, thumb_url)
        thumb_response = requests.get(thumb_link, stream=True)
        with open('fdmn_thumb_frame.png', 'wb') as out_file:
            shutil.copyfileobj(thumb_response.raw, out_file)
        del thumb_response
    response = requests.get(vlink, stream=True)
    with open('mv_poster.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    
    #OPENING POSTER PHOTO
    poster_org = Image.open('mv_poster.png', 'r')
    #OPENING FRAME PHOTOS
    post_frame = Image.open('fdmn_post_frame.png', 'r')
    thumb_frame = Image.open('fdmn_thumb_frame.png', 'r')
    #GETTING PHOTO SIZES
    po_w, po_h = poster_org.size
    pf_w, pf_h = post_frame.size
    tf_w, tf_h = thumb_frame.size
    #RESIZING POSTER FOR THUMB
    po_top = poster_org.resize((1465, 2160))
    enl_w,enl_h = tf_w,int(po_h/po_w*tf_w)
    po_bot = poster_org.resize((enl_w,enl_h))
    #RESIZING POSTER FOR POST
    pp_w, pp_h = 1810, 2715
    pp = poster_org.resize((pp_w, pp_h))
    #CREATING POST POSTER
    blank_frame = Image.new('RGB', (pf_w, pf_h), (255, 255, 255, 255))
    offset = (int((pf_w-pp_w)/2), int((pf_h-pp_h)/2))
    blank_frame.paste(pp,offset)
    blank_frame.paste(post_frame, (0,0),mask=post_frame)
    blank_frame.save('post_poster_v2.jpg')
    #UPLOADING TO GOOGLE DRIVE
    gdrvupload('post_poster_v2.jpg')
    #blank_frame.show()
    #CREATING THUMB POSTER
    left = 0
    top = crop_height(enl_h,tf_h)
    right = tf_w
    bottom = top+tf_h
    po_stf = po_bot.crop((left,top,right,bottom))
    po_stf.paste(thumb_frame,None,mask=thumb_frame)
    left = 2200 - int(1465/2)
    top = 0
    right = left + 1465
    bottom = top + 2160
    po_stf.paste(po_top,(left,top,right,bottom))
    po_tf_s320 = po_stf.resize((320,int(tf_h*320/tf_w)))
    po_tf_s320.save('thumb_poster.jpg')
    #po_tf_s320.show()
