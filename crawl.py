import requests as rq
from lxml import etree
import json
import subprocess
import os 


def work(url,cookie):
    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.",
        "Referer":"http://www.bilibili.com",
        "cookie":cookie
        }
    web=rq.get(url,headers=header).text

    html=etree.HTML(web)#尋找影片標題
    title=html.xpath("//h1[@class='video-title']")[0].text
    for invalid in ['*','"','/','\\','<','>',':','|','?',' ']:
        title=title.replace(invalid,'')#影片標題的非法符號和空格必須消除，否則可能會報錯

    
    os.chdir(os.path.expanduser('~/Downloads'))
    os.makedirs('./BilibiliSave/{}'.format(title),exist_ok=True)

    script=html.xpath("//head//script[4]")[0]#xpath搜索后結果為list格式，需要從list中提取
    str_script=str(script.text)

    json_script=str_script.replace("window.__playinfo__=","")#移除多餘部分，從json轉換成dict格式
    dict_script=json.loads(json_script)


    video_data_list=dict_script['data']['dash']['video']
    audio_data_list=dict_script['data']['dash']['audio']

    video_source=video_data_list[0]['baseUrl']#video audio存放地址
    audio_source=audio_data_list[0]['baseUrl']


    v=open('./BilibiliSave/{}/video.mp4'.format(title),'wb')#下載video和audio
    v.write(rq.get(video_source,headers=header).content)
    v.close()
    a=open('./BilibiliSave/{}/audio.mp3'.format(title),'wb')
    a.write(rq.get(audio_source,headers=header).content)
    a.close()


    subprocess.run("ffmpeg -y -i ./BilibiliSave/{}/video.mp4 -i ./BilibiliSave/{}/audio.mp3 -c copy ./BilibiliSave/{}/combined.mp4".format(title,title,title) )#合成video和audio
    return title,' 下載成功。'

