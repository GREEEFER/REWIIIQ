from pyrogram import Client, filters
from pyrogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from os.path import exists
from json import loads,dumps 
from pathlib import Path
from os import listdir
from os import mkdir
from os import unlink
from os.path import isfile, join
from datetime import timedelta
from random import randint
import re
from re import findall
from bs4 import BeautifulSoup
from py7zr import FILTER_COPY
from multivolumefile import MultiVolume
from io import BufferedReader
from py7zr import SevenZipFile
from move_profile import move_to_profile
from urllib.parse import quote
from time import time, localtime
from yarl import URL
import asyncio
import tgcrypto
import aiohttp_socks
import aiohttp
import requests
import traceback
import time
import os
import ssl
import http.server
import socketserver
import yt_dlp
from uptodl import search, get_info
import psutil
from upload import NextcloudClient
import json
import base64

user_data = {}

ssl._create_default_https_context = ssl._create_unverified_context

def split_file(file_path, chunk_size):
    """Divide un archivo en chunks y los almacena en una lista.

    Args:
        file_path: La ruta del archivo a dividir.
        chunk_size: El tamaño de cada chunk en bytes.

    Returns:
        Una lista de rutas de archivo para cada chunk.
    """
    file_path = Path(file_path)
    file_name = file_path.name
    
    chunks = []
    with open(file_path, 'rb') as file:
        chunk_num = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_file_name = f"{file_name}_part{chunk_num}"
            chunk_file_path = file_path.parent / chunk_file_name
            chunks.append(chunk_file_path)
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_num += 1

    return chunks




from pathlib import Path
from os import unlink, walk

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)

    if fpath.is_dir():
        
        with MultiVolume(
            fpath.with_name(fpath.name + ".7z"), mode="wb", volume=volume, ext_digits=3
        ) as archive:
            with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
                if password:
                    archive_writer.set_encoded_header_mode(True)
                    archive_writer.set_encrypted_header(True)

                for root, _, files in walk(fpath):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, str(fpath))
                        archive_writer.write(file_path, relative_path)

    else:
        # If it's a file, use the existing logic
        fsize = fpath.stat().st_size

        if not volume:
            volume = fsize + 1024

        ext_digits = len(str(fsize // volume + 1))
        if ext_digits < 3:
            ext_digits = 3

        with MultiVolume(
            fpath.with_name(fpath.name + ".7z"), mode="wb", volume=volume, ext_digits=ext_digits
        ) as archive:
            with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
                if password:
                    archive_writer.set_encoded_header_mode(True)
                    archive_writer.set_encrypted_header(True)

                archive_writer.write(fpath, fpath.name)

    files = []
    for file in archive._files:
        files.append(file.name)
    # Only unlink the original path if it's a file
    if fpath.is_file(): 
        unlink(fpath)
    return files
	
	

from configs import api_id, api_hash, token
admins = ['Astro_Bots']
bot = Client("client",api_id,api_hash,bot_token=token) 
CONFIG = {}
global_conf = {
       "token": "atMYvrlxNC2BNhQplNw4bipHFl9cp3oS",
       "host": "https://arkansas-ya0x.onrender.com/"
   }


traffic = {
"downlink":"0",
"uplink":"0"}

traffico = 0

print(global_conf["host"])


stream_sites = ['youtube.com', 'xnxx.com', 'twitch.tv', 'dailymotion.com']



SECOND = 0


def getuser(username):
    try:
        user_info = CONFIG[username]
        return user_info
    except:
        return None

def createuser(username):
    CONFIG[username] = {"username":"","password":"","proxy":"","zips":"99","calidad":"None","automatic":"off","server":"1547","mode":"moodle"}
	
	
def deleteuser(username):
    
    if username in CONFIG:
        del CONFIG[username]
        print(f"Usuario {username} eliminado de la configuración.")
    else:
        print(f"El usuario {username} no existe en la configuración.")


	
@bot.on_message()
async def new_event(client: Client, message: Message):
    global traffico
    await bot.set_bot_commands([
    BotCommand("start","Inicia el Bot"),
    BotCommand("help","Muestra ayuda básica"),
    BotCommand("config","Configurar el host y el token"),
    BotCommand("zips","Tamaño de las partes a subir"),
    BotCommand("calidad","Establecer calidad"),
    BotCommand("auto","subidas en automáticas"),
    BotCommand("ls","Listar archivos en bot"),
    BotCommand("del_all","Borrar todos los archivos"),
    BotCommand("status","Muestra el estado del server"),    BotCommand("add_user","Añadir usuario al bot"),
    BotCommand("ban_user","Quitar usuario del bot")])
  
    msg = message.text
    id = message.from_user.id
    username = message.from_user.username
    @bot.on_callback_query(filters.regex(r"^/download"))
    async def download_callback(client, query):
        url = url_temp["Actual_url"]  # Obtén la URL almacenada en el diccionario
    # Llama a la función download_file() con los parámetros necesarios
        await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
        await query.answer("Descargando archivo...")
    if msg is None:
        msg = ""
    
    if getuser(username):
        if exists(str(id)):
            pass
        else:
            mkdir(str(id))
        pass
    else:
        if username in admins:
            createuser(username)
        else:
            await bot.send_message(id,f"❌@{username} 𝕍𝔸𝕃𝕃𝔸𝕊𝔼 ℕ𝕆 𝕋𝕀𝔼ℕ𝔼𝕊 𝔸ℂℂ𝔼𝕊𝕆❌")
            return
    if "/start" in msg:
        await message.reply(f"👋ℍ𝕠𝕝𝕒 😄 @{username} 𝕥𝕖 𝕖𝕤𝕥𝕒𝕧𝕒 𝕖𝕤𝕡𝕖𝕣𝕒𝕟𝕕𝕠. 𝕋𝕖𝕟𝕘𝕠 𝕝𝕒 𝕔𝕒𝕡𝕒𝕔𝕚𝕕𝕒𝕕 𝕕𝕖 ⬆️ 𝕒 𝕝𝕒 ☁️ 𝔼𝕤𝕥𝕖 𝕓𝕠𝕥 𝕖𝕤 𝕡𝕣𝕠𝕡𝕚𝕖𝕕𝕒𝕕 𝕕𝕖 @Music_botsupreme")
		
    elif "/calidad" in msg:
        calidad = msg.split(" ")[1]
        CONFIG[username]["calidad"] = calidad
        await bot.send_message(id, "𝕊𝕖 𝕒 𝕒𝕔𝕥𝕦𝕒𝕝𝕚𝕫𝕒𝕕𝕠 𝕝𝕒 𝕔𝕒𝕝𝕚𝕕𝕒𝕕 𝕖𝕤𝕡𝕖𝕣𝕠 𝕤𝕖𝕒 𝕝𝕒 𝕔𝕠𝕣𝕣𝕖𝕔𝕥𝕒✅")
	    
    elif "/zips" in msg:
        zips = msg.split(" ")[1]
        CONFIG[username]["zips"] = zips
        await bot.send_message(id,"📚𝕋𝕒𝕞𝕒ñ𝕠 𝕕𝕖 𝕝𝕠𝕤 𝕫𝕚𝕡𝕤 𝕘𝕦𝕒𝕣𝕕𝕒𝕕𝕠𝕤 𝕔𝕠𝕣𝕣𝕖𝕔𝕥𝕒𝕞𝕖𝕟𝕥𝕖 𝕠 𝕖𝕤𝕠 𝕔𝕣𝕖𝕠✅")
    	 
    elif "/add_user" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            createuser(usernames)  
            await bot.send_message(id, f"ℍ𝕒𝕤 𝕒𝕘𝕘 𝕒 𝕖𝕝 👤 @{usernames} 𝕒𝕝 𝔹𝕠𝕥 😁 𝕞𝕒𝕤 𝕝𝕖 𝕧𝕒𝕝𝕖 𝕕𝕚𝕤𝕗𝕣𝕦𝕥𝕒𝕣 𝕤𝕦 𝕖𝕤𝕥𝕒𝕟𝕔𝕚𝕒 👌")
        else:
           await bot.send_message(id, "‼️𝕊𝕆𝕃𝕆 ℙ𝔸ℝ𝔸 𝔸𝔻𝕄𝕀ℕ𝕊‼️")
           return

    elif "/ban_user" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            deleteuser(usernames)  
            await bot.send_message(id, f"ℍ𝕒𝕤 𝕙𝕖𝕔𝕙𝕒𝕕𝕠 @ {usernames} 𝕕𝕖𝕝 𝕓𝕠𝕥 𝕒 𝕓𝕒𝕤𝕖 𝕕𝕖 𝕡𝕒𝕥𝕒𝕕𝕒𝕤 𝕔𝕣𝕖𝕠 𝕢𝕦𝕖 𝕟𝕠 𝕣𝕖𝕘𝕣𝕖𝕤𝕒𝕣𝕒.🤣")
        else:
            await bot.send_message(id, "‼️𝕊𝕆𝕃𝕆 ℙ𝔸ℝ𝔸 𝔸𝔻𝕄𝕀ℕ𝕊‼️")
            return

    elif "/auto" in msg:
        try:
            if CONFIG[username]["automatic"] == "off":
                CONFIG[username]["automatic"] = "on"
                await bot.send_message(id, "✅𝕄𝕖 𝕙𝕒𝕤 𝕡𝕦𝕖𝕤𝕥𝕠 𝕖𝕟 𝕒𝕦𝕥𝕠𝕞𝕒𝕥𝕚𝕔𝕠✅")
            else:
                CONFIG[username]["automatic"] = "off"
                await bot.send_message(id, "😢❎𝕄𝕖 𝕙𝕒𝕤 𝕢𝕦𝕚𝕥𝕒𝕕𝕠 𝕕?? 𝕒𝕦𝕥𝕠𝕞𝕒𝕥𝕚𝕔𝕠❎")
        except Exception as e:
            await bot.send_message(id, f"‼️𝔼ℝℝ𝕆ℝ 𝔸𝕃 ℂ𝔸𝕄𝔹𝕀𝔸ℝ 𝔼𝕃 𝕄𝕆𝔻𝕆 𝔸𝕌𝕋𝕆𝕄𝔸𝕋𝕀ℂ𝕆‼️: {e}")			
			
    elif "/config" in msg:
        parts = msg.split(" ", 2)  
        if len(parts) == 3:
            _, host, token = parts  

        
            global_conf["host"] = host
            global_conf["token"] = token 

            await bot.send_message(id, f"✔️ℂ𝕆ℕ𝔽𝕀𝔾𝕌ℝ𝔸ℂ𝕀𝕆ℕ 𝔸𝕃𝕄𝔸ℂ𝔼ℕ𝔸𝔻𝔸 ℂ𝕆ℝℝ𝔼ℂ𝕋𝔸𝕄𝔼ℕ𝕋𝔼: \n 👌Host: {host}\n 💪Token: {token}")
        else:
            await bot.send_message(id, "💢𝔼ℝℝ𝕆ℝ 𝔸𝕃 𝔾𝕌𝔸ℝ𝔻𝔸ℝ 𝕃𝔸 ℂ𝕆ℕ𝔽𝕀𝔾𝕌ℝ𝔸ℂ𝕀𝕆ℕ, 𝔽𝕆ℝ𝕄𝔸𝕋𝕆 ✔️ℂ𝕆ℝℝ𝔼ℂ𝕋𝕆: /config host token")
						
    elif "/del_all" in msg:
        try:
            root_directory = os.path.join(str(id))  # Get the user's root directory
            if os.path.exists(root_directory):
                # Clear folder_indexes
                user_data[id]['folder_indexes'] = {} 
                
                for item in os.listdir(root_directory):
                    item_path = os.path.join(root_directory, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        import shutil
                        shutil.rmtree(item_path)
                await bot.send_message(id, "𝕋𝕆𝔻𝕆𝕊 𝔸ℝℂℍ𝕀𝕍𝕆𝕊 𝕐 ℂ𝔸ℝℙ𝔼𝕋𝔸𝕊 ℍ𝔸ℕ 𝕊𝕀𝔻𝕆 𝔼𝕃𝕀𝕄𝕀ℕ𝔸𝔻𝕆")
            else:
                await bot.send_message(id, f"𝕃𝔸 ℝ𝕌𝕋𝔸 {root_directory} ℕ𝕆 𝔼𝕏𝕀𝕊𝕋𝔼") 
        except Exception as e:
            await bot.send_message(id, f"𝔼ℝℝ𝕆ℝ 𝔸𝕃 𝔼𝕃𝕀𝕄𝕀ℕ𝔸ℝ: {e}")	
			
    elif "/help" in msg:
        msg = "ℙ𝕠𝕣𝕗𝕒𝕧𝕠𝕣 𝕝𝕖𝕖𝕣 𝕔𝕠𝕟 𝕒𝕥𝕖𝕟𝕔𝕚𝕠𝕟\n\n"
        msg += "𝔼𝕤𝕥𝕠𝕤 𝕤𝕠𝕟 𝕝𝕠𝕤 𝕡𝕒𝕤𝕠𝕤 𝕢𝕦𝕖 𝕕𝕖𝕧𝕖𝕤 𝕦𝕤𝕒𝕣\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /zips 99\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /calidad 480p\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /auto\n"
        msg += "ℂ𝕠𝕞𝕒𝕟𝕕𝕠 /config\n"
        msg += "𝔼𝕤 𝕖𝕟 𝕖𝕤𝕖 𝕠𝕣𝕕𝕖𝕟 𝕖𝕤𝕡𝕖𝕔𝕚𝕗𝕚𝕔𝕠 𝕔𝕦𝕒𝕝𝕢𝕦𝕚𝕖𝕣 𝕠𝕥𝕣𝕒 𝕕𝕦𝕕𝕒 𝕔𝕠𝕞𝕦𝕟𝕚𝕔𝕒𝕣𝕝𝕠 𝕖𝕟 𝕖𝕝 𝕘𝕣𝕦𝕡𝕠."
        await bot.send_message(id,msg)
		
    elif "/ls" in msg:
        count = 1  # Start index from 1
        msg = f"📔Tu directorio actual ⬇️\n"
    
        # Get the current directory from user data
        current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id))) 
    
        msg += f"📘Localización: {current_directory}\n\n"  
    
        if os.path.exists(current_directory):
            # Reset folder_indexes for the user
            user_data[id] = user_data.get(id, {})
            user_data[id]['folder_indexes'] = {}

            for item in os.listdir(current_directory):
                # Check if it's a file or a folder
                item_path = os.path.join(current_directory, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    size_str = sizeof_fmt(size)
                    msg += f"{count} 📄 {item} | {size_str}\n"
                    count += 1
                elif os.path.isdir(item_path):
                    msg += f"{count} 📁 {item}\n"
                    user_data[id]['folder_indexes'][count] = item  # Store index-name mapping
                    count += 1
            msg += "/ls Ver\n"
            msg += "/back Subir un nivel\n"
            msg += "/del_all Eliminar directorio raíz"
            await bot.send_message(id, msg)
        else:
            await bot.send_message(id, f"La ruta {current_directory} no existe.")		
		
    elif "/status" in msg:
        system_info = await get_system_info()        	
        cpu = system_info['cpu_percent']
        ram = system_info['ram_total']
        ram_used = system_info['ram_used']
        ram_percent = system_info['ram_percent']
        ram_free = system_info['ram_free']
        Disk = system_info['disk_total']
        Disk_used = system_info['disk_used']
        Disk_free = system_info['disk_free']
        downlink = traffic["downlink"]
        uplink = traffic["uplink"]
        traffics = sizeof_fmt(traffico)
        msg = "📊𝔻𝕒𝕥𝕠𝕤 𝕕𝕖𝕝 𝕤𝕚𝕤𝕥𝕖𝕞𝕒\n\n"
        msg += f"💻ℂℙ𝕌: {cpu}%\n"
        msg += f"💾ℝ𝕒𝕞: {ram}\n"
        msg += f"📉𝕌𝕤𝕠 𝕕𝕖 ℝ𝕒𝕞: {ram_used}\n"
        msg += f"💽ℝ𝕒𝕞 𝕕𝕚𝕤𝕡𝕠𝕟𝕚𝕓𝕝𝕖: {ram_free}\n"
        msg += f"📶ℙ𝕠𝕣𝕔𝕖𝕟𝕥𝕒??𝕖 ℝ𝕒𝕞: {ram_percent}%\n"
        msg += f"💿𝔻𝕚𝕤𝕔𝕠 𝕥𝕠𝕥𝕒𝕝: {Disk}\n"
        msg += f"📀𝔻𝕚𝕤𝕔𝕠 𝕌𝕤𝕒𝕕𝕠: {Disk_used}\n"
        msg += f"🗃️𝔻𝕚𝕤𝕔𝕠 𝕃𝕚𝕓𝕣𝕖: {Disk_free}\n"
        msg += "⚡️𝕋𝕣𝕒𝕗𝕚𝕔𝕠 𝕕𝕖 𝕝𝕒 𝕣𝕖𝕕\n\n"
        msg += f"⬇️𝔻𝕖𝕤𝕔𝕒𝕣𝕘𝕒: {downlink}/s\n"
        msg += f"⬆️𝕊𝕦𝕓𝕚𝕕𝕒: {uplink}/s\n\n"
        msg += f"𝕋𝕣𝕒𝕗𝕚𝕔𝕠 𝕥𝕠𝕥𝕒𝕝: {traffics}"
        await bot.send_message(id,msg)
		
		
                
import time
from time import localtime

SECOND = None  # Inicializa la variable global

def sizeof_fmt(size):
    """Convierte el tamaño a un formato legible."""
    if size is None:
        return "0 B"  # Manejo de None
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def porcent(index, max_value):
    """Calcula el porcentaje."""
    if max_value == 0:  # Para evitar división por cero
        return 0
    porcent = index / max_value
    porcent *= 100
    return round(porcent)

async def download_func(current, total, filename, starttime, msg):
    """Muestra el progreso de la descarga."""

    def text_progress(index, max_value):
        """Genera una representación visual del progreso."""
        try:
            if max_value < 0:
                max_value += 0
            porcent = index / max_value * 100
            porcent = round(porcent)
            make_text = '['
            for index_make in range(1, 15):
                make_text += '■' if porcent >= index_make * 5 else '□'
            make_text += ']'
            return make_text
        except Exception as ex:
            print(f"Error en text_progress: {ex}")
            return ''

    global SECOND
    try:
        speed = (current / (time.time() - starttime)) if starttime else 0  # Calcula la velocidad
        percentage = porcent(current, total)  # Llama a la función porcent

        message = "📥Download File.... \n"
        message += f"{text_progress(current, total)}, {percentage}%\n"
        message += f"📥 Download: {sizeof_fmt(current)}*\n"
        message += f"💾 Total: {sizeof_fmt(total)}\n"
        message += f"🏎️ Velocity: {sizeof_fmt(speed)}\n"

        current_second = localtime().tm_sec
        
        # Actualiza el mensaje solo si ha cambiado el segundo
        if SECOND is None or current_second != SECOND:
            try:
                await msg.edit(message)
            except Exception as ex:
                print(f"Error al actualizar el mensaje: {ex}")
        
        SECOND = current_second

    except Exception as ex:
        print(f"Error en download_func: {ex}")

	
	
def upload_func(current,total,starttime,filename,msg):
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0  
    percentage = int((current / total) * 100)

    message = "⬇️ Subiendo*\n"
    message += f"{text_progress(current, total)}, {percentage}%\n"
    message += f"⬇️ *Subido: {sizeof_fmt(current)}\n"
    message += f"🗂 Total: {sizeof_fmt(total)}\n"
    message += f"🚀 Velocidad: {sizeof_fmt(speed)}\n"
    message += f"⏳ Porcentaje: {percentage}%\n"
    traffic["uplink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec


class UploadProgress(BufferedReader):
    def __init__(self,file,callback):
        f = open(file, "rb")
        self.filename = file.split("/")[-1]
        self.__read_callback = callback
        super().__init__(raw=f)
        self.start = time.time()
        self.length = os.path.getsize(file)
    
    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(UploadProgress, self).read(size)
        
async def uploadfile(file, msg, username):
    global global_conf
    original_filename = os.path.basename(file)  # Obtiene el nombre de archivo de la ruta original
    fsize = Path(file).stat().st_size
    zips_size = 1024 * 1024 * int(CONFIG[username]["zips"])


    path = [file]
    if fsize > zips_size:
        await msg.edit("📚Comprimiendo...")
        path = sevenzip(file, volume=zips_size)

    try:
        if CONFIG[username]["proxy"] == "":
            connector_on = aiohttp.TCPConnector()
        else:
            connector_on = aiohttp_socks.ProxyConnector.from_url(CONFIG[username]["proxy"])
        async with aiohttp.ClientSession(connector=connector_on) as session:
            token = global_conf["token"]
            
            urls = []
            if token:
                for fpath in path:
                    await msg.edit(f"⬆️Subiendo...")
                    file = UploadProgress(
                        fpath,
                        lambda current, total, start, filename: upload_func(
                            current, total, start, filename, msg
                        ),
                    )
                    upload = await uploadtoken(file, token, session)
                    if upload:
                        url = upload
                        await msg.edit(
                            "✅Subida completada. Procediendo a convertir el link a perfil..."
                        )

                        if url:
                            url = url.replace("draftfile.php/", "webservice/draftfile.php/")
                            url = url + "?token=" + token
                            urls.append(url)
                            await msg.edit(f"✅Subida exitosa✅")
                            

                # Mover la lógica de escritura del archivo fuera del bucle for
                print(urls)
                if urls:
                    with open(f"{original_filename}.txt", "w") as txt:  # Usa original_filename
                        txt.write("\n".join(urls))
                    await bot.send_document(username, f"{original_filename}.txt")
                    os.remove(f"{original_filename}.txt")
                    
                else:
                    await msg.edit(f"❌ No se pudo subir ningún archivo.")
            else:
                await bot.send_message(
                    username,
                    "‼️No se completo el inicio de seccion posibles razones: web caida , token incorrecto, token baneado‼️",
                )
                return
    except Exception as ex:
        traceback.print_exc()
        await bot.send_message(username, f"{ex}")


async def uploadtoken(f, token, session):
    try:
        # Declara global_conf como global
        global global_conf

        # Obtén el host desde el diccionario
        host = global_conf["host"]
        
        

        url = f"{host}webservice/upload.php"
        query = {"token": token, "file": f}
        async with session.post(url, data=query, ssl=True) as response:
            text = await response.text()
            print(text)
            dat = loads(text)[0]
            url = f"{host}draftfile.php/{str(dat['contextid'])}/user/draft/{str(dat['itemid'])}/{str(quote(dat['filename']))}"
            return url
    except:
        traceback.print_exc()
        return None

import yt_dlp
import aiohttp
import time

def download_progres(data,message,format, username):
    global CONFIG
    quality = CONFIG[username]["calidad"]
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _total_bytes_str = data["_total_bytes_estimate_str"]        
        _speed_str = data["_speed_str"].replace(" ","")
        _eta_str = data["_eta_str"]
        _format_str = format        
        msg= f"{filename}\n"
        msg+= f"💾Descargado: {_downloaded_bytes_str}\n"
        msg+= f"📦Total: {_total_bytes_str} \n"
        msg+= f"⚡️Velocidad: {_speed_str}/s \n"
        msg+= f"🎥Calidad: {quality}\n"
        msg+= f"⏰Tiempo restante: {_eta_str}"
        traffic["downlink"] = _speed_str
        global SECOND 
        if SECOND != localtime().tm_sec:
        #if int(localtime().tm_sec) % 2 == 0 :
            try:
                message.edit(msg,reply_markup=message.reply_markup)
            except:
                pass
        SECOND = localtime().tm_sec

		
async def delcloud(filename, msg, username):
        base_url = "https://arkansas-ya0x.onrender.com/"  # Reemplaza con tu URL Nextcloud válida
        nextcloud_client = NextcloudClient(base_url)
        v = "1547"
        type = "uo"
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit("Borrando........")		
        result = nextcloud_client.delete_nexc(url = f'{base_url}remote.php/webdav/?dir=/{filename}', cookies=data)
        await msg.edit(f"{result}")
        return
		
		
		
async def upx(filename, msg, username):
        global server_s
        base_url = "https://arkansas-ya0x.onrender.com/"  # Reemplaza con tu URL Nextcloud válida
        nextcloud_client = NextcloudClient(base_url)
        type = "uo"
        v = CONFIG[username]["server"]
        print(v)
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit(data)		
        result = await nextcloud_client.upload_file(filename, data)
        if "https://arkansas-ya0x.onrender.com/" in result:
            await msg.edit(f"✅Subida correcta✅:\n {result}")
        else:
            await msg.edit("‼️Error al subir‼️")
		
        return
			     
def generate():
    prefix = "web-file-upload-"
    random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    unique_id = str(uuid.uuid4().time_low)

    random_name = f"{prefix}{random_string}-{unique_id}"
    return random_name

	

async def file_renamer(file):
    filename = file.split("/")[-1]
    path = file.split(filename)[0]
    if len(filename)>21:
        p = filename[:10]
        f = filename[-11:]
        filex = p + f
    else:
         filex = filename
    filename = path + re.sub(r'[^A-Za-z0-9.]', '', filex)
    os.rename(file,filename)
    return filename
	

				 
		
async def ytdlp_downloader(url, id, msg, username, callback, format):
    """Descarga un video de YouTube utilizando yt-dlp."""

    class YT_DLP_LOGGER(object):
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass

    resolution = str(format)
    dlp = {
        "logger": YT_DLP_LOGGER(),
        "progress_hooks":[callback],
        "outtmpl": f"{id}/%(title)s.%(ext)s",
        "format": f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"  # Prioritize height first
    }

    downloader = yt_dlp.YoutubeDL(dlp)
    print("Se esta descargando mamawebo")
    loop = asyncio.get_running_loop()

    # Obtén información sobre el video
    filedata = await loop.run_in_executor(None, downloader.extract_info, url)

    # Verifica si la descarga está dividida
    if "entries" in filedata:
        # Descarga dividida
        total_size = 0
        for entry in filedata["entries"]:
            total_size += entry["filesize"]
    else:
        # Descarga completa
        if "filesize" in filedata:
            total_size = filedata["filesize"]
        else:
            # No se puede obtener el tamaño total
            total_size = 0

    # ... (tu código para el progreso de la descarga)
    filepath = downloader.prepare_filename(filedata)
    filename = filedata["requested_downloads"][0]["_filename"]
    return filename

def obtener_ip_publica():
  """Obtiene la IP pública usando la API de icanhazip.com."""
  try:
    response = requests.get("https://icanhazip.com/")
    return response.text.strip()
  except requests.exceptions.RequestException as e:
    print(f"Error al obtener la IP: {e}")
    return None	
	
	
	
	

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]	
	

import asyncio
import aiohttp
import certifi
import ssl	


async def download_file(url, id, msg, callback=None):
    global traffico
    """Downloads a file from MediaFire and saves it to a specified path."""

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the ssl parameter with the context object
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    ) as session:
        response = await session.get(url)

        response = await session.get(url)
        filename = url.split("/")[-1]

        # Save to {id}/{filename} 
        path = f"{id}/{filename}"
        f = open(path, "wb")

        chunk_ = 0
        total = int(response.headers.get("Content-Length"))
        traffico += total
        start = time.time()  # Llama a la función time.time() para obtener el tiempo actual
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            chunk_ += len(chunk)
            if callback:
                await callback(chunk_, total, filename, start, msg)
            f.write(chunk)
            f.flush()

        return path

@Client.on_callback_query(filters.regex(r"^download_"))  # Filtra por el prefijo "download_"
async def download_callback(client, query):
    global url_temp
    url = url_temp["Actual_url"]
    await download_file(url, id, query.message, callback=download_func)
    await query.answer("Descargando archivo...")		
		
		


	
async def download_mediafire(url, id, msg, callback=None):
    """Downloads a file from MediaFire and saves it to a specified path."""
    global traffico

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the `ssl` parameter with the context object
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    )
    
    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename

    # Save to {id}/{filename} 
    path = f"{id}/{filename}"
    f = open(path, "wb")

    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    traffico += total
    start = time.time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_ += len(chunk)
        if callback:
            await callback(chunk_, total, filename, start, msg)
        f.write(chunk)
        f.flush()

    return path

	
        
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

async def get_cpu_percent():
    """Obtiene el porcentaje de uso de la CPU en un hilo separado."""
    loop = asyncio.get_event_loop()
    cpu_percent = await loop.run_in_executor(executor, psutil.cpu_percent)  # No se necesita el argumento 'interval'
    return cpu_percent

import asyncio
import psutil
import os
import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()
	
	
	
	
async def get_system_info():
    """Obtiene información del sistema y la devuelve como un diccionario."""
    
    info = {}

    # Memoria RAM
    ram = psutil.virtual_memory()
    info["ram_total"] = sizeof_fmt(ram.total)
    info["ram_used"] = sizeof_fmt(ram.used)
    info["ram_free"] = sizeof_fmt(ram.free)
    info["ram_percent"] = ram.percent

    # CPU
    info["cpu_percent"] = await get_cpu_percent()

    # Almacenamiento del disco
    disk = psutil.disk_usage('/')  # Obtener información del disco raíz ('/')
    info["disk_total"] = sizeof_fmt(disk.total)  # Convertir a GB
    info["disk_used"] = sizeof_fmt(disk.used)  # Convertir a GB
    info["disk_free"] = sizeof_fmt(disk.free)  # Convertir a GB
    info["disk_percent"] = disk.percent

    return info
   
	
	
	
	
	
def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)
	
	
import threading
import http.server
import socketserver
# Asegúrate de importar tu módulo bot

# Función para ejecutar el servidor web
def run_server():
    PORT = 4500
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Función para ejecutar el bot
def run_bot():
    bot.run()  # Suponiendo que 'run()' es la función que inicia tu bot

if __name__ == "__main__":
    # Inicia el servidor web en un hilo separado
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Ejecuta el bot en el hilo principal
    run_bot()  