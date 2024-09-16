from server import keep_alive

# Start the web server to keep the bot alive
keep_alive()

# Your bot logic here
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# List of allowed user IDs
ALLOWED_USER_IDS = [2032347579,1445924971]  # Replace these with actual user IDs

def secure_command(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ALLOWED_USER_IDS:
            await update.message.reply_text("𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭 𝐃𝐌 𝐌𝐘 𝐎𝐖𝐍𝐄𝐑 👉🏻@𝐅𝐍𝐂_𝐎𝐦𝐊𝐚𝐑 ")
            return
        await func(update, context)
    return wrapper

@secure_command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("𝐒𝐞𝐧𝐝 𝐦𝐞 𝐚 𝐭𝐞𝐱𝐭 𝐟𝐢𝐥𝐞📂")

@secure_command
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the document file
    document = update.message.document
    file = await document.get_file()
    
    # Download the file
    input_file_path = f"./{document.file_name}"
    await file.download_to_drive(input_file_path)

    # Process the file
    await update.message.reply_text("𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐟𝐢𝐥𝐞...𝐰𝐚𝐢𝐭 𝐒𝐈𝐑😈")
    
    # Specify the word after which to cut the URL
    cut_after_word = context.user_data.get('cut_after_word', 'auth=')  # Default word
    replacement_word = context.user_data.get('replacement_word', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjYwNjY1MDYsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiYjJoME5XcHlXa1ptUWtaYU4wUkVNbXRXUTFCV1p6MDkiLCJmaXJzdF9uYW1lIjoiTHpsSlkyUldRWHBYVEhjd1dWcFhZbUZLTjB3MVVUMDkiLCJlbWFpbCI6IlpESkRTVzFDUkZoVlIwb3dMekY1YkhSUWFFTkZhRWRtVWtJM1lYYzNZVTg0UkdrMU1UZFVTRzV6TkQwPSIsInBob25lIjoiUWxGQ1VURTVZVlYxVjFaWE9XZDNUalpFUzBwNVp6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJSSGRFZDBGVVUxUmljbkJrVFVkbk1XUjRWRkJRZHowOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoidXBwZXIgdGhhbiAzMSIsImRldmljZV9tb2RlbCI6IlhpYW9NaSBNMjAwN0oxN0MiLCJyZW1vdGVfYWRkciI6IjQ0LjIyMy45My4xNzIifX0.Pc87bmMz8Pm1Z1FtFqzrABbi8DsMCOy5tB_K8g1a7tO1yr3J8_8TDrFrNMaFLzXMorAoOB4xmsjOIzTkkdinzXzb8-gD-PrLkGyi5gzjO_mF-Bqjhxbvkk-274VXsGHdE15Idc7EtOvYgUr-1PAV-ceLF14PLYipGUcQaFayUEczDyPr8HkhL3QNHZyBbQRIPTt2dzOioN09xXze5tkRxR1UtIRrvmNvI5oa-FR5IWqp_S-BI_JypNvgXuZYcrzxE84IGDYufsx5QKRScQzWh4wclEOTMPd3Jfit2WUkf1VbiokWtrI33Hr7Jkr0cV0QmH9EFk-fyTxmmc7OHypetw')  # Default replacement word

    # Open the input text file and read lines with UTF-8 encoding
    with open(input_file_path, 'r', encoding='utf-8') as f:
        urls = f.readlines()

    # Process each URL
    updated_urls = []
    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        if cut_after_word in url:
            # Cut the URL at the specified word and replace the rest
            index = url.index(cut_after_word) + len(cut_after_word)
            new_url = url[:index] + replacement_word  # Keep the part before and add the replacement
            updated_urls.append(new_url + '\n')
        else:
            updated_urls.append(url + '\n')  # If the word is not found, keep the original URL

    # Write the updated URLs back to the same input file
    with open(input_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_urls)

    # Send back the processed file
    with open(input_file_path, 'rb') as f:
        await update.message.reply_document(InputFile(f, filename=document.file_name))

@secure_command
async def set_cut_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['cut_after_word'] = context.args[0] if context.args else 'auth='
    await update.message.reply_text(f"Set the word to cut after: {context.user_data['cut_after_word']}")

@secure_command
async def set_replacement_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['replacement_word'] = context.args[0] if context.args else 'new_value'
    await update.message.reply_text(f"Set the replacement word: {context.user_data['replacement_word']}")

if __name__ == '__main__':
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    app = ApplicationBuilder().token('7504169790:AAGzS8YTC9BCTfIRRtEU-ray7pEqndrlw5s').build()

    # Add command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('set_cut_word', set_cut_word))
    app.add_handler(CommandHandler('set_replacement_word', set_replacement_word))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    app.run_polling()
