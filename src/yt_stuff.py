import re
import shutil

from tqdm import tqdm
from urllib import request
from urllib.parse import urlparse, parse_qs
from typing import List
from pathlib import Path
from argparse import ArgumentParser

from pytube import Playlist, YouTube, StreamQuery, Search
from moviepy.editor import (
    AudioFileClip, concatenate_audioclips,
    VideoFileClip, concatenate_videoclips
)

from http.client import IncompleteRead


def select_stream(streams: StreamQuery,
                  only_audio: bool = True,
                  hq: bool = True):
    return streams.filter(only_audio=only_audio).first()


def _download_playlist(link: str,
                       output_path: str,
                       *,
                       only_audio: bool = True,
                       combine: bool = False):
    path = Path(output_path)
    savepath = path
    if combine:
        savepath = path / 'tmp'
    savepath.mkdir(exist_ok=True, parents=True)

    pl = Playlist(link)
    download_list = []
    for vurl in tqdm(pl.video_urls):
        video = YouTube(vurl, use_oauth=True, allow_oauth_cache=True)
        title = re.sub(
            r' |\.|/', '_', video.title
        )
        download_list.append(title)
        if only_audio:
            stream = select_stream(video.streams)

            stream.download(
                output_path=savepath,
                filename=f'{title}.mp4'
            )
        else:
            raise NotImplementedError('only audio for now')
    
    if combine:
        Clip = AudioFileClip
        concat = concatenate_audioclips
        parts = []
        for name in download_list:
            filepath = str(savepath / f'{name}.mp4')
            part = Clip(filepath)
            parts.append(part)

        title = re.sub(
            r' |\.|/', '_', pl.title
        )
        outpath = str(path / f'{title}.mp3')
        final_clip: AudioFileClip = concat(parts)
        final_clip.write_audiofile(outpath)
        shutil.rmtree(savepath)


def download_playlist(*args, **kwargs):
    try:
        _download_playlist(*args, **kwargs)
    except IncompleteRead as e:
        print('ERROR')
        print(e)


def form_playlist(ids: List[str]):
    videos_url = (
        "http://www.youtube.com/watch_videos?video_ids=" +
        ','.join(ids)
    )
    pl_id = request.urlopen(videos_url).geturl().split('list=')[1]
    pl_url = (
        "https://www.youtube.com/playlist?list=" +
        pl_id +
        "&disable_polymer=true"
    )
    return pl_url


def form_playlist_from_urls(list_of_urls: List[str]):
    ids = map(
        lambda url: parse_qs(urlparse(url).query)['v'][0],
        list_of_urls
    )
    return form_playlist(ids)


def search_whole(titles: List[str]):
    urls = []
    for title in titles:
        s = Search(title)

        # Find opening itself
        for i, r in enumerate(s.results):
            url = r.watch_url
            urls.append(url)
            break
    print(len(urls))
    return urls


if __name__ == '__main__':
    # parser = ArgumentParser()
    # parser.add_argument('--link', required=True)
    # parser.add_argument('--output_path', default='./art')
    # parser.add_argument('--combine', action='store_true')
    # args = parser.parse_args()
    
    # download_playlist(
    #     args.link, args.output_path,
    #     combine=args.combine
    # )

    lst = [
        'Ao no Sumika (青のすみか)" by Tatsuya Kitani (キタニタツヤ)',
        '"SPECIALZ" by King Gnu'
    ]
    search_whole(lst)

    # urls = [
    #     "https://www.youtube.com/watch?v=NaMkdLfcFys&list=PLK4PlFPZ-gb7QreGrHl1sQUmwfnDSaCNG&index=2&ab_channel=RecommendedForYou",
    #     "https://www.youtube.com/watch?v=D_B9wC3kYyQ&list=PLK4PlFPZ-gb7QreGrHl1sQUmwfnDSaCNG&index=1&t=6s&ab_channel=MOJHAJO%27STECHNIQUE"
    # ]
    # form_playlist(urls)
