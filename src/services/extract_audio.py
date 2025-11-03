import os
import base64
import tempfile
import logging
from moviepy.editor import VideoFileClip
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

TEMP_DIR = os.path.join(tempfile.gettempdir(), "bec_audio_extractor")
os.makedirs(TEMP_DIR, exist_ok=True)


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe um vídeo do Telegram, extrai o áudio e envia o MP3 de volta."""

    message = update.message
    logger.info("📩 Recebendo mensagem...")

    file = None
    if message.video:
        logger.info("🎥 Vídeo detectado.")
        file = await message.video.get_file()
    elif message.document and message.document.mime_type.startswith("video/"):
        logger.info("📄 Documento de vídeo detectado.")
        file = await message.document.get_file()
    else:
        await message.reply_text("❌ Envie um vídeo para extrair o áudio.")
        logger.warning("Mensagem recebida não contém vídeo.")
        return

    # Caminhos temporários
    video_filename = f"{file.file_id}.mp4"
    video_path = os.path.join(TEMP_DIR, video_filename)
    audio_filename = f"{file.file_id}.mp3"
    audio_path = os.path.join(TEMP_DIR, audio_filename)

    logger.info(f"⬇️ Baixando vídeo para {video_path}")
    await file.download_to_drive(video_path)
    logger.info("✅ Download concluído")

    try:
        logger.info("🎞️ Abrindo vídeo com MoviePy...")
        clip = VideoFileClip(video_path)
        logger.info("🎧 Extraindo áudio...")
        clip.audio.write_audiofile(audio_path, codec="mp3", verbose=False, logger=None)
        clip.close()
        logger.info(f"✅ Áudio extraído em: {audio_path}")

        await message.reply_audio(audio=open(audio_path, "rb"), caption="✅ Áudio extraído com sucesso!")
        logger.info("📤 Áudio enviado para o usuário.")

        # Base64 opcional
        with open(audio_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        logger.debug(f"Tamanho base64: {len(audio_b64)} bytes")

    except Exception as e:
        logger.exception("❌ Erro ao extrair áudio:")
        await message.reply_text(f"❌ Erro ao extrair o áudio: {e}")

    finally:
        # Limpeza
        if os.path.exists(video_path):
            os.remove(video_path)
            logger.info(f"🧹 Removido {video_path}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"🧹 Removido {audio_path}")
