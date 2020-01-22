from lyric_scraper import AZLyricScraper
from tqdm import tqdm
import logging

def collectLyrics(artist_name, artist_name_bis = '', ouput_path = 'lyrics.txt'):
    """
    Collects all available lyrics of a given artist from AZlyrics.com into a txt file
    
    INPUT
    -----
        -artist_name : str, name of the artist to collect lyrics from
        -artist_name_bis (optional):  str, sometimes an alternative artist name
                                      is used to access the song list page  on 
                                      AZlyrics.com of a given artist such as 
                                      'Kanye West' and 'West'
        -ouput_path : str, the txt filepath to save lyrics into
    """
    scraper = AZLyricScraper()
    if len(artist_name_bis)>0:
        song_list = scraper.list_songs(artist_name_bis)
    else:
        song_list = scraper.list_songs(artist_name)
    while('\n\n') in song_list:
        song_list.remove('\n\n')
    logging.info("Collecting " + artist_name + "'s lyrics...")
    f= open(ouput_path,"w+")
    for track_name in tqdm(song_list) :
        lyrics = scraper.get_lyrics(artist_name, track_name)
        f.write(lyrics + "\n")
    logging.info("Done")
    f.close()