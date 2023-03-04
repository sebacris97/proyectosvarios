import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re
#para transformar letras con acento en letras sin acento
from unidecode import unidecode


#hace distintas transformaciones para que la url de azlyrics sea valida
#si la banda empieza con the, se lo saca
#si el titulo de la cancion tien palabra1-palabra2 lo deja en palabra1palabra2
#si el titulo o artista tiene acentos transofrma las letras a la letra sin acento
#si el titulo es palabra1 - palabra2 deja solo palabra1
#si el titulo es palabra1 (palabra2) solo deja palabra 1
#con estas transformaciones suele enecontrar cualquier letra que este disponible
def parse_url(artist_name, track_name):
    url_artist = artist_name.lower()
    url_artist = unidecode(url_artist)
    if url_artist.split(' ')[0] == 'the':
        url_artist = ''.join(url_artist.split(' ')[1:])
    url_artist = url_artist.replace(' ','')
    url_artist = re.sub("[^a-zA-Z]+", "", url_artist)
    url_track = unidecode(''.join(track_name.split(" - ")[0].replace(' ','').split('-')).split('(')[0].replace('&','').replace('ñ','n').lower())
    url_track = re.sub("[^a-zA-Z0-9]+", "", url_track)
    url = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track+'.html'
    print(url)
    return url

#recibe nombre artista y nombre de cancion y retorna la letra si es que existe
#o no lyrics si no la encuentra
def get_lyrics(artist_name, track_name):
    
    #setting up the url according to azlyrics criteria
    url = parse_url(artist_name, track_name)
    request = requests.get(url)
    
    #si la pagina existe
    if request.status_code != 404:
        html_text = request.content#text
        #si uso text en vez de content tengo problemas con caracteres español
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find_all('div')[22].text #el div 22 tiene la letra

    return 'no lyrics'
