import psutil
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

prefix = os.getenv('APP_NAME')
cpu_warning_threshold = int(os.getenv('CPU_WARNING_THRESHOLD'))
is_cpu_warning_active = False
tg_bot_chatid = "1348940059"

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://tgbot.www.vanportdev.com/msg/{tg_bot_chatid}";
    payload = {
        'msg': message,
    }
    requests.post(url, json=payload)

# Function to monitor CPU usage
def monitor_cpu_usage():
    global is_cpu_warning_active
    while True:
        # Get total CPU usage
        total_cpu_usage = psutil.cpu_percent(interval=1) * psutil.cpu_count()
        print(f"<b>[{prefix}]</b> Total CPU Usage: {total_cpu_usage}%")

        # Check if total CPU usage exceeds 400%
        if total_cpu_usage > cpu_warning_threshold:
            if not is_cpu_warning_active:
                is_cpu_warning_active = True
                send_telegram_message(f"<b>[{prefix}]</b> cpu_notifier >> Alert: ⚠️  Total CPU usage exceeded {cpu_warning_threshold}%. Current usage: <b>{total_cpu_usage}%</b>")
        else:
            if is_cpu_warning_active:
                is_cpu_warning_active = False
                send_telegram_message(f"<b>[{prefix}]</b> cpu_notifier >> Alert: ❤️  Total CPU usage resumed normal. Current usage: <b>{total_cpu_usage}%</b>")

        time.sleep(1)  # Check every 5 seconds

if __name__ == "__main__":
    send_telegram_message(f"<b>[{prefix}]</b> cpu_notifier >> Engaged 👌 ")
    monitor_cpu_usage()

