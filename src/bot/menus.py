from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🎥 YouTube", callback_data="menu_youtube"),
            InlineKeyboardButton("📸 Instagram", callback_data="menu_instagram"),
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
