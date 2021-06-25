import lyricsgenius, pykakasi
from lyricsgenius.api.public_methods import song
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, USLT, Encoding
from mutagen import MutagenError

token = 'GeniusTOKEN'
genius = lyricsgenius.Genius(token)

class Cancion:

    def __init__(self, archivo):

        self.archivo = archivo
        esValido = False
        tieneLetra = False
        self.esFlac = False
        self.esMp3 = False

        try:
            # Es un archivo flac
            song = FLAC(archivo)

            self.esFlac = True

            try:
                so = song["LYRICS"]
                tieneLetra = True
            except:
                tieneLetra = False
                esValido = True

                try:
                    artista = song["artist"]
                    nombreCancion = song["title"]

                    artista = artista[0]
                    nombreCancion = nombreCancion[0]
                except:
                    esValido = False

        except MutagenError:

            try:
                song = ID3(archivo)
                esValido = True

                self.esMp3 = True

                try:
                    letra = song.getall('USLT')[0]
                    tieneLetra = True
                except:
                    tieneLetra = False

                    artista = song.getall('TPE1')[0]
                    nombreCancion = song.getall('TIT2')[0]

                    artista = artista[0]
                    nombreCancion = nombreCancion[0]

            except:
                esValido = False

        if self.esFlac:
            self.archivo_cancion = FLAC(archivo)
        elif self.esMp3:
            self.archivo_cancion = ID3(archivo)


        if esValido == False:
            self.letra = ['errorValido']
        elif tieneLetra == True:
            self.letra = ['errorLetra']

        else:

            self.cancion = genius.search_song(nombreCancion, artista, get_full_info=False)
            try:
                self.letra = [self.cancion.lyrics]
            except:
                self.letra = ['noEncontrada']

    def obtener_archivo(self):
        return self.archivo_cancion



