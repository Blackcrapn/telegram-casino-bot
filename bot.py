import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.getenv('8401279746:AAHKHzsJpuhoj-5V9nnhEJroTsRlMe0KtZA')

class SimpleBot:
    def __init__(self):
        self.creator_id = None
        self.users = {}

    def init_user(self, user_id: int, username: str):
        if user_id not in self.users:
            self.users[user_id] = {
                "username": username, "balance": 1000, "games_played": 0
            }

bot_data = SimpleBot()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    if bot_data.creator_id is None:
        bot_data.creator_id = user_id
        await update.message.reply_text("🎉 Вы создатель! Баланс: ∞")
    else:
        if user_id == bot_data.creator_id:
            await update.message.reply_text("👑 Создатель!")
        else:
            await update.message.reply_text("🎰 Добро пожаловать!")
    
    bot_data.init_user(user_id, user.username)
    await update.message.reply_text("Команды: /play [ставка] /stats /author")

async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👨‍💻 Автор: Самир")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_data.init_user(user_id, update.effective_user.username)
    
    if len(context.args) != 1:
        await update.message.reply_text("Использование: /play [ставка]")
        return

    try:
        bet = int(context.args[0])
    except:
        await update.message.reply_text("❌ Ставка должна быть числом")
        return

    user = bot_data.users[user_id]
    is_creator = user_id == bot_data.creator_id
    
    if not is_creator and bet > user["balance"]:
        await update.message.reply_text("❌ Недостаточно средств")
        return

    if bet <= 0:
        await update.message.reply_text("❌ Ставка > 0")
        return

    if not is_creator:
        user["balance"] -= bet
    
    user["games_played"] += 1

    if random.choice([True, False]):
        win_amount = bet * 2
        result_text = f"🎉 Выиграл {win_amount}!"
        if not is_creator:
            user["balance"] += win_amount
    else:
        win_amount = 0
        result_text = "❌ Проиграл"

    result_text += f"\n💰 Баланс: {'∞' if is_creator else user['balance']}"
    await update.message.reply_text(result_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_data.init_user(user_id, update.effective_user.username)
    
    user = bot_data.users[user_id]
    is_creator = user_id == bot_data.creator_id
    
    await update.message.reply_text(
        f"📊 Статистика {'👑' if is_creator else ''}\n"
        f"💰 Баланс: {'∞' if is_creator else user['balance']}\n"
        f"🎮 Игр: {user['games_played']}"
    )

def main():
    if not TOKEN:
        print("❌ Токен не найден!")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("author", author))
    
    print("🤖 Бот запущен! Работает 24/7")
    application.run_polling()

if __name__ == '__main__':
    main()
