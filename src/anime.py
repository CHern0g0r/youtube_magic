'''
https://docs.api.jikan.moe/#tag/anime/operation/getAnimeRelations
https://www.animesonglyrics.com/results?_token=fGarEonvS5aNpjRQAZKQkQiyOSy87mMe4jabw8WG&q=friren
'''

import ast
import requests

from bs4 import BeautifulSoup


def get_op_id_from_lyrics(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, features='lxml')
    scripts = soup.find_all('script')
    ids = []
    for scr in scripts:
        text = scr.string
        if text and text.startswith('yapi'):
            text = text[5:-1]
            idx = text.split(',')[0][1:-1]
            ids.append(idx)
    return ids


if __name__ == '__main__':
    # url = 'https://www.animesonglyrics.com/sousou-no-frieren/yuusha'
    url = 'https://www.animesonglyrics.com/sousou-no-frieren/yuusha/video#videotab2'
    get_op_url(url)