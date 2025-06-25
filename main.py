import os, pandas as pd
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def load_all_data():
    dfs = []
    for f in os.listdir("databases"):
        if f.endswith(".xlsx"):
            df = pd.read_excel(os.path.join("databases", f))
            name = next((c for c in df.columns if 'name' in c.lower() or 'اسم' in c), None)
            num = next((c for c in df.columns if 'number' in c.lower() or 'رقم' in c), None)
            if name and num:
                df = df[[name,num]].copy()
                df.columns = ['name','number']
                dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame(columns=['name','number'])

data = load_all_data()

def start(update, context):
    kb = [[InlineKeyboardButton("🔍 الاسم", callback_data='name')],
          [InlineKeyboardButton("🔢 الرقم", callback_data='number')]]
    update.message.reply_text("اختر طريقة البحث:", reply_markup=InlineKeyboardMarkup(kb))

def choose(update, context):
    query = update.callback_query
    query.answer()
    context.user_data['mode'] = query.data
    prompt = "✍️ اكتب الاسم:" if query.data=='name' else "📞 اكتب الرقم:"
    query.edit_message_text(prompt)

def handle_msg(update, context):
    text = update.message.text.strip()
    mode = context.user_data.get('mode')
    if not mode: 
        return update.message.reply_text("أرسل /start لاختيار نوع البحث")
    col = 'name' if mode=='name' else 'number'
    df = data[data[col].astype(str).str.contains(text, case=False, na=False)]
    if df.empty:
        update.message.reply_text("❌ بلا نتائج.")
    else:
        resp = "\n".join(f"👤 {r['name']} - 📞 {r['number']}" for _,r in df.head(10).iterrows())
        update.message.reply_text(resp)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(choose))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_msg))

@app.route("/webhook", methods=["POST"])
def webhook():
    dispatcher.process_update(request.get_json(force=True))
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)