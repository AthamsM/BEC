from telegram import Update
from telegram.ext import ContextTypes
from src.config.settings import SOCIAL_DOWNLOAD_API_TOKEN
from src.bot.menus import type_quality_menu as tqm
import httpx

async def social_network_extraction(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try :

        # Link da api
        api_endpoint = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"

        # Pegando o link que o usuário mandar
        message = update.message
        link = message.text

        # Criando o header
        header = {
            "x-rapidapi-key": SOCIAL_DOWNLOAD_API_TOKEN,
            "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        try :

            # Fazendo a requisição para a api do rapidapi
            async with httpx.AsyncClient() as client :

                response = await client.post(api_endpoint, json = {"url": link}, headers = header)
                data = response.json()

            # Pegando as mídias do json
            medias = data["medias"]

            # Filtrando os campos das mídias
            filtered_media = []
            for media in medias :

                filtered_media.append({
                    "formatId": media.get("formatId") or media.get("id"),
                    "label": media.get("label"),
                    "type": media.get("type"),
                    "ext": media.get("ext"),
                    "quality": media.get("quality"),
                    "url": media.get("url")
                })

            # Salvando a filtered_media
            context.user_data["filtered_media"] = filtered_media

            # Chamando o menu type_quality_menu
            await tqm(message, filtered_media)

        except ValueError:

            await message.reply_text("❌ Envie um link válido")
            return

    except KeyError:

        await message.reply_text("❌ Erro ao tentar enviar o link")
        return