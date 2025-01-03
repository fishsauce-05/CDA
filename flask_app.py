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
menu_url = f"https://graph.facebook.com/v17.0/me/messenger_profile?access_token={ACCESS_TOKEN}"


logging.basicConfig(level=logging.DEBUG)

create_users_table()
users = get_all_users()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    logging.info("------------------ trigger webhook")
    if request.method == 'GET':
        # Lấy thông tin từ query parameters
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        logging.debug(f"Mode: {mode}, Token: {token}, Challenge: {challenge}")

        # Kiểm tra token xác minh
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200  # Gửi lại hub.challenge để xác thực
        else:
            return 'Forbidden', 403

    if request.method == 'POST':
        data = request.get_json()
        logging.info("Received data:", data)

        # Kiểm tra dữ liệu nếu là tin nhắn và lấy thông tin người gửi và nội dung tin nhắn
        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for message_data in entry["messaging"]:
                        sender_id = message_data["sender"]["id"]
                        if users.get(sender_id) == None:

                            count = len(users) + 1234
                            nickname = f"#CDA{count:05}"
                            users[sender_id] = User(sender_id, state = 'WELCOME', nickname = nickname, introduce = "Chưa có")
                            save_user_to_db(users.get(sender_id))
                            user = users.get(sender_id)
                            postback_welcome(user)

                        user = users.get(sender_id)

                        if "message" in message_data:
                            message_text = message_data["message"].get("text", "")
                            print("ID: ", sender_id)
                            # Gửi phản hồi lại đúng nội dung tin nhắn
                            if message_text:
                                # Nếu tin nhắn bắt đầu bằng "/"
                                if message_text.startswith("/"):
                                    response = handle_command(user, message_text) #handle_command
                                    if response:
                                        send_message(sender_id, response)
                                else:
                                    if user.state == 'TALK':
                                        send_message(user.partner_id, message_text)
                                    else:
                                        send_message(sender_id, "CÁI NÀY ĐỂ FIX BUG, KỆ ĐI:\n" + user.state)

                        if "postback" in message_data:
                            handle_postback(user, message_data["postback"]["payload"], users) #handle_postback
                            send_message(sender_id,"CÁI NÀY ĐỂ FIX BUG, KỆ ĐI:\nPayload: " + message_data["postback"]["payload"] + "\nState: " + user.state)


        return "Message Received", 200


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

def send_message(recipient_id, message_text):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        print(f"Message sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        if response.status_code == 500:
            print(f"Response content: {response.text}")

def setup_persistent_menu():
    menu_url = f"https://graph.facebook.com/v17.0/me/messenger_profile?access_token={ACCESS_TOKEN}"
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
                    {"type": "postback", "title": "Report", "payload": "MENU_REPORT"},
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
    url = f"https://graph.facebook.com/v17.0/me/messenger_profile?access_token={ACCESS_TOKEN}"
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
    menu_url = f"https://graph.facebook.com/v17.0/me/messenger_profile?access_token={ACCESS_TOKEN}"
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

