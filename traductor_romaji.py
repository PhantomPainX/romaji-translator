import mutagen, pykakasi, os, api_genius
from tqdm import tqdm
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen import MutagenError
from mutagen.id3 import ID3, USLT, Encoding

# -------------------- Configuraciones ----------------------

# example: D:/Users/Manuel/Musica/canciones_test

ruta = ""

# Activar la obtención de lyrics de canciones desde Genius
# Se detectara automaticamente si la cancion ya tiene

# Activate obtaining song lyrics from Genius
# It will be automatically detected if the song already has

obtener_lyrics = False

#-----------------------Nota | Note [IMPORTANTE]
"""
Si algunas canciones no se traducen de los signos japones a romajo, cambia la variable esLatino = 0 
en el inicio del codigo de la traduccion, luego intercambia los metodos de deteccion en cada
tipo de archivo en el codigo referidos como comentarios "Deteccion caracteres latinos en letra" y 
Deteccion caracter の en letra

If some songs are not translated from the Japanese signs to Romajo, change the variable esLatino = 0
at the beginning of the translation code, then swap the detection methods in each
type of file in the code referred to as comments "Deteccion caracteres latinos en letra" and
Deteccion caracter の en letra
"""

# ---------------------- Contadores ------------------------
flac_traducido = 0
flac_sin_letra = 0
flac_char_latino = 0

mp3_traducido = 0
mp3_sin_letra = 0
mp3_char_latino = 0

archivo_ini = 0
error = 0

agregado_lyric = 0
# --------------- Obtener letras desde la api ----------------------

os.system('cls')

print("Agregando letras desde Genius")
print("")

if obtener_lyrics == True:
    for root, dir, files in os.walk(ruta):
        for file in tqdm(files,desc="Procesando", ncols=100):

            archivo = os.path.join(root, file)

            if ".ini" in file:
                continue

            song = api_genius.Cancion(archivo)

            if song.letra[0] == 'errorValido':
                continue
            elif song.letra[0] == 'errorLetra':
                continue
            elif song.letra[0] == 'noEncontrada':
                continue

            else:
                if song.esFlac:

                    song.archivo_cancion['LYRICS'] = song.letra[0]
                    song.archivo_cancion.save()
                    
                    agregado_lyric += 1

                elif song.esMp3:

                    song.archivo_cancion.setall("USLT", [USLT(encoding=Encoding.UTF8, text=song.letra[0])])
                    song.archivo_cancion.save()

                    agregado_lyric += 1

#--------------------------- Traduccion caracteres japoneses a romaji ---------------------------------------

romaji = pykakasi.kakasi()
contador_archivos = 0

for root, dir, files in os.walk(ruta):
    for file in files:

        contador_archivos += 1


os.system('cls')
print("Traduciendo Caracteres JPN a Romaji")
print("")

for root, dir, files in os.walk(ruta):

    for file in tqdm(files,desc="Procesando", ncols=100):

        esLatino = 1

        archivo = os.path.join(root, file)

        if ".ini" in file:
            archivo_ini += 1
            continue

        try:
            # Es un archivo flac
            cancion = FLAC(archivo)

            try:
                lista_letra = cancion["LYRICS"]
            except:
                flac_sin_letra += 1
                continue
            
            # Deteccion caracteres latinos en letra
            """
            try:
                for i in range(30, 50):
                    if "a" in lista_letra[0][i] or "e" in lista_letra[0][i] or "i" in lista_letra[0][i] or "o" in lista_letra[0][i]:
                        esLatino = 1
            
                if esLatino == 1:
                    flac_char_latino += 1
                    
                    continue
            except:
                error += 1
                continue
            """

            # Deteccion caracter の en letra
            try:
                for i in range(len(lista_letra[0])):
                    if "の" in lista_letra[0][i]:
                        esLatino = 0  
                if esLatino == 1:
                    flac_char_latino += 1
                    continue
            except:
                error += 1
                continue    
            
            cadena_traducida = ""
            opciones_traduccion = romaji.convert(lista_letra[0])
            #print(opciones_traduccion)
            for forma in opciones_traduccion:

                traduccion = str(forma['passport'])

                if traduccion == "kun":

                    traduccion = "kimi"

                if traduccion == "ha":

                    traduccion = "wa"

                if "\r\n\r\n" in traduccion:
                    cadena_traducida += "{}\r\n\r\n".format(traduccion.replace("\r\n", ""))

                elif "\r\n" in traduccion:
                    cadena_traducida += "{}\r\n".format(traduccion.replace("\r\n", ""))

                elif "\n\n" in traduccion:
                    cadena_traducida += "{}\n\n".format(traduccion.replace("\n", ""))
                
                elif "\n" in traduccion:
                    cadena_traducida += "{}\n".format(traduccion.replace("\n", ""))

                else:
                    cadena_traducida += "{} ".format(traduccion)

            lista_letra[0] = cadena_traducida

            #print(lista_letra)

            cancion['LYRICS'] = lista_letra[0]
            cancion.save()

            flac_traducido += 1


        except MutagenError:
            # Es un archivo mp3

            try:
                cancion = ID3(archivo)
            except:
                error += 1
                continue

            try:
                letra = cancion.getall('USLT')[0]
            except:
                mp3_sin_letra += 1
                continue

            list_letra = [letra.text]

            # Deteccion caracteres latinos en letra
            """
            try:
                for i in range(30, 50):
                    if "a" in list_letra[0][i] or "e" in list_letra[0][i] or "i" in list_letra[0][i] or "o" in list_letra[0][i]:
                        esLatino = 1
            
                if esLatino == 1:
                    mp3_char_latino += 1
                    continue
            except:
                error += 1
                continue
            """
            # Deteccion caracter の en letra
            try:
                for i in range(len(list_letra[0])):
                    if "の" in list_letra[0][i]:
                        esLatino = 0  
                if esLatino == 1:
                    mp3_char_latino += 1
                    continue
            except:
                error += 1
                continue


            cadena_traducida = ""
            opciones_traduccion = romaji.convert(list_letra[0])
            #print(opciones_traduccion)
            for forma in opciones_traduccion:

                traduccion = str(forma['passport'])

                if traduccion == "kun":

                    traduccion = "kimi"

                if traduccion == "ha":

                    traduccion = "wa"

                if "\r\n\r\n" in traduccion:
                    cadena_traducida += "{}\r\n\r\n".format(traduccion.replace("\r\n", ""))

                elif "\r\n" in traduccion:
                    cadena_traducida += "{}\r\n".format(traduccion.replace("\r\n", ""))

                elif "\n\n" in traduccion:
                    cadena_traducida += "{}\n\n".format(traduccion.replace("\n", ""))
                
                elif "\n" in traduccion:
                    cadena_traducida += "{}\n".format(traduccion.replace("\n", ""))

                else:
                    cadena_traducida += "{} ".format(traduccion)

            list_letra[0] = cadena_traducida

            #print(list_letra)

            cancion.setall("USLT", [USLT(encoding=Encoding.UTF8, text=list_letra[0])])
            cancion.save()

            mp3_traducido += 1

os.system('cls')

print("FLAC: (Traducidas {} | Sin Letra {} | Caracteres Latinos {})".format(flac_traducido,flac_sin_letra,flac_char_latino))
print("")
print("Mp3: (Traducidas {} | Sin Letra {} | Caracteres Latinos {})".format(mp3_traducido,mp3_sin_letra,mp3_char_latino))
print("")
print("Letra agregada a {} canciones desde Genius" .format(agregado_lyric))
print("")
print("Canciones escaneadas correctamente: {}" .format(flac_traducido+flac_sin_letra+mp3_traducido+
                                            mp3_sin_letra+mp3_char_latino+flac_char_latino))
print("Canciones con error {}" .format(error))
print("Archivos ini: {}" .format(archivo_ini))
print("---------------------")
print("Total: {}" .format(flac_traducido+flac_sin_letra+mp3_traducido+mp3_sin_letra+error+archivo_ini+
                                            mp3_char_latino+flac_char_latino))