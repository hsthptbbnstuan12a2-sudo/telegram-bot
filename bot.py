from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator
from pypinyin import pinyin, Style

# Hàm dịch văn bản
def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

# Hàm xử lý tin nhắn
def handle_message(update: Update, context: CallbackContext):
    message = update.message.text
    language = "zh" if any("\u4e00" <= char <= "\u9fff" for char in message) else "vi"
    
    if language == "zh":  # Tiếng Trung, dịch sang tiếng Việt
        translated_text = translate_text(message, "zh-CN", "vi")
        update.message.reply_text(translated_text)
    else:  # Tiếng Việt, dịch sang tiếng Trung
        translated_text = translate_text(message, "vi", "zh-CN")
        update.message.reply_text(translated_text)

# Hàm hiển thị Pinyin
def show_pinyin(update: Update, context: CallbackContext):
    message = update.message.text
    if any("\u4e00" <= char <= "\u9fff" for char in message):  # Kiểm tra xem có phải chữ Hán không
        pinyin_text = " ".join([word[0] for word in pinyin(message, style=Style.TONE3)])
        update.message.reply_text(f"Pinyin: {pinyin_text}")
    else:
        update.message.reply_text("Vui lòng gửi một tin nhắn bằng tiếng Trung để hiển thị Pinyin.")

# Hàm bắt đầu
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Chào mừng bạn đến với Bot dịch và Pinyin!")

# Hàm chính
def main():
    # Sử dụng token mà bạn nhận được từ BotFather
    TOKEN = "8719537947:AAHjSTAt9FAx832t7_LnXaq_Kf_ZaR-pDMQ"
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, show_pinyin))  # Hiển thị Pinyin
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
