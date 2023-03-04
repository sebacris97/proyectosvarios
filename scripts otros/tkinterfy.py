import spotipy
import spotipy.util as util
from tkinter import *
from tkinter.scrolledtext import *

import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re

#para transformar letras con acento en letras sin acento
from unidecode import unidecode


def login_spotify(username,client_id,client_secret,redirect_url,scope):
    # Set up credentials and authenticate with Spotify API
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_url)
    return spotipy.Spotify(auth=token)

def create_window(title,size,topmost):
    # Create a window to display the information
    root = Tk()
    root.geometry("310x410")
    root.title("Current Track Info")
    root.attributes('-topmost', 'true') #que este siempre encima de todo
    return root

def setting_up_window(root):
    title = StringVar()
    artist = StringVar()
    album = StringVar()
    contador = DoubleVar()
    title_label = Label(root,textvariable = title)
    artist_label = Label(root,textvariable = artist)
    album_label = Label(root,textvariable = album)
    contador_label = Label(root,textvariable = contador)
    text=ScrolledText(root, font="Verdana 10",wrap=WORD)
    text.pack() #con pack la pongo en la ventana
    return [title,contador,text,artist,album]


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

def actualizar():
    
    current_track = sp.current_user_playing_track()
    
    # Extract relevant information from response
    if current_track is not None:
        
        try:
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']
            album_name = current_track['item']['album']['name']
        except:
            track_name = ''
            artist_name = ''
            album_name = ''
            pass

        try:
            text.yview(contador.get())
            contador.set(contador.get()+0.25) #0.25 es la velocidad a la que scrollea las letras
        except:
            pass

        if title.get() != track_name:

            contador.set(0) #empieza cancion nueva el contador vuelve a 0
            text.delete('1.0',END) #se borran las letras de la cancion anterior
                

            title.set(track_name)
            artist.set(artist_name)
            album.set(album_name)



            title.set(track_name) #le ponemos a la variable title el titulo de la cancion actual
            text.insert(END, track_name+'\n')
            text.insert(END, artist_name+'\n')
            text.insert(END, album_name+'\n\n')


            
            #getting the lyrics

            #setting up the url according to azlyrics criteria
            url = parse_url(artist_name, track_name)
            request = requests.get(url)
            
            #si la pagina existe
            if request.status_code != 404:
                
                html_text = request.content#text
                #si uso text en vez de content tengo problemas con caracteres español
                
                soup = BeautifulSoup(html_text, 'html.parser')

                lyrics_text = soup.find_all('div')[22].text #el div 22 tiene la letra

                for i in lyrics_text:
                    text.insert(END, i)
                
            else:
                text.insert(END, 'no lyrics avaiable')
            
    else:
        text.delete('1.0',END)
        text.insert(END, 'no song playing')
        title.set('')

    #llamado recursivo cada 500ms
    root.after(500,actualizar)





username = 'sebacris97'
client_id = '4809312ab757475e83bdf86881c70558'
client_secret = '883ba1bdd5fd4b63829a826160d05b90'
redirect_url = 'http://localhost:8888/callback'
scope = 'user-read-currently-playing'
sp = login_spotify(username,client_id,client_secret,redirect_url,scope)

size = "310x410"
window_title = "Current track info"
topmost = True #que este siempre encima de todo  
root = create_window(window_title,size,topmost)

#recibe una ventana de parametro
title,contador,text,artist,album = setting_up_window(root)
        
root.after(500,actualizar)

