# Telegram OSINT Bot

1. أنشئ repo جديد في GitHub وادخل المشروع.
2. ارفع ملفات Excel (`.xlsx`) في مجلد `databases/`.
3. اربط المشروع مع Render:
   - اختر "New → Web Service"
   - ربط مع GitHub repo اللي أنشأته
   - أدخل:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn main:app`
   - أضف في Environment:
     - KEY: `BOT_TOKEN`
     - VALUE: `توكن_البوت_من_BotFather`
4. Render رح يعطيك رابط HTTPS مثل: `https://osint-bot.onrender.com`
5. ارسل للـ webhook:
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<your-app>.onrender.com/webhook
6. روح لتليجرام وجرب:
   - /start → اختار طريقة البحث → اكتب الاسم أو الرقم → تظهر النتائج من ملفاتك
