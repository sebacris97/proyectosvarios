import spotipy
import spotipy.util as util
from tkinter import *
import tkinter.scrolledtext as scrolledtext

import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re

#para transformar letras con acento en letras sin acento
from unidecode import unidecode




# Set up credentials and authenticate with Spotify API
username = 'sebacris97'
client_id = '4809312ab757475e83bdf86881c70558'
client_secret = '883ba1bdd5fd4b63829a826160d05b90'
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-read-currently-playing'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)


def actualizar():
    current_track = sp.current_user_playing_track()
    
    # Extract relevant information from response
    if current_track is not None:

        #donothing_text.set('')
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        album_name = current_track['item']['album']['name']

        if title.get() != track_name:
            text.delete('1.0',END)
                
            # Add labels for track information
            title.set(track_name)
            artist.set(artist_name)
            album.set(album_name+'\n')

            #setting up the url according to azlyrics criteria
            url_artist = artist_name.lower()
            url_artist = unidecode(url_artist)
            if url_artist.split(' ')[0] == 'the':
                url_artist = ''.join(url_artist.split(' ')[1:])
            url_artist = url_artist.replace(' ','')
            url_artist = re.sub("[^a-zA-Z]+", "", url_artist)
            url_track = unidecode(track_name.replace(' ','').split('-')[0].split('(')[0].replace('&','').replace('ñ','n').lower())
            url_track = re.sub("[^a-zA-Z0-9]+", "", url_track)
            url = 'https://www.azlyrics.com/lyrics/'+url_artist+'/'+url_track+'.html'
            print(url)
            
            #getting the lyrics
            request = requests.get(url)
            if request.status_code != 404:
                html_text = request.content#text
                #si uso text en vez de content tengor problemas con caracteres español
                soup = BeautifulSoup(html_text, 'html.parser')
                
                lyrics_text = soup.find_all('div')[22].text

                text.insert(END, track_name+'\n')
                text.insert(END, artist_name+'\n')
                text.insert(END, album_name+'\n\n')
                for i in lyrics_text:
                    text.insert(END, i)

                
                #showing lyrics on window
                #lyrics.set(lyrics_text)
                
            else:
                
                text.insert(END, 'no lyrics avaiable')
            
    else:
        text.delete('1.0',END)
        text.insert(END, 'no song playing')
                    
##        title.set('')
##        artist.set('')
##        album.set('')
##        lyrics.set('')
##        donothing_text.set('No current track playing')

    root.after(500,actualizar)



# Create a window to display the information
root = Tk()
root.geometry("310x410")
root.title("Current Track Info")

title = StringVar()
artist = StringVar()
album = StringVar()
##donothing_text = StringVar()
##lyrics = StringVar()
track_label = Label(root,textvariable = title)
artist_label = Label(root,textvariable = artist)
album_label = Label(root,textvariable = album)
##nothing_label = Label(root,textvariable = donothing_text)
##lyrics_label = Label(root,textvariable = lyrics)

v=Scrollbar(root, orient='vertical')
v.pack(side='right', fill='y')
text=Text(root, font="Verdana 10", yscrollcommand=v.set, wrap=WORD)
text.tag_configure("center", justify='center')
text.tag_add("center", 1.0, "end")
v.config(command=text.yview)
text.pack()

##track_label.pack()
##artist_label.pack()
##album_label.pack()
##lyrics_label.pack()
##nothing_label.pack()




root.attributes('-topmost', 'true')
        
root.after(500,actualizar)
