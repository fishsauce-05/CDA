from flask import Flask, request
import requests
import logging
# from dotenv import load_dotenv
import json

from manage_command import handle_command
from db_connection import *
from user import User
from postback import *
from manage_postback import handle_postback
from handle_waitlist import *
from constant import *

# Load biến môi trường từ file .env
app = Flask(__name__, static_folder="assets")

VERIFY_TOKEN = "CDA"


logging.basicConfig(level=logging.DEBUG)

create_users_table()
users = get_all_users()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    if request.method == 'GET':
        # Facebook xác thực webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200  # Trả về mã xác thực
        else:
            return 'Forbidden', 403

    elif request.method == 'POST':
        # Xử lý tin nhắn từ webhook
        data = request.get_json()
        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for message_data in entry["messaging"]:
                        sender_id = message_data["sender"]["id"]

                        # Kiểm tra nếu người dùng mới
                        if sender_id not in users:
                            new_user = User(sender_id,"WELCOME")
                            users[sender_id] = new_user
                            save_user_to_db(new_user)

                        user = users[sender_id]

                        # Xử lý tin nhắn văn bản và ảnh+ video
                        if "message" in message_data:
                            if "attachments" in message_data["message"]:
                                for attachment in message_data["message"]["attachments"]:
                                    if attachment["type"] == "image":
                                        image_url = attachment["payload"]["url"]
                                        if user.state == 'TALK' and user.partner_id:
                                            send_image(user.partner_id, image_url)
                                        else:
                                            send_message(sender_id, "Bạn chưa có đối phương trong cuộc trò chuyện.")
                                    elif attachment["type"] == "video":
                                        video_url = attachment["payload"]["url"]
                                        if user.state == 'TALK' and user.partner_id:
                                            send_video(user.partner_id, video_url)
                                        else:
                                            send_message(sender_id, "Bạn chưa có đối phương trong cuộc trò chuyện.")
                                    elif attachment["type"] == "audio":
                                        audio_url = attachment["payload"]["url"]
                                        if user.state == 'TALK' and user.partner_id:
                                           # send_message(sender_id, "Nhớ giọng Trinh vãiii")
                                            send_audio(user.partner_id, audio_url)
                                        else:
                                            send_message(sender_id, "Bạn chưa có đối phương trong cuộc trò chuyện")
                            elif "text" in message_data["message"]:
                                message_text = message_data["message"].get("text", "")
                                print("ID: ", sender_id)
                                # Gửi phản hồi lại đúng nội dung tin nhắn
                                if message_text:
                                    # Nếu tin nhắn bắt đầu bằng "/"
                                    if message_text.startswith("/"):
                                        response = handle_command(user, message_text) #handle_command
                                        if response:
                                            send_message(sender_id, response)
                                            if message_text.startswith("/nickname") or message_text.startswith("/gioithieu"):
                                                if user.state != 'SEARCH':
                                                    postback_retry(user) #Gửi thông báo đã đổi biệt danh/giới thiệu trước khi tìm kiếm
                                    else:
                                        if user.state == 'TALK':
                                            send_message(user.partner_id, message_text)
                                        # else:
                                        #     send_message(sender_id, "CÁI NÀY ĐỂ FIX BUG, KỆ ĐI:\n" + user.state)
                                        elif user.state == 'WELCOME' or user.state == 'END':
                                            postback_welcome(user)
                                        else:
                                            send_message(sender_id, "🤖 Dường như bạn đang chưa rõ cách hoạt động của tụi mình\n Hãy bấm vào nút *Hướng dẫn sử dụng* để hiểu rõ hơn cách tụi mình hoạt động nhé!")
                                           # send_message(sender_id, "CÁI NÀY ĐỂ FIX BUG, KỆ ĐI:\n" + user.state)
                        # Xử lý postback
                        if "postback" in message_data:
                            handle_postback(user, message_data["postback"]["payload"], users)
                          #  send_message(sender_id,"CÁI NÀY ĐỂ FIX BUG, KỆ ĐI:\nPayload: " + message_data["postback"]["payload"] + "\nState: " + user.state)

        return "Message received", 200



# def handle_postback(user, payload):
#     # actions = {
#     #     "START_CHAT": "Bắt đầu cuộc trò chuyện!",
#     #     "GUIDE": "Đây là hướng dẫn sử dụng!",
#     #     "END_CHAT": "Kết thúc cuộc trò chuyện và về hàng chờ.",
#     #     "CHANGE_INFO": "Vui lòng cung cấp thông tin mới.",
#     #     "REPORT": "Vui lòng báo cáo vấn đề.",
#     #     "VIEW_QUEUE": "Xem hàng chờ hiện tại."
#     # }
#     match payload:
#         case "START_CHAT":
#             postback_welcome(user)
#             user.next_state()
#             update_state(user.id, user.state)
#             send_message(user.id, user.state)
#             return None
#     # message = actions.get(payload, "Lệnh không hợp lệ.")
#     send_message(user.id, user.state)

#Giong Trinh dauu
def send_audio(recipient_id, audio_url):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "audio",
                "payload": {"url": audio_url}
            }
        },
        "messaging_type": "RESPONSE"
    }
    try:
        response = requests.post(f"https://graph.facebook.com/{facebook_api_version}/me/messages?access_token={ACCESS_TOKEN}", headers=headers, json=payload)
        response.raise_for_status()
        print(f"Audio sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send audio: {e}")

#Gui clip
def send_video(recipient_id, video_url):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "video",
                "payload": {"url": video_url}
            }
        },
        "messaging_type": "RESPONSE"
    }
    try:
        response = requests.post(f"https://graph.facebook.com/{facebook_api_version}/me/messages?access_token={ACCESS_TOKEN}", headers=headers, json=payload)
        response.raise_for_status()
        print(f"Video sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send video: {e}")

#Gui clip-send
def send_message(recipient_id, message_text):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE"
    }
    try:
        response = requests.post(f"https://graph.facebook.com/{facebook_api_version}/me/messages?access_token={ACCESS_TOKEN}", headers=headers, json=payload)
        response.raise_for_status()
        print(f"Message sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
#Xu ly hinh anh
def send_image(recipient_id, image_url):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {"url": image_url}
            }
        },
        "messaging_type": "RESPONSE"
    }
    try:
        response = requests.post(f"https://graph.facebook.com/{facebook_api_version}/me/messages?access_token={ACCESS_TOKEN}", headers=headers, json=payload)
        response.raise_for_status()
        print(f"Image sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send image: {e}")

def setup_persistent_menu():
    payload = {
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": False,
                "call_to_actions": [
                    {"type": "postback", "title": "Bắt đầu", "payload": "#WELCOME"},
                    {"type": "postback", "title": "Hướng dẫn", "payload": "MENU_GUIDE"},
                    {"type": "postback", "title": "❌KẾT THÚC", "payload": "MENU_END"},
                    {"type": "postback", "title": "Đổi thông tin", "payload": "MENU_CHANGE_INFO"},
                    {"type": "postback", "title": "Xem hàng chờ", "payload": "MENU_VIEW_QUEUE"}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(menu_url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Persistent menu created successfully!")
    else:
        print("Failed to create persistent menu.")
        print("Response:", response.json())

def delete_persistent_menu():
    url = f"https://graph.facebook.com/{facebook_api_version}/me/messenger_profile?access_token={ACCESS_TOKEN}"
    payload = {
        "fields": ["persistent_menu"]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Persistent menu deleted successfully!")
    else:
        print("Failed to delete persistent menu.")
        print(response.json())

def setup_get_started_button():
    payload = {
        "get_started": {
            "payload": "#WELCOME"
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(menu_url, json=payload, headers=headers)
    print(response.json())

if __name__ == "__main__":
    setup_get_started_button()
    # postback_welcome()
    delete_persistent_menu()
    setup_persistent_menu()
    app.run(debug=False, port=5005)