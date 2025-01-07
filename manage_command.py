# manage_command.py
import requests
import json
from postback import *
from db_connection import *
from constant import *


def handle_command(user, message_text):
    """Xử lý các lệnh người dùng và trả về phản hồi tương ứng."""
    # Tách từng dòng của tin nhắn
    commands = message_text.strip().split("\n")
    responses = []

    for command_text in commands:
        if command_text.startswith("/"):
            message = command_text[1:].split()
            command = message[0]
            response = process_command(user, command, message)
            responses.append(response)
        else:
            responses.append("Câu lệnh không hợp lệ. Hãy bắt đầu lệnh với '/'.")

    # Kết hợp các phản hồi lại thành một chuỗi, mỗi phản hồi trên một dòng
    return "\n".join(responses)

def process_command(user, command, message):
    """
    Kiểm tra trạng thái của người dùng và trả về phản hồi tương ứng với lệnh.
    """
    if command == "fix":
        user.state = 'WELCOME'
        update_state(user.id, user.state)
        postback_welcome(user)
        return "Quay về WELCOME, sửa chữa mọi lỗi lầm."

    if command == "nickname":
        new_nickname = " ".join(message[1:])
        if not new_nickname:
            return "Bạn chưa nhập nickname. Vui lòng nhập nickname sau lệnh /nickname."
        if len(new_nickname) > 17:
            return "Nickname quá dài, giới hạn là 17 kí tự."
        if is_nickname_exists(new_nickname):
            return f"Nickname '{new_nickname}' đã tồn tại trong hệ thống."
        else:
            user.nickname = new_nickname
            update_nickname(user.id, user.nickname)
            return f"Đã đổi nickname thành: {user.nickname}."
            postback_retry(user)  # Kiểm tra thông tin sau khi đổi nickname

    if command == "gioithieu":
        new_introduce = " ".join(message[1:])
        if not new_introduce:
            return "Bạn chưa nhập phần giới thiệu. Vui lòng nhập phần giới thiệu sau lệnh /gioithieu."
        user.introduce = new_introduce
        update_introduce(user.id, user.introduce)
        return f"Đã đổi giới thiệu thành: {user.introduce}."
        postback_retry(user)  # Kiểm tra thông tin sau khi đổi giới thiệu

    if command.lower() == "end":
        postback_confirm_end(user)
        return "Lời kết thúc."

    if command == "state":
        if len(message) < 2:
            return "Bạn cần cung cấp state mới. Ví dụ: /state WELCOME."
        new_state = message[1].upper()
        user.state = new_state
        update_state(user.id, user.state)
        return f"Đã đổi state thành: {user.state}."

    if command == "lenh":
        return (
            "Danh sách lệnh khả dụng: \n"
            "/nickname [biệt danh] - Đặt biệt danh.\n"
            "/gioithieu [giới thiệu] - Viết giới thiệu ngắn gọn.\n"
            "/end - Kết thúc cuộc trò chuyện."
        )

    return "Câu lệnh chưa tồn tại, vui lòng kiểm tra danh sách câu lệnh bằng /lenh."



def send_button_template(recipient_id):
    """Gửi generic template với 4 sự lựa chọn và ảnh minh họa"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "CHAT ẨN DANH NÀO!",
                            "image_url": image_menu_welcome_1,  # Thay thế bằng URL hình ảnh bạn muốn
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Bắt đầu",
                                    "payload": "START_CHAT"
                                },
                                {
                                    "type": "postback",
                                    "title": "Hướng dẫn sử dụng",
                                    "payload": "GUIDE"
                                },
                                {
                                    "type": "postback",
                                    "title": "Giới thiệu",
                                    "payload": "GUIDE"
                                }
                            ]
                        },
                        {
                            "title": "CHUYỆN GÌ ĐANG DIỄN RA VẬY?",
                            "image_url": image_menu_welcome_2,  # Thay thế bằng URL hình ảnh bạn muốn
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Sắp tới CDA có gì?",
                                    "url": "https://www.facebook.com/photo?fbid=1215821146884051&set=a.611431897322982"
                                },
                                {
                                    "type": "postback",
                                    "title": "Xem hàng chờ",
                                    "payload": "VIEW_QUEUE"
                                }

                            ]
                        },
                        {
                            "title": "LIÊN HỆ CHÚNG MÌNH",
                            "image_url": image_menu_welcome_3,  # Thay thế bằng URL hình ảnh bạn muốn
                            "buttons": [
                                {
                                    "type":"web_url",
                                    "title": "Báo lỗi",
                                    "url":"https://www.facebook.com/CDAclub"
                                },
                                {
                                    "type": "postback",
                                    "title": "Liên hệ admin",
                                    "payload": "CONTACT_ADMIN"
                                },
                                {
                                    "type":"web_url",
                                    "title": "Fanpage CDA",
                                    "url":"https://www.facebook.com/CDAclub"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        print(f"Generic template with image sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send generic template with image: {e}")