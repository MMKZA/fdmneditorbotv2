import re
from translation import Translation

async def download_progress(stdout,vcap):
    raw_prog = stdout.decode().strip().replace(" ","")
    prog_lst = re.findall('\[download][0-9]*\.[0-9]+%of[0-9]*\.[0-9]+[a-zA-Z]+[0-9]*\.[0-9]+[a-zA-Z]+/sETA[0-9]+:[0-9]+', raw_prog)
    prcnt_lst = []
    ttl_sz = ''
    spd_lst = []
    eta_lst = []
    spd_kw = ['KiB/s','MiB/s','GiB/s']
    sz_kw = ['KiBat','MiBat','GiBat']
    spd_unt = []
    sz_unt = []
    for p in prog_lst:
        prcnt_lst.append(re.findall('[0-9]*\.[0-9]+%', p)[0])
        eta_lst.append(re.findall('ETA[0-9]+:[0-9]+', p)[0].replace('ETA',''))
        k = re.findall('[0-9]*\.[0-9]+[a-zA-Z]+/s', p)[0]
        for spd in spd_kw:
            if spd in k:
                spd_lst.append(k.replace(spd,''))
                spd_unt.append(spd)
        l = re.findall('[0-9]*\.[0-9]+[a-zA-Z]+',p)[0]
        for sz in sz_kw:
            if sz in l:
                ttl_sz = l.replace(sz,'')
                sz_unt.append(sz.replace('at',''))
    dld_lst = []
    for p in prcnt_lst:
        dld_lst.append("{:.2f}".format(float(p.strip('%'))*float(ttl_sz)/100))
    for i in range(0,len(prcnt_lst)):
        text = Translation.DOWNLOAD_START + '\n<code>{}</code>\nPercent Completed: {}\nDownloaded: {} of {} {}\nSpeed: {} {}\nETA: {} min : {} sec'.format(vcap,
                                                                                                       prcnt_lst[i],
                                                                                                       dld_lst[i],
                                                                                                       ttl_sz,
                                                                                                       sz_unt[i],
                                                                                                       spd_lst[i],
                                                                                                       spd_unt[i],
                                                                                                       eta_lst[i].split(':')[0],
                                                                                                       eta_lst[i].split(':')[1]
                                                                                                       )
        return text
