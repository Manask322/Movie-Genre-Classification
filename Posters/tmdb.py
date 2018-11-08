import os
import requests
import pandas as pd
import tmdb as tb
import os

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
KEY = '53566b3f0e15c689ebe4667fe8a6e554'
nr=0          
def _get_json(url):
    r = requests.get(url)
    return r.json()
    
def _download_images(url, path='/home/manas/Desktop/Desktop/movie-genre-master/movie-genre-master/Posters'):
    """download all images in list 'urls' to 'path' """
    global nr
    # for nr, url in enumerate(urls):
    r = requests.get(url)
    filetype = r.headers['content-type'].split('/')[-1]
    filename = 'poster_{0}.{1}'.format(nr+1,filetype)
    filepath = os.path.join(path, filename)
    with open(filepath,'wb') as w:
        w.write(r.content)
    nr=nr+1

def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id

        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size. 

        Args:
            imdbid (str): IMDB id of the movie

        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url) 

    return poster_urls

def tmdb_posters(imdbid, count=None, outpath='.'):    
    urls = get_poster_urls(imdbid)
    # print len(urls)
    # if count is not None:
    #     urls = urls[:count]
    print len(urls)
    _download_images(urls[0], outpath)

if __name__=="__main__":
    df=pd.read_csv("FormattedMovieData2.csv")
    ID=list(df.ID)
    Num=list(df.Num)
    for i,num in zip(ID,Num):
	    tb.tmdb_posters(i)