from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

# Criando menu para o download das mídias
async def type_quality_menu(message, medias):

    keyboard = []

    for media in medias:

        keyboard.append([InlineKeyboardButton(f"🎞️ {media['type']} - {media['quality']}", callback_data=f"extract-{media['formatId']}")])

    markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("👉 Escolha a qualidade:", reply_markup=markup)