from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def main_menu():

    keyboard = [
        [
            InlineKeyboardButton("🎥 YouTube e Instagram", callback_data="menu_social_network_extraction"),
        ],
        [
            InlineKeyboardButton("🔊 Extrair Áudio", callback_data="menu_extract_audio"),
        ],
        [
            InlineKeyboardButton("🎧 Converter Áudio", callback_data="menu_audio_convert"),
            InlineKeyboardButton("🎬 Converter Vídeo", callback_data="menu_video_convert"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# Criando o menu para o download das mídias
async def type_quality_menu(message, medias):

    keyboard = []
    board = []
    aux = 0

    for media in medias:

        board.append(InlineKeyboardButton(f"🎞️ {media['type']} - {media['quality']}", callback_data=f"extract-{media['formatId']}"))
        
        aux = aux + 1

        if aux % 2 == 0 :

            keyboard.append(board)
            board = []

    if aux % 2 != 0 :

        keyboard.append(board)

    markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("👉 Escolha a qualidade:", reply_markup=markup)

# Criando menu para conversão de áudios
async def audio_convert_menu(message, context: ContextTypes.DEFAULT_TYPE):
    keyboard= [
        [InlineKeyboardButton("MP3 🎧", callback_data ="convert_audio-mp3"),
         InlineKeyboardButton("WAV 🎵", callback_data ="convert_audio-wav")],

        [InlineKeyboardButton("AAC 🎶", callback_data ="convert_audio-aac"),
         InlineKeyboardButton("FLAC 💽", callback_data ="convert_audio-flac")],


        [InlineKeyboardButton("AMR 📱", callback_data ="convert_audio-amr"),
         InlineKeyboardButton("M4A 🎙️", callback_data ="convert_audio-m4a")],

        [InlineKeyboardButton("OGG 🟠", callback_data ="convert_audio-ogg"), # Formato Studio apps music
         InlineKeyboardButton("WMA 🪟", callback_data ="convert_audio-wma")] # Formato Windowszin

        [InlineKeyboardButton("AIFF 🎼", callback_data ="convert_audio-aiff")], # Formato Apple

    ]

    markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("🎧 Escolha o formato de áudio para conversão:", reply_markup=markup)

async def video_convert_menu(message, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("MKV 🎞️", callback_data="convert_video-mkv"),
        InlineKeyboardButton("FLV 📺", callback_data="convert_video-flv")],

        [InlineKeyboardButton("MOV 🎬", callback_data="convert_video-mov"),
        InlineKeyboardButton("AVI 🎥", callback_data="convert_video-avi")],

        [InlineKeyboardButton("WEBM 🌐", callback_data="convert_video-webm"),
        InlineKeyboardButton("WMV 🪟", callback_data="convert_video-wmv")],

        [InlineKeyboardButton("OGV 🟠", callback_data="convert_video-ogv"),
        InlineKeyboardButton("3GP 📱", callback_data="convert_video-3gp")],

        [InlineKeyboardButton("MP4 🎞️", callback_data="convert_video-mp4")]
    ]

    markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("🎬 Escolha o formato de vídeo para conversão:", reply_markup=markup)