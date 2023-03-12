import spotipy
import spotipy.util as util
from tkinter import *
from tkinter.scrolledtext import *
from unidecode import unidecode
#from az import get_lyrics
#import azapi
from lyrics_extractor import SongLyrics

class LyricsWindow(Tk):

    def __init__(self):
        super().__init__()

        #self.API = azapi.AZlyrics()
        GCS_API_KEY = 'AIzaSyCfPLivvWZu_rLf3dCceZMWxvNS6NQ2SVk'
        GCS_ENGINE_ID = 'b68b26a7f065541a7'
        self.API = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)

        username = 'sebacris97'
        client_id = '4809312ab757475e83bdf86881c70558'
        client_secret = '883ba1bdd5fd4b63829a826160d05b90'
        redirect_url = 'http://localhost:8888/callback'
        scope = 'user-read-currently-playing'
        self.sp = self.login_spotify(username,client_id,client_secret,redirect_url,scope)

        size = "345x410"
        window_title = "Current track info"
        topmost = True #que este siempre encima de todo  
        self.configure_window(window_title,size,topmost)

        #recibe una ventana de parametro
        self.song_title,self.album,self.artist, self.song_time = self.setting_up_window()

        self.actualizar()
    
    def login_spotify(self,username,client_id,client_secret,redirect_url,scope):
        # Set up credentials and authenticate with Spotify API
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_url)
        return spotipy.Spotify(auth=token)

    def configure_window(self,title,size,topmost):
        # Create a window to display the information
        self.geometry(size)
        self.title("Current Track Info")
        self.attributes('-topmost', 'true') #que este siempre encima de todo

    def setting_up_window(self):
        title = StringVar()
        album = StringVar()
        artist = StringVar()
        song_time = StringVar()
        title_label = Label(self,textvariable = title)
        album_label = Label(self,textvariable = album)
        artist_label = Label(self,textvariable = artist)
        song_time_label = Label(self,textvariable = song_time)
        self.lyrics_text = ScrolledText(self, wrap=WORD, font="Verdana 10")
        self.lyrics_text.bind("<Key>", lambda e: "break") #desactiva el escribir
        title_label.pack()
        album_label.pack()
        artist_label.pack()
        song_time_label.pack()
        self.lyrics_text.pack()
        return [title,album,artist,song_time]

    #imprimir minutos en formato mm:ss
    def tiempo(self,current_time, total_time):
        minutes1,seconds1 = divmod(current_time / 1000, 60)
        minutes2,seconds2 = divmod(total_time / 1000, 60)
        current_time = f"{minutes1:02.0f}:{seconds1:05.2f}".split('.')[0]
        total_time = f"{minutes2:02.0f}:{seconds2:05.2f}".split('.')[0]
        return current_time+' - '+total_time

    def check_song(self):
        current_track = self.sp.current_user_playing_track()
        if current_track is not None and current_track['currently_playing_type'] != 'episode':
            try:
                self.track_name = current_track['item']['name']
                self.track_artist = current_track['item']['artists'][0]['name']
                self.track_album = current_track['item']['album']['name']
                self.current_time = current_track["progress_ms"]
                self.total_time = current_track['item']["duration_ms"]
                return current_track
            except:
                self.check_song()
        else:
            return None
            
    def actualizar_lyrics_text(self):
        #self.API.artist = unidecode(self.track_artist) #cambio caracteres de otro idioma por ingles
        #self.API.title = unidecode(self.track_name)
        #lyrics = self.API.getLyrics(ext='lrc')
        #self.lyrics_text.insert(END, lyrics if type(lyrics) != int else 'No lyrics found')
        try:
            lyrics = self.API.get_lyrics(unidecode(self.track_name+' '+self.track_artist))['lyrics']
            self.lyrics_text.insert(END, lyrics)
            self.lyrics_text.insert(1.0,'\n\n\n')
            self.lyrics_text.insert(END,'\n\n\n')
        except:
            self.lyrics_text.insert(END, 'No lyrics found')

    def actualizar_tiempo(self):
        self.song_time.set(self.tiempo(self.current_time,self.total_time))

    def actualizar_y(self):
        cociente = (self.current_time/self.total_time)*0.725
        self.lyrics_text.yview_moveto(cociente)
        
    def actualizar(self):

        if self.check_song() != None:

            self.actualizar_y()
            self.actualizar_tiempo()

            if self.song_title.get() != self.track_name: #si cambio la cancion

                self.lyrics_text.delete('1.0',END)
                self.song_title.set(self.track_name)
                self.album.set(self.track_album)
                self.artist.set(self.track_artist)
                self.actualizar_lyrics_text()
        else:
            self.song_title.set('No song\'s playing')
            self.album.set('')
            self.artist.set('')
            self.song_time.set('')
            self.lyrics_text.delete('1.0',END)
            self.lyrics_text.insert(END, 'no lyrics to show')
            self.title("Current Track Info")
            
        self.after(250,self.actualizar) #llamado recursivo cada 500ms
        

def main():
    window = LyricsWindow()
    window.mainloop()
    

if __name__ == "__main__":
    main()
