import pandas as pd

from pathlib import Path
from tqdm import tqdm
from pytube import Channel, YouTube, Playlist


url = ''

path = Path('')


def main():
    # video = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    # stream = video.streams.filter(only_audio=True).first()
    # stream.download(filename=f"{video.title}.mp3")
    # print("The video is downloaded in MP3")

    table = path / 'log.csv'
    if table.exists():
        log = pd.read_csv(table)
    else:
        log = pd.DataFrame({
            'id': [],
            'title': [],
            'watched': []
        })

    done = set(map(str, log['id']))
    print(done)

    c = Channel(url)
    for i, vurl in enumerate(tqdm(c.video_urls)):
        video = YouTube(vurl, use_oauth=True, allow_oauth_cache=True)
        pre, idx = video.title.split('#')
        title = '_'.join(pre.split('|')[0].strip().split(' '))
        mp_title = '_'.join([idx, title])

        if idx not in done:
            print('Download:', mp_title)
            row = pd.DataFrame({
                'id': [idx],
                'title': [title],
                'watched': [False]
            })
            filepath = path / 'videos'
            stream = video.streams.filter(only_audio=True).first()
            stream.download(output_path=filepath, filename=f'{mp_title}.mp3')
            done.add(idx)
            log = pd.concat([row, log], ignore_index=True)
        if i == 50:
            break
    log.to_csv(table, index=False)


if __name__ == '__main__':
    main()
    print('end')
