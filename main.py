import logging
from telegram import (
    Update, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackContext
)

# === AYARLAR ===
BOT_TOKEN = "BURAYA_BOT_TOKENİNİ_YAZ"
ZORUNLU_KANALLAR = ["R1704Y", "kfJt32U3Qo1jOWZk"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === KANAL KONTROL ===
async def kanallara_abone_mi(user_id: int, context: CallbackContext) -> bool:
    for kanal in ZORUNLU_KANALLAR:
        try:
            member = await context.bot.get_chat_member(f"@{kanal}", user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# === /start ===
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if not await kanallara_abone_mi(user.id, context):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Kanal 1", url="https://t.me/R1704Y")],
             [InlineKeyboardButton("📢 Kanal 2", url="https://t.me/+kfJt32U3Qo1jOWZk")]]
        )
        await update.message.reply_text(
            "🚫 Erişim Engellendi\n\n"
            "Botu kullanabilmek için önce aşağıdaki kanallara katılmalısın:\n"
            "➡️ @R1704Y\n"
            "➡️ @kfJt32U3Qo1jOWZk\n\n"
            "✅ Katıldıktan sonra /start yaz.",
            reply_markup=keyboard
        )
        return

    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton("📌 Komutlar")],
            [KeyboardButton("ℹ️ Bilgi")],
            [KeyboardButton("💎 Premium")]
        ],
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"✨ Hoş geldin {user.first_name}!\n\n"
        "🔹 Benim görevim senin için log ve proxy hizmeti sağlamak.\n"
        "🔹 Ayrıca gönderdiğin dosyaları işleyip temizleyebilirim.\n\n"
        "🎛️ Menüden istediğin aracı seç ve kullanmaya başla.",
        reply_markup=menu
    )

# === KOMUTLAR ===
async def komutlar(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📌 Komutlar Menüsü\n\n"
        "🔎 /log <site> → Belirtilen siteye ait logları çek.\n"
        "🧹 /urltemizle → Log dosyalarındaki URL kısmını temizle.\n"
        "🌐 /proxy_list → Proxy listesi indir.\n"
        "💎 /premium → Premium üyelik hakkında bilgi al."
    )

# === HAKKIMIZDA ===
async def hakkimizda(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ Bilgilendirme\n\n"
        "Bu bot senin için:\n"
        "- Proxy ve log toplar\n"
        "- Dosyaları temizler\n"
        "- Premium olursan ekstra özellikler açılır\n\n"
        "⏱️ Bot sürekli aktif ve kesintisiz çalışır."
    )

# === PREMIUM ===
async def premium(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💎 Premium Üyelik\n\n"
        "✔️ Daha hızlı sorgulama\n"
        "✔️ Öncelikli destek\n\n"
        "📩 Premium satın almak için: @kyrenwastaken"
    )

# === MESAJ YAKALAYICI (Menü Butonları) ===
async def mesaj_yakalayici(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "📌 Komutlar":
        await komutlar(update, context)
    elif text == "ℹ️ Bilgi":
        await hakkimizda(update, context)
    elif text == "💎 Premium":
        await premium(update, context)
    else:
        await update.message.reply_text("❓ Geçerli bir seçim yapmadın. Menüden tuşlara basabilirsin.")

# === MAIN ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("komutlar", komutlar))
    app.add_handler(CommandHandler("hakkimizda", hakkimizda))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakalayici))

    print("✅ Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
