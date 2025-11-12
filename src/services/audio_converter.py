from telegram import Update
from telegram.ext import ContextTypes
from src.config.settings import FREECONVERT_API_KEY
import requests, os, time, httpx, asyncio, json



# Recebe o arquivo e o armazena
async def audio_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        # Busca o arquivo de áudio enviado pelo usuário (seja um áudio pelo telegram ou vindo de outra
        # unidade de armazenamento)
        audio = update.message.audio or update.message.voice

        file = await audio.get_file()
        file_name = f"{update.effective_user.id}_input.{file.file_path.split('.')[-1]}"

        await file.download_to_drive(file_name)

        context.user_data["audio_file"] = file_name

        # Chamada do menu de opções de conversão somente agora
        from src.bot.menus import audio_convert_menu
        await audio_convert_menu(update.message, context)
    
    except KeyError:
        await update.message.reply_text("❌ Erro nenhum arquivo de áudio detectado.")
        return

# Conversão - Callback do menu
async def audio_convert(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        query = update.callback_query
        await query.answer()

        file_name = context.user_data.get("audio_file")

        output_format = query.data.replace("convert_audio-", "")
        await query.edit_message_text(f"⏳ Convertendo para {output_format}...")

        try:
            converted_file = await call_audio_convert_api(file_name, output_format)
            await query.message.reply_document(open(converted_file, "rb"))

            # Fazendo a limpeza (Garbage my friend)
            os.remove(file_name)
            os.remove(converted_file)
            del context.user_data["audio_file"]

            await query.message.reply_text("✅ Conversão concluída!")
        
        except Exception as e:
            import traceback
            print("❌ ERRO NA CONVERSÃO:")
            print(traceback.format_exc())

            await query.message.reply_text(f"❌ Erro ao converter: {str(e)}")
            return


    except KeyError:
        await update.message.reply_text("⚠️ Nenhum áudio encontrado. Envie novamente.")
        return


# Conversão - adequação de funcionamento para estruturação via API
async def call_audio_convert_api(input_file, output_format):

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
