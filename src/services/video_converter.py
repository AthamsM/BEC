from telegram import Update
from telegram.ext import ContextTypes
from src.config.settings import FREECONVERT_API_KEY
import requests, os, time, httpx, asyncio, json

async def video_receive (update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        
        video = update.message.video

        file = await video.get_file()
        file_name = f"{update.effective_user.id}_input.{file.file_path.split('.')[-1]}"

        await file.download_to_drive(file_name)

        context.user_data["video_file"] = file_name

        # Chamada do menu de opções de conversão somente agora
        from src.bot.menus import video_convert_menu
        await video_convert_menu(update.message, context)

    except KeyError:
        
        await update.message.reply_text("❌ Erro nenhum arquivo de áudio detectado.")
        return

async def video_convert (update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        query = update.callback_query
        await query.answer()

        file_name = context.user_data.get("video_file")

        output_format = query.data.replace("convert_video-", "")
        await query.edit_message_text(f"⏳ Convertendo para {output_format}...")

        try:

            converted_file = await call_video_convert_api(file_name, output_format)
            await query.message.reply_document(open(converted_file, "rb"))

            os.remove(file_name)
            os.remove(converted_file)
            del context.user_data["video_file"]

            await query.message.reply_text("✅ Conversão concluída!")

        except Exception as e:

            await query.message.reply_text(f"❌ Erro ao converter: {str(e)}")
            return

    except KeyError:
        
        await update.message.reply_text("⚠️ Nenhum video encontrado. Envie novamente.")
        return

async def call_video_convert_api (input_file, output_format):

    url = "https://api.freeconvert.com/v1/process/jobs"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {FREECONVERT_API_KEY}"
    }

    # Definindo o job com tarefas de importação, conversão e exportação
    input_body = {
        "tasks": {
            "import-1": {
                "operation": "import/upload"
            },
            "convert-1": {
                "operation": "convert",
                "input": "import-1",
                "output_format": output_format
            },
            "export-1": {
                "operation": "export/url",
                "input": "convert-1"
            }
        }
    }

    async with httpx.AsyncClient() as client:
            # Criar job
            job = await client.post(url, data=json.dumps(input_body), headers=headers)
            
            if job.status_code >= 400:
                raise Exception(f"Falha ao criar job: {job.text}")

            job_data = job.json()
            
            # tasks vêm como lista — precisamos buscar pelo name "import-1"
            import_task = next(task for task in job_data["tasks"] if task["name"] == "import-1")
            upload_url = import_task["result"]["form"]["url"]
            upload_params = import_task["result"]["form"]["parameters"]


            # Upload do arquivo
            with open(input_file, "rb") as f:
                files = {"file": f}
                await client.post(upload_url, data=upload_params, files=files)

            # Polling até terminar conversão
            while True:
                check = await client.get(f"{url}/{job_data['id']}", headers=headers)
                status = check.json()

                if status.get("status") == "completed":
                    break
                if status.get("status") == "failed":
                    raise Exception("Conversão falhou.")

                await asyncio.sleep(2)

            # Link para download vindo do export
            export_task = next(task for task in status["tasks"] if task["name"] == "export-1")
            file_url = export_task["result"]["url"]


            # Download
            file_data = await client.get(file_url)
            output_file = f"converted.{output_format}"

            with open(output_file, "wb") as f:
                f.write(file_data.content)

            return output_file