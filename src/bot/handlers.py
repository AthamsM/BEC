import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from .menus import main_menu

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Mostra o menu principal."""
    await update.message.reply_text(
        "🎵 Bem-vindo ao BEC!\nEscolha o que deseja fazer:",
        reply_markup=main_menu()
    )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com os botões do menu."""
    query = update.callback_query
    await query.answer()  # evita 'loading...' infinito no Telegram
    data = query.data

    if data == "menu_youtube":
        await query.edit_message_text("🎥 Envie um link do YouTube para converter áudio ou vídeo.")
        # Aqui depois chama o service: youtube_service.handle(update, context) Se vira pra entender ai

    elif data == "menu_instagram":
        await query.edit_message_text("📸 Envie um link do Instagram para converter mídia.")

    elif data == "menu_extract_audio":
        await query.edit_message_text("🔊 Envie um vídeo e eu extraio o áudio pra você.")

    elif data == "menu_audio_convert":
        await query.edit_message_text("🎧 Envie um arquivo de áudio e escolha o formato de saída.")

    elif data == "menu_video_convert":
        await query.edit_message_text("🎬 Envie um vídeo e escolha o formato de saída.")

    else:
        await query.edit_message_text("❌ Opção desconhecida.")
