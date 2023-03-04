import requests
from bs4 import BeautifulSoup
import os
import sys
import pathlib
from pathlib import Path
import urllib
import urllib.parse as urlparse
import urllib.request

from pyunpack import Archive

print("escriba el nombre de la pelicula:\n")

buscador='https://www.subdivx.com/index.php?accion=5&masdesc=&buscar2='




while True:
    palabra=input().replace(" ","%20").lower()
    buscador2=buscador+palabra

    vgm_url = buscador2
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    links = []
    for link in soup.find_all('a',{'class': 'titulo_menu_izq'}):
        aux=link.get('href')
        links.append(aux)
        print(aux)

    if len(links)==0:
        print("NO SE ENCONTARON SUBTITULOS")
        sys.exit()

    downloadble_links=[]

    for link in links:
      vgm_url = link
      html_text = requests.get(vgm_url).text
      soup = BeautifulSoup(html_text, 'html.parser')
      for d_link in soup.find_all('a',{'class': 'link1'}):
        aux='https://www.subdivx.com/'+d_link.get('href')
        downloadble_links.append(aux)
        print(aux)

    print(*downloadble_links[:], sep='\n')
    path=pathlib.Path(__file__).parent.resolve() / palabra
    Path(path).mkdir(parents=True, exist_ok=True)

    for link in downloadble_links:
        identifier = link[37:link.index('&')]
        if link[-1]!='1':
            url = 'https://www.subdivx.com/sub'+link[-1]+'/'+identifier
        else:
            url = 'https://www.subdivx.com/sub/'+identifier
        extension = '.rar'
        r = requests.get(url+extension,allow_redirects=True)
        if r.status_code!=200:
            extension = '.zip'
            r = requests.get(url+extension,allow_redirects=True)
        file_name = path/(identifier+extension)
        print(file_name)
        with open(file_name, 'wb') as outfile:
            outfile.write(r.content)
        try:
            Archive(file_name).extractall(path)
        except:
            pass
        os.remove(file_name)

    print (str(len(links))+" subtitulos encontrados")
