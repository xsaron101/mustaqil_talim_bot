import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# ==========================================
# SOZLAMALAR
# ==========================================

TOKEN = "8776276014:AAE0b4SmrI_lHda3BFrFlGXkwWUREk4vTdY"

ADMIN_ID = 8573650612

# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==========================================
# HOLATLAR
# ==========================================

BUYURTMA_TURI, FAN_NOMI, SAHIFA_SONI, MUDDAT, TELEFON = range(5)


# ==========================================
# /start BUYRUG'I
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📚 Kurs ishi",
                callback_data="Kurs ishi"
            )
        ],
        [
            InlineKeyboardButton(
                "📄 Referat",
                callback_data="Referat"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Taqdimot",
                callback_data="Taqdimot"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    xabar = (
        "👋 Assalomu alaykum!\n\n"
        "📚 Mustaqil ta'lim buyurtma botiga xush kelibsiz!\n\n"
        "👇 Buyurtma turini tanlang:"
    )

    await update.message.reply_text(
        xabar,
        reply_markup=reply_markup
    )

    return BUYURTMA_TURI


# ==========================================
# BUYURTMA TURINI TANLASH
# ==========================================

async def buyurtma_turi(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    context.user_data["tur"] = query.data

    matn = (
        f"✅ Siz *{query.data}* tanladingiz.\n\n"
        "📚 Endi fan nomini yozing.\n"
        "Masalan: Matematika, Fizika, Informatika"
    )

    await query.edit_message_text(
        matn,
        parse_mode="Markdown"
    )

    return FAN_NOMI


# ==========================================
# FAN NOMI
# ==========================================

async def fan_nomi(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["fan"] = update.message.text

    await update.message.reply_text(
        "📄 Sahifalar soni qancha?\n\n"
        "Masalan: 20, 30, 40"
    )

    return SAHIFA_SONI


# ==========================================
# SAHIFA SONI
# ==========================================

async def sahifa_soni(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["sahifa"] = update.message.text

    await update.message.reply_text(
        "⏰ Qachongacha kerak?\n\n"
        "Masalan: 3 kun, 1 hafta"
    )

    return MUDDAT


# ==========================================
# MUDDAT
# ==========================================

async def muddat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["muddat"] = update.message.text

    await update.message.reply_text(
        "📱 Telefon raqamingizni yozing.\n\n"
        "Masalan: +998901234567"
    )

    return TELEFON


# ==========================================
# TELEFON VA BUYURTMANI YAKUNLASH
# ==========================================

async def telefon(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["telefon"] = update.message.text

    user = update.message.from_user

    # --------------------------------------
    # TALABAGA YUBORILADIGAN XABAR
    # --------------------------------------

    talaba_xabar = (
        "✅ *Buyurtmangiz qabul qilindi!*\n\n"
        f"📌 *Tur:* {context.user_data['tur']}\n"
        f"📚 *Fan:* {context.user_data['fan']}\n"
        f"📄 *Sahifa:* {context.user_data['sahifa']}\n"
        f"⏰ *Muddat:* {context.user_data['muddat']}\n"
        f"📱 *Telefon:* {context.user_data['telefon']}\n\n"
        "☎️ Tez orada siz bilan bog'lanamiz!"
    )

    await update.message.reply_text(
        talaba_xabar,
        parse_mode="Markdown"
    )

    # --------------------------------------
    # USERNAME
    # --------------------------------------

    username = user.username if user.username else "Mavjud emas"

    # --------------------------------------
    # ADMIN UCHUN XABAR
    # --------------------------------------

    admin_xabar = (
        "🔔 *YANGI BUYURTMA!*\n\n"
        f"👤 *Talaba:* {user.full_name}\n"
        f"🔗 *Username:* @{username}\n"
        f"🆔 *ID:* {user.id}\n\n"
        f"📌 *Tur:* {context.user_data['tur']}\n"
        f"📚 *Fan:* {context.user_data['fan']}\n"
        f"📄 *Sahifa:* {context.user_data['sahifa']}\n"
        f"⏰ *Muddat:* {context.user_data['muddat']}\n"
        f"📱 *Telefon:* {context.user_data['telefon']}"
    )

    # --------------------------------------
    # ADMIN GA YUBORISH
    # --------------------------------------

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_xabar,
        parse_mode="Markdown"
    )

    return ConversationHandler.END


# ==========================================
# BUYURTMANI BEKOR QILISH
# ==========================================

async def bekor(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "❌ Buyurtma bekor qilindi.\n\n"
        "🔄 Qaytadan boshlash uchun /start buyrug'ini bosing."
    )

    return ConversationHandler.END


# ==========================================
# MAIN
# ==========================================

def main():

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(

        entry_points=[
            CommandHandler("start", start)
        ],

        states={

            BUYURTMA_TURI: [
                CallbackQueryHandler(buyurtma_turi)
            ],

            FAN_NOMI: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    fan_nomi
                )
            ],

            SAHIFA_SONI: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sahifa_soni
                )
            ],

            MUDDAT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    muddat
                )
            ],

            TELEFON: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    telefon
                )
            ],
        },

        fallbacks=[
            CommandHandler("bekor", bekor)
        ],
    )

    app.add_handler(conv_handler)

    print("✅ Bot ishga tushdi!")

    app.run_polling()


# ==========================================
# DASturni ISHGA TUSHIRISH
# ==========================================

if __name__ == "__main__":
    main()