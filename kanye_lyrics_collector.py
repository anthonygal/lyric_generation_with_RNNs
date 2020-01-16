from lyric_scraper import AZLyricScraper
from tqdm import tqdm
import logging


def collect_kanye_lyrics(ouput_path = 'kanye_lyrics_test.txt'):
    scraper = AZLyricScraper()
    kanye_tracks = scraper.list_songs('west')
    while('\n\n') in kanye_tracks:
        kanye_tracks.remove('\n\n')
    logging.info("Collecting Kanye's lyrics...")
    print(kanye_tracks)
    f= open(ouput_path,"w+")
    for track_name in tqdm(kanye_tracks) :
        lyrics = scraper.get_lyrics('kanyewest', track_name)
        f.write(lyrics + "\n")
    logging.info("Done")
    f.close()



collect_kanye_lyrics()
