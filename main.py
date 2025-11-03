import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Importa o TOKEN e os handlers
from src.config.settings import TOKEN
from src.bot.handlers import start, menu_callback, message_callback

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    # Verifica se o TOKEN foi carregado
    if not TOKEN:
        logging.critical("Token do Telegram não encontrado! Verifique seu .env e settings.py.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers principais
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND, message_callback))

    # TODO: Adicionar handlers para receber mensagens (links, arquivos)
    # Ex: app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
