# manage_command.py
import requests
import json
from postback import *
from db_connection import *

ACCESS_TOKEN = "EAAMKvcenz40BOZCNZA5TaYwfcyrd403LZAiE0xEiIRyGChu3WkFaX54u75sghT6wZB7eRseqpT2h4VwMYKyQOm4oziZBttKZAYOWlspfxNf0MzfkfhLYnPFhz78Bss3R1DXNDxweMEnvmFL0INlTnYqlVZCDY6GNmkIZA98Ao6g0sY38eYpZC2rnNjkFqnTU5rXbq"
url = f"https://graph.facebook.com/v17.0/351769248871162/messages?access_token={ACCESS_TOKEN}"


def handle_command(user,message_text):
    """Xử lý các lệnh người dùng và trả về phản hồi tương ứng."""
    message = message_text[1:].split()
    command = message[0]
    response = process_command(user,command, message)
    return response


def process_command(user,command, message):
    """Kiểm tra trạng thái của người dùng và trả về phản hồi tương ứng với lệnh."""
    if command == "fix":
        user.state = 'WELCOME'
        update_state(user.id, user.state)
        postback_welcome(user)
        return "Quay về WELCOME, sửa chữa mọi lỗi lầm"
    if command == "nickname":
        user.nickname = " ".join(message[1:])
        if len(user.nickname) > 17:
            return "Nickname quá dài, giới hạn là 17 kí tự (số tuổi của CDA)"
        if is_nickname_exists(user.nickname):
            return f"Nickname '{user.nickname}' đã tồn tại trong hệ thống."
        else:
            update_nickname(user.id, user.nickname)
            return f"Đã đổi nick name thành: {user.nickname}"
    if command == "gioithieu":
        user.introduce = " ".join(message[1:])
        update_introduce(user.id, user.introduce)
        return f"Đã đổi giới thiệu thành: {user.introduce}"
    if (command == 'end') | (command == 'End') | (command == 'END'):
        postback_confirm_end(user)
        return "Lời kết thúc"

    if command == 'state':
        user.state = message[1]
        update_state(user.id,user.state)
        return f"Đã đổi state thành: {user.state}"
    else:
        return "Câu lệnh chưa tồn tại, vui lòng kiểm tra danh sách câu lệnh bằng /lenh"

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
                            "image_url": "https://cdn.tuoitre.vn/thumb_w/480/471584752817336320/2023/3/5/cau-do-2-16779929961011467051251.jpg",  # Thay thế bằng URL hình ảnh bạn muốn
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
                            "image_url": "https://cdn.tuoitre.vn/thumb_w/480/471584752817336320/2023/3/5/cau-do-1-16779929960982066590826.jpg",  # Thay thế bằng URL hình ảnh bạn muốn
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
                            "image_url": "https://bibungbia.pythonanywhere.com/assets/fire.png",  # Thay thế bằng URL hình ảnh bạn muốn
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
