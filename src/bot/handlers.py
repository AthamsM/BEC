import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from .menus import main_menu
from src.services.social_network_extraction import social_network_extraction
from src.services import extract_audio
from src.services.audio_converter import audio_receive, audio_convert

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

    if data == "menu_social_network_extraction":
        
        await query.edit_message_text("🎥 Envie um link do YouTube ou do Instagram para extrair o áudio ou o vídeo.")
        
        # Setando a operação que o usuário quer fazer
        context.user_data["operation"] = "social_network_extraction"

    elif data == "menu_extract_audio":
        
        await query.edit_message_text("🔊 Envie um vídeo e eu extraio o áudio pra você.")
        
        context.user_data["operation"] = "extract_audio"

    elif data == "menu_audio_convert":
        
        await query.edit_message_text("🎧 Envie um arquivo de áudio e escolha o formato de saída.")

        context.user_data["operation"] = "audio_converter"

    elif data == "menu_video_convert":
        
        await query.edit_message_text("🎬 Envie um vídeo e escolha o formato de saída.")

    # Olhando se o usuário escolheu alguma opção de mídia para baixar
    elif data.startswith("extract-"):

        # Pegando o id da mídia que o usuário escolheu para baixar
        choice = int(data.split("-", 1)[1])

        # Recuperando a filtered_media
        filtered_media = context.user_data.get("filtered_media", [])

        # Retornando o download da mídia selecionada para o usuário
        for fm in filtered_media :

            if int(fm["formatId"]) == choice :
                
                await query.message.reply_text(f"👉 Você escolheu: {fm['type']} - {fm['quality']}")
                await query.message.reply_text(f"👉 Link: {fm['url']}")
                return
        
        await query.message.reply_text("❌ Mídia não encontrada")
    
    # Olhando qual das opções de conversão o usuário escolheu para prosseguir na conversão de áudio
    elif data.startswith("convert_audio"):
        await audio_convert(update, context)

    else:
        await query.edit_message_text("❌ Opção desconhecida.")

# Callback para mensagens
async def message_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    # Pegando a operação que o usuário quer fazer
    data = context.user_data.get("operation")
    logger.info(f"Message calback é {data}")

    if data == "social_network_extraction" :

        # Chamando a função que vai fazer a extração
        await social_network_extraction(update, context)
        
    elif data == "extract_audio":
        
        await extract_audio.handle(update, context)
    
    elif data == "audio_converter":

        await audio_receive(update, context)
    
    else :

        await message.reply_text("❌ Mensagem Inválida")
