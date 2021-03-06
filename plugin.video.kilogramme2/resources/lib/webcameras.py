# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import App
from App import P
from urlparse import urlparse, parse_qs


@P.cached(30)
@P.action()
def wc_index(params):
    items = []

    url = 'http://live.saimanet.kg'
    content = App.http_request(url)
    if content:
        html = BeautifulSoup(content, 'html.parser')
        for camera in html.find_all(class_='onemaincam'):
            try:
                camera = camera.find(class_='title').find('a')
                label = App.bs_get_text(camera)
                href = camera.get('href')

                content = App.http_request(url + href)
                if content:
                    html1 = BeautifulSoup(content, 'html.parser')
                    iframe = html1.find('iframe')
                    youtubeId = iframe.get('src').split('/')[-1]
                    items.append(
                        {
                            'label': label,
                            'url': 'plugin://plugin.video.youtube?action=play_video&videoid=' + youtubeId,
                            'is_playable': False
                        }
                    )
                    # source = html1.find('source')
                    # items.append(
                    #     {
                    #         'label': label,
                    #         'url': source.get('src'),
                    #         'is_playable': True
                    #     }
                    # )
            except:
                pass

    url = 'https://elcat.kg/translation/'
    content = App.http_request(url)
    if content:
        html = BeautifulSoup(content, 'html.parser')
        for div in html.find_all(class_='tranlation__item'):
            try:
                title = div.find('h2').text
                camera_number = div.get('id').split('_')[1]
                camera_div = html.find(id='start_stream' + camera_number)
                camera_src = camera_div.find('iframe').get('src')
                camera_name = camera_src.split('?')[1].split('&')[0].split('=')[1]
                
                items.append(
                    {
                        'label': title,
                        'url': 'https://webcam.elcat.kg:5443/LiveApp/streams/' + camera_name +'.m3u8?token=null ',
                        'is_playable': True
                    }
                )
            except:
                pass
    
    petro_cameras = [
        {
            'label': 'Петрозаводск, площадь Кирова',
            'url': 'http://s1.moidom-stream.ru/s/public/0000000088.m3u8'
        },
        {
            'label': 'Петрозаводск, Московская - Варкауса',
            'url': 'http://s1.moidom-stream.ru/s/public/0000002179.m3u8'
        },
        {
            'label': 'Петрозаводск, Онежская набережная',
            'url': 'http://s1.moidom-stream.ru/s/public/0000000103.m3u8'
        },
        {
            'label': 'Петрозаводск, Древлянское кольцо',
            'url': 'http://s1.moidom-stream.ru/s/public/0000000192.m3u8'
        },
        
    ]
    
    for camera in petro_cameras:
        items.append(
            {
                'label': camera['label'],
                'url': camera['url'],
                'is_playable': True
            }
        )


    petro_cameras = [
        'https://moigorod.sampo.ru/stream/156',
        'https://moigorod.sampo.ru/stream/125',
        'https://moigorod.sampo.ru/stream/17',
        'https://moigorod.sampo.ru/stream/20',
        'https://moigorod.sampo.ru/stream/58',
        'https://moigorod.sampo.ru/stream/295',
        'https://moigorod.sampo.ru/stream/117',
        'https://moigorod.sampo.ru/stream/186',
        'https://moigorod.sampo.ru/stream/198',
        'https://moigorod.sampo.ru/stream/25'
    ]
    for url in petro_cameras:
        items.append(getSampoStream(url))

    return items


def getSampoStream(url):
    content = App.http_request(url)
    if content:
        html = BeautifulSoup(content, 'html.parser')
        label = html.find('h1').text.encode('utf-8')
        result = re.compile("src : '(.+?)',").findall(content)
        if len(result) > 0:
            src = result[0]
            return {
                'label': 'Петрозаводск, ' + label,
                'url': src,
                'is_playable': True
            }