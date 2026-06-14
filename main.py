import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 1. First Screen: Welcome, Testimonials & Free Channel Join
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔘 JOIN FREE CHANNEL", url="https://t.me/apexedge99")],
        [InlineKeyboardButton("✅ I Joined The Free Channel", callback_data="joined_free")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "<b>Welcome to Apex Entries 📊</b>\n\n"
        "Join our free public group first, watch our performance, analysis, and execution style — "
        "then apply for VIP access if you want to take your trading to the next level.\n\n"
        "Inside the free channel you'll see:\n"
        "• Free market analysis\n• Live trade ideas\n• Gold (XAUUSD) updates\n"
        "• Educational content\n• Real execution examples\n\n"
        "━━━━━━━━━━━━━━\n"
        "After joining the free channel, return here and press the button below."
    )
    
    # Check if this is a fresh /start command or a "Back" button press
    if update.message:
        # DEBUG: List all files in current directory
        current_dir = os.getcwd()
        all_files = os.listdir(current_dir)
        logging.info(f"Current directory: {current_dir}")
        logging.info(f"All files found: {all_files}")
        
        # Try multiple possible filename patterns
        possible_names = [
            "1 jpeg", "2 jpeg", "3 jpeg", "4 jpeg", "5 jpeg",  # With space
            "1.jpeg", "2.jpeg", "3.jpeg", "4.jpeg", "5.jpeg",  # With dot
            "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg",      # With .jpg
            "1", "2", "3", "4", "5"                            # Just numbers
        ]
        
        # Find which files actually exist
        image_files = []
        for name in possible_names:
            if os.path.exists(name):
                image_files.append(name)
                logging.info(f"Found image file: {name}")
        
        # If no files found with exact names, look for any jpeg/jpg files
        if not image_files:
            for file in all_files:
                if file.lower().endswith(('.jpeg', '.jpg')):
                    image_files.append(file)
                    logging.info(f"Found image file by extension: {file}")
        
        media_group = []
        
        # Build the media group array
        for i, file_name in enumerate(image_files[:5]):  # Limit to 5 images
            try:
                with open(file_name, 'rb') as f:
                    image_data = f.read()
                    if i == 0:
                        media_group.append(InputMediaPhoto(media=image_data, caption=text, parse_mode="HTML"))
                    else:
                        media_group.append(InputMediaPhoto(media=image_data))
                logging.info(f"Successfully loaded: {file_name}")
            except Exception as e:
                logging.error(f"Error loading {file_name}: {e}")

        if media_group:
            # Send the album with images
            await update.message.reply_media_group(media=media_group)
            # Send the inline keyboard buttons underneath
            await update.message.reply_text("👇 Use the buttons below to proceed:", reply_markup=reply_markup)
        else:
            # Fallback: send text only
            logging.warning("No images found, sending text-only message")
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")
            
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

# 2. Button Handler for the Flow
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "joined_free":
        keyboard = [
            [InlineKeyboardButton("🏆 Apply For VIP Access", callback_data="apply_vip")],
            [InlineKeyboardButton("📩 Send Message To Support", callback_data="support_info")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "<b>Good decision ✅</b>\n\n"
            "Now you can apply for access to the private VIP group where we share:\n\n"
            "📊 Advanced market analysis\n🎯 Structured trade executions\n"
            "📍 Liquidity & institutional zones\n🎥 Analysis before entries\n"
            "🧠 Professional trading concepts\n\n"
            "Choose an option below 👇"
        )
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

    elif query.data == "apply_vip":
        keyboard = [
            [InlineKeyboardButton("🔗 Register with Vantage", url="https://vigco.co/la-com/aRdk9CvK")],
            [InlineKeyboardButton("✅ Send ID to Support", url="https://t.me/reedexecution")],
            [InlineKeyboardButton("⬅️ Back", callback_data="joined_free")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = (
            "🔘 <b>Apply For VIP Access</b>\n\n"
            "1️⃣ Register with our trusted broker Vantage using the official link below\n"
            "2️⃣ Verify your account\n"
            "3️⃣ Log in and activate the promotion from the Bonus/Promotions section\n"
            "4️⃣ Fund the account\n"
            "5️⃣ Send your account ID screenshot\n\n"
            "Once approved, you'll receive the VIP group access link 🔐\n\n"
            "🎁 <b>Vantage Promotion:</b>\n"
            "• Get 150% bonus on your first deposit\n"
            "• Get 25% bonus on every future deposit"
        )
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

    elif query.data == "support_info":
        keyboard = [
            [InlineKeyboardButton("👉 Contact Support", url="https://t.me/reedexecution")],
            [InlineKeyboardButton("⬅️ Back", callback_data="joined_free")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "🔘 <b>Send Message To Support</b>\n\n"
            "For direct support, VIP approval, or questions regarding access:\n\n"
            "Our team is ready to assist you with your transition to VIP."
        )
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

    elif query.data == "back_to_start":
        await start(update, context)

# 3. Main Function
def main():
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        print("ERROR: Please set your BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_buttons))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
