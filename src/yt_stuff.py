import re
import shutil

from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser

from pytube import Playlist, YouTube, StreamQuery
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


def form_playlist():
    pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--link', required=True)
    parser.add_argument('--output_path', default='./art')
    parser.add_argument('--combine', action='store_true')
    args = parser.parse_args()
    
    download_playlist(
        args.link, args.output_path,
        combine=args.combine
    )