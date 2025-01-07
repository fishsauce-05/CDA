from user import User
import requests
import json
from db_connection import *
from handle_waitlist import *
from constant import *

headers = {"Content-Type": "application/json"}
def out(payload):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        print(f"Generic template with image sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send generic template with image: {e}")

#Bắt đầu sửa từ đây

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

def postback_welcome(user):  # Template hiện ra lúc chào đón
    # Kiểm tra thông tin nickname và giới thiệu
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = (
            "🎉 Chào mừng sự trở lại của Chatbot Hẹn Hò! 🎉\n\n"
            "Sau một thời gian vắng bóng, chatbot hẹn hò của CDA đã chính thức quay trở lại và mạnh mẽ hơn bao giờ hết! 🚀 "
            "Với những nâng cấp đáng chú ý, chatbot hẹn hò giờ đây không chỉ giúp bạn tìm được những cuộc trò chuyện thú vị mà còn mang lại những kết nối thực sự, gần gũi và cá nhân hóa hơn.\n\n"
            "✨ Tại sao bạn nên thử sử dụng chatbot hẹn hò của CDA:\n"
            "💬 Tìm kiếm bạn đồng hành: Chatbot giúp bạn khám phá những hồ sơ phù hợp với sở thích và yêu cầu của bạn.\n"
            "💡 Gợi ý những câu hỏi hẹn hò: Chatbot cung cấp những câu hỏi thú vị để bạn dễ dàng tạo ra một cuộc trò chuyện lôi cuốn.\n"
            "📅 Trò chuyện tự động và nhanh chóng: Bạn có thể trò chuyện với chatbot để làm quen và tìm hiểu, hoặc đơn giản là giải trí.\n"
            "💬 Hỗ trợ 24/7: Dù bạn ở đâu, vào lúc nào, chatbot luôn sẵn sàng trợ giúp.\n"
            "🔒 Tính năng bảo mật và riêng tư: Mọi thông tin cá nhân của bạn sẽ được bảo vệ an toàn.\n\n"
            "🎉 Trải nghiệm ngay và tìm kiếm tình yêu! Đừng ngần ngại trò chuyện với chatbot của chúng mình để bắt đầu hành trình tìm kiếm một nửa yêu thương!\n\n"
            "👉 Để bắt đầu, hãy ấn nút *BẮT ĐẦU* ngay nhé!"
        )
        payload_text = {
            "recipient": {"id": user.id},
            "message": {"text": text}
        }
        out(payload_text)

    text = (
        "🎉 Trang chủ của Chatbot Hẹn Hò!"
    )

    payload_text = {
        "recipient": {"id": user.id},
        "message": {"text": text}
    }
    out(payload_text)

    # Luôn hiển thị template chào mừng
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "CHAT ẨN DANH NÀO!",
                            "image_url": image_menu_welcome_1,
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Bắt đầu",
                                    "payload": "#START"
                                },
                                {
                                    "type": "postback",
                                    "title": "Hướng dẫn sử dụng",
                                    "payload": "MENU_GUIDE"
                                },
                                {
                                    "type": "postback",
                                    "title": "Giới thiệu",
                                    "payload": "MENU_INTRODUCTION"
                                }
                            ]
                        },
                        {
                            "title": "ĐANG CÓ GÌ DIỄN RA VẬY?",
                            "image_url": image_menu_welcome_2,
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "title": "Sắp tới CDA có gì?",
                                    "url": "https://www.facebook.com/share/p/19XFWoMewv/?mibextid=wwXIfr"
                                },
                                {
                                    "type": "postback",
                                    "title": "Xem hàng chờ",
                                    "payload": "MENU_VIEW_QUEUE"
                                }
                            ]
                        },
                        {
                            "title": "ALO, TÔI NGHE",
                            "image_url": image_menu_welcome_3,
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "title": "Báo lỗi",
                                    "url": "https://www.messenger.com/t/226475877409994"
                                },
                                {
                                    "type": "web_url",
                                    "title": "Liên hệ admin",
                                    "url": "https://www.messenger.com/t/226475877409994"
                                },
                                {
                                    "type": "web_url",
                                    "title": "Fanpage CDA",
                                    "url": "https://www.facebook.com/CDAclub"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    out(payload)
    send_image(user.id, sticker_welcome)


def postback_first_come_nickname(user):
    # Kiểm tra nickname
    if not user.introduce or user.introduce == "Chưa có":
        text = ''' 💡Bạn hãy nhập theo cú pháp sau:
👉 /nickname <nickname_của_bạn>
✨ Ví dụ: /nickname mai khanhh
        '''
        payload = {
            "recipient": {"id": user.id},
            "message": {"text": text}
        }
        out(payload)
        return False  # Chưa hoàn thành bước này
    return True  #  giới thiệu đã hợp lệ

def postback_first_come(user):
    text = (
        "💡 *Thông tin hiện tại của bạn:*\n"
        "• Nickname: (chưa có)\n"
        "• Giới thiệu: (chưa có)\n\n"
        "👉 Để bắt đầu, hãy ấn nút ở phía dưới để điền đầy đủ thông tin cần thiết\n"
    )

    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Điền thông tin bản thân",
                            "payload": "#START_NHAP"
                        }
                    ]
                }
            }
        }
    }
    out(payload)


def postback_remind_nickname(user):
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = '''Tiếp tới, bạn hãy điền phần giới thiệu. Vui lòng nhập thông tin trước khi tiếp tục.
+ Câu lệnh: /gioithieu <giới_thiệu_bản_thân>
       VD : /gioithieu Tôi là thành viên CLB CDA Gen 17
            /gioithieu cần người gấp màn hộ, nhiều muỗi mà bung màn ra không bít gấp 🥺
'''
        payload = {
            "recipient": {"id": user.id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "NHẬP THÔNG TIN",
                                "payload": "#RETRY"
                            }
                        ]
                    }
                }
            }
        }
    else:
        text = '''Đừng quên các câu lệnh:
/nickname để đổi biệt danh
/gioithieu để giới thiệu ngắn về mình nhé!
'''
        payload = {
            "recipient": {"id": user.id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "TIẾP",
                                "payload": "#NEXT"
                            }
                        ]
                    }
                }
            }
        }
    out(payload)


def postback_setting(user):
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = '''Tiếp tới, bạn hãy điền phần giới thiệu. Vui lòng nhập thông tin trước khi tiếp tục.
Câu lệnh: /gioithieu <giới_thiệu_bản_thân>
VD : /gioithieu Tôi là thành viên CLB CDA Gen 17

'''
        payload = {
            "recipient": {"id": user.id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "NHẬP THÔNG TIN",
                                "payload": "#RETRY"
                            }
                        ]
                    }
                }
            }
        }
    else:
        gender, partner = 'A', 'B'
        match user.gender:
            case 'MALE':
                gender = '👱‍♂️ Nam'
            case 'FEMALE':
                gender = '👱‍♀️ Nữ'
            case 'BI':
                gender = '🏳️‍🌈 Bisexual'
        match user.partner_gender:
            case 'MALE':
                partner = '👱‍♂️ Nam'
            case 'FEMALE':
                partner = '👱‍♀️ Nữ'
            case 'BI':
                partner = '🏳️‍🌈 Bisexual'

        text = f'''🤖 *Thông tin hiện tại của bạn:*  
- 🏷️ *Nickname:* {user.nickname}  
- 👤 *Giới tính bạn chọn:* {gender}  
- ❤️ *Gu bạn chọn:* {partner}  
- ✍️ *Giới thiệu ngắn gọn:* "{user.introduce}"  

👉 Bạn có muốn thay đổi thông tin hay bắt đầu tìm kiếm ngay? 🎯  
        '''
        payload = {
            "recipient": {"id": user.id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "TÌM KIẾM LUÔN!",
                                "payload": "#SEARCH"
                            },
                            {
                                "type": "postback",
                                "title": "ĐỔI THÔNG TIN",
                                "payload": "#CHANGE"
                            }
                        ]
                    }
                }
            }
        }
    out(payload)


def postback_setgender(user):
    """Hiển thị bước chọn giới tính."""
    text = "Hãy chọn giới tính của bạn:"
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": [
                        {"type": "postback", "title": "👱‍♂️ Nam", "payload": "#ME_MALE"},
                        {"type": "postback", "title": "👱‍♀️ Nữ", "payload": "#ME_FEMALE"},
                        {"type": "postback", "title": "🏳️‍🌈 Bisexual", "payload": "#ME_BI"}
                    ]
                }
            }
        }
    }
    out(payload)


def  postback_partnergender(user): #Hiện ra để người dùng chọn gu của mình
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Gu của bạn là gì?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "👱‍♂️ Nam",
                            "payload": "#YOU_MALE"
                        },
                        {
                            "type": "postback",
                            "title": "👱‍♀️ Nữ",
                            "payload": "#YOU_FEMALE"
                        },
                        {
                            "type": "postback",
                            "title": "🏳️‍🌈 Bisexual",
                            "payload": "#YOU_BI"
                        },
                    ]
                }
            }
        }
    }
    out(payload)

def postback_search(user): #Thông báo bắt đầu tìm kiếm
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": " 🤖BOTBOT đang tìm kiếm...\nĐợi chút nhé",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "DỪNG TÌM KIẾM",
                            "payload": "#STOP_SEARCH"
                        }

                    ]
                }
            }
        }
    }
    out(payload)
    send_image(user.id, sticker_search)

def postback_found(user, partner, wait_time):
    #Code ne
    diff = datetime.now() - partner.last_action_time if partner.last_action_time else timedelta(seconds=0)
    wait_seconds = diff.total_seconds()  #Thay time

    #dk
    if wait_seconds < 60:
        text_user = f'''🎉 BOTBOT đã tìm thấy! 
💌 Bạn đã được mai mối với: *{partner.nickname}*  
📖 Một chút về họ: *{partner.introduce}*  

⏳ {partner.nickname} chỉ mới chờ *{wait_time}*, duyên số đã tìm đến hai bạn trước khi Cupid kịp giương cung! 
✨ Hai bạn có thể *nhắn tin*, *gửi ảnh*, *video*, và *voice* cho nhau.  

👉 *Hãy cùng bắt đầu cuộc trò chuyện ngay nào!* 
        '''
    else:
        text_user = f'''🤖 BOTBOT đã tìm thấy!  
Bạn đã được mai mối với: *{partner.nickname}*  
📖 Một chút về họ: *{partner.introduce}*  

⏳ {partner.nickname} đã đợi bạn *{wait_time}*, có thể họ chưa để ý tin nhắn ngay.  
✨ Gặp nhau là duyên số, hãy kiên nhẫn một chút nhé!  

Hai bạn có thể:  
- Nhắn tin  
- Gửi ảnh  
- Gửi video  
- Gửi voice  

👉 Nếu thấy {partner.nickname} quá lâu không phản hồi, bạn có thể gõ */end* để kết thúc và tìm kiếm người khác.  
Chúc bạn trò chuyện thật vui vẻ!
        '''

    # Send the message to the user
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text_user,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "XEM HÀNG CHỜ",
                            "payload": "MENU_VIEW_QUEUE"
                        },
                        {
                            "type": "postback",
                            "title": "GỢI Ý MỞ LỜI",
                            "payload": "SUGGEST"
                        },
                        {
                            "type": "postback",
                            "title": "CHƠI TRÒ CHƠI",
                            "payload": "GAME"
                        }
                    ]
                }
            }
        }
    }
    out(payload)

    # Construct message for partner
    text_partner = f'''Đã tìm thấy!
Sau {wait_time}, chúng tôi đã tìm được người phù hợp cho bạn, hehe

Bạn đã được mai mối với: {user.nickname}
1 xíu về họ: {user.introduce}\n
Hai bạn có thể gửi ảnh, video và voice cho nhau.\n
Chúc bạn ngon miệng!
'''
    payload = {
        "recipient": {"id": partner.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text_partner,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "GỢI Ý MỞ LỜI",
                            "payload": "SUGGEST"
                        },
                        {
                            "type": "postback",
                            "title": "CHƠI TRÒ CHƠI",
                            "payload": "GAME"
                        }
                    ]
                }
            }
        }
    }
    out(payload)
    send_image(user.id, sticker_found_finder)
    send_image(user.id, sticker_found_waiter)


def postback_feedback(user): #Yêu cầu người dùng feedback về cuộc trò chuyện vừa rồi
    payload= {}
    out(payload)

def postback_confirm_end(user): #Hiện ra khi người dùng muốn end, hỏi lại cho chắc là có muốn rời không?
    # ở đây phải có #END
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Bạn có chắc chắn muốn thoát?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Thoát",
                            "payload": "#END"
                        },
                        {
                            "type": "postback",
                            "title": "Không",
                            "payload": "NOTHING"
                        }
                    ]
                }
            }
        }
    }
    out(payload)

def postback_end_chat(user): #Khi end chat
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Xong 1 hiệp, tiếp phát nữa nhể?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "TÌM MỐI MỚI",
                            "payload": "#AGAIN"
                        },
                        {
                            "type": "postback",
                            "title": "XEM HÀNG CHỜ",
                            "payload": "MENU_VIEW_QUEUE"
                        },
                        {
                            "type": "postback",
                            "title": "VỀ TRANG CHỦ",
                            "payload": "#WELCOME"
                        },
                    ]
                }
            }
        }
    }
    out(payload)
def postback_partner_end(partner_id):
    payload = {
        "recipient": {"id": partner_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Người kia đã bỏ bạn mà ra đi... Thôi thì đổi đào nhỉ?",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "TÌM MỐI MỚI",
                            "payload": "#AGAIN"
                        },
                        {
                            "type": "postback",
                            "title": "XEM HÀNG CHỜ",
                            "payload": "MENU_VIEW_QUEUE"
                        },
                        {
                            "type": "postback",
                            "title": "VỀ TRANG CHỦ",
                            "payload": "#WELCOME"
                        },
                    ]
                }
            }
        }
    }
    out(payload)

def postback_end(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Kết thúc 1 hiệp",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "VỀ TRANG CHỦ",
                            "payload": "#WELCOME"
                        },
                    ]
                }
            }
        }
    }
    out(payload)

def postback_guide(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "text": (
                "🌟 *Hướng dẫn sử dụng Chatbot Hẹn Hò CDA* 🌟\n\n"
                "💡 *1. Nhập thông tin cá nhân:*\n"
                "- ✏️ Nhập nickname: `/nickname <nickname_của_bạn>`\n"
                "- 🖋️ Nhập giới thiệu bản thân: `/gioithieu <giới_thiệu_ngắn_gọn>`\n"
                "- 👤 Chọn giới tính: Nam, Nữ hoặc Bí mật.\n"
                "- 🎯 Chọn gu giới tính bạn muốn làm quen: Nam, Nữ hoặc 'Nhạc nào cũng nhảy'.\n\n"
                "🔍 *2. Bắt đầu tìm kiếm:*\n"
                "- Sau khi nhập đủ thông tin, nhấn nút 'Tìm kiếm' để kết nối với một người phù hợp! 🥰\n\n"
                "⚙️ *3. Tùy chỉnh thông tin cá nhân:*\n"
                "- 🔄 Đổi nickname: `/nickname <nickname_mới>`\n"
                "- 🔄 Đổi giới thiệu: `/gioithieu <giới_thiệu_mới>`\n"
                "- 🔄 Thay đổi gu hoặc giới tính bằng cách chọn lại trong 'Đổi thông tin'.\n\n"
                "💬 *4. Gợi ý mở lời:*\n"
                "- 🗨️ Nhấn 'Gợi ý mở lời' khi không biết cách bắt đầu. Chúng tôi sẽ cung cấp ý tưởng thú vị! 😄\n\n"
                "❌ *5. Kết thúc trò chuyện:*\n"
                "- Nếu không thấy phù hợp, gõ /end hoặc nhấn 'Kết thúc' để tìm kiếm người khác. 🛑\n\n"
                "🔒 *6. Lưu ý & bảo mật:*\n"
                "- 🔐 Khi đang tìm kiếm, bạn sẽ không thể nhấn 'Bắt đầu' lại.\n"
                "- 🔇 Do chưa được sự cấp phép của Facebook, cuộc trò chuyện sẽ chỉ có chức năng gửi tin nhắn, hình ảnh, video và voice.\n"
                "- 🔏 Mọi thông tin cá nhân sẽ được bảo vệ tuyệt đối.\n\n"
                "👉 *Gõ lệnh /lenh để xem danh sách đầy đủ các lệnh.*\n\n"
                "💖 *Chúc bạn tìm được những kết nối thú vị và ý nghĩa!* 💖"
            )
        },
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_introduction(user):
    """Gửi tin nhắn giới thiệu về chatbot."""
    text = (
        f"🎉 Xin chào {user.nickname if user.nickname else 'bạn'}! 🎉\n\n"
        "Chào mừng bạn đến với chatbot Hẹn Hò CDA! Đây là những tính năng nổi bật mà chúng tôi mang lại:\n\n"
        "✨ *Tính năng nổi bật:*\n"
        "💬 *Trò chuyện ẩn danh:* Tìm kiếm những cuộc trò chuyện thú vị và kết nối với những người bạn mới.\n"
        "💡 *Gợi ý câu hỏi thú vị:* Không biết bắt đầu từ đâu? Hãy thử các gợi ý mở đầu cực hay ho của chúng tôi.\n"
        "📅 *Trò chuyện mọi lúc mọi nơi:* Không giới hạn thời gian, bạn có thể sử dụng chatbot 24/7.\n"
        "🔒 *Bảo mật tuyệt đối:* Tất cả thông tin của bạn sẽ được giữ riêng tư.\n\n"
        "👉 Hãy bắt đầu hành trình của bạn ngay bây giờ bằng cách nhấn nút *Bắt đầu* hoặc chọn tính năng mà bạn yêu thích!\n\n"
        "Chúc bạn có trải nghiệm thật tuyệt vời! 😊"
    )

    payload = {
        "recipient": {"id": user.id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_game(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Hiện tại, tính năng này đang trong quá trình hoàn thiện.\nThử lại sau 3/2 nhó.😊"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_view_queue(user): #Xem hàng đợi, toàn là code SQL, nên để anh viết
    print("Wait list after global ", wait_list)
    count_male = 0
    for x in wait_list:
        if (x.gender == "MALE"):
            count_male += 1
    count_male += 3
    count_female = 0
    for x in wait_list:
        if x.gender == "FEMALE":
            count_female += 1
    count_female += 5
    count_bi = 0
    for x in wait_list:
        if x.gender == "BI":
            count_bi += 1
    count_bi += 7
    count_suit = 0
    for x in wait_list:
        if (check_match(user, x)) and (user.id != x.id) :
            count_suit += 1
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": f'''Hiện đang có:
{count_male} Nam
{count_female} Nữ
{count_bi} Bí mật trong hàng chờ

{count_suit} người phù hợp gu của bạn
'''},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_change_info(user): #Nằm ở menu khi người dùng muốn đổi nickname hoặc giới thiệu bản thân
    postback_remind_nickname(user)

#def postback_suggest(user): #Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
#    payload = {
#        "recipient": {"id": user.id},
#        "message": {"text": "Chào bạn, bạn ăn cơm chưa \n Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ ? Nếu không thì cho mình thử nhé :3 \n Trời lạnh như này mình hỏi nhỏ, cậu có cần ai nhắc mặc ấm hong \n Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian của cuộc đời không, vậy nên hãy đền bù bằng cách trò chuyện với tớ hôm nay đi \n Cậu ơi mình đang làm một bài khảo sát : Cậu thích uống trà sữa với đường hay với tớ hơn vậy \n Nay xem tarot người ta bảo tớ nhắn tin với định mệnh mà tình cờ thế nào nay tớ lại nhắn với mỗi cậu nhỉ "},
#        "messaging_type": "RESPONSE"
#    }
#    out(payload)
def postback_suggest(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Trước tiên bạn muốn lựa chọn thả thính dưới phong cách trai hay gái",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Nam",
                            "payload": "SUGGEST_BOY"
                        },
                        {
                            "type": "postback",
                            "title": "Nữ",
                            "payload": "SUGGEST_GIRL"
                        },
                    ]
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_boy(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": (
                        "Bạn chỉ việc nhấn vào nút và văn bản sẽ được chuyển sang cho người được ghép cặp với bạn.\n\n"
                        "1. Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ? "
                        "Nếu không thì cho mình thử nhé 😎✨\n"
                        "2. Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian không? "
                        "Vậy nên đền bù cho tớ bằng cách trò chuyện hôm nay đi! 😏🕒\n"
                        "3. Mình đang làm khảo sát: Bạn thích uống trà sữa với đường hay với mình hơn? "
                        "Đừng chọn sai nhé 😉🧋"
                    ),
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "1. Tự tin, hài hước",
                            "payload": "SUGGEST_BOY_1"
                        },
                        {
                            "type": "postback",
                            "title": "2. Táo bạo, dí dỏm",
                            "payload": "SUGGEST_BOY_2"
                        },
                        {
                            "type": "postback",
                            "title": "3. Dễ thương, vui vẻ",
                            "payload": "SUGGEST_BOY_3"
                        }
                    ]
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_boy1(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ? "
                            "Nếu không thì cho mình thử nhé 😎✨'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Chúc bạn may mắn! 🎉"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ? Nếu không thì cho mình thử nhé 😎✨"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_boy2(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian không? "
                            "Vậy nên đền bù cho tớ bằng cách trò chuyện hôm nay đi! 😏🕒'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Chúc bạn thành công! 💬"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian không? Vậy nên đền bù cho tớ bằng cách trò chuyện hôm nay đi! 😏🕒"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_boy3(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Mình đang làm khảo sát: Bạn thích uống trà sữa với đường hay với mình hơn? "
                            "Đừng chọn sai nhé 😉🧋'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Hy vọng bạn có một khởi đầu tuyệt vời! 🍹"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Mình đang làm khảo sát: Bạn thích uống trà sữa với đường hay với mình hơn? Đừng chọn sai nhé 😉🧋"},
        "messaging_type": "RESPONSE"
    }
    out(payload)


def postback_suggest_girl(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": (
                        "Bạn chỉ việc nhấn vào nút và văn bản sẽ được gửi tới người được ghép cặp.\n\n"
                        "1. Trời lạnh như này, mình hỏi nhỏ, cậu có cần ai nhắc mặc ấm hong? 🧥❄️\n"
                        "2. Nay xem tarot, người ta bảo tớ nhắn tin với định mệnh. "
                        "Tự nhiên tớ lại nhắn với cậu, cậu thấy có hợp lý không? 🔮😌\n"
                        "3. Cậu thích kiểu người nói chuyện thú vị hay đáng yêu hơn? "
                        "Vì mình giỏi cả hai nên hơi phân vân! 😊💬"
                    ),
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "1. Ấm áp, nhẹ nhàng.",
                            "payload": "SUGGEST_GIRL_1"
                        },
                        {
                            "type": "postback",
                            "title": "2. Huyền bí, tinh tế",
                            "payload": "SUGGEST_GIRL_2"
                        },
                        {
                            "type": "postback",
                            "title": "3. Hài hước, đáng yêu.",
                            "payload": "SUGGEST_GIRL_3"
                        }
                    ]
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_girl1(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Trời lạnh như này, mình hỏi nhỏ, cậu có cần ai nhắc mặc ấm hong? 🧥❄️'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Chúc bạn thành công! 🔥"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Trời lạnh như này, mình hỏi nhỏ, cậu có cần ai nhắc mặc ấm hong? 🧥❄️"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_girl2(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Nay xem tarot, người ta bảo tớ nhắn tin với định mệnh. "
                            "Tự nhiên tớ lại nhắn với cậu, cậu thấy có hợp lý không? 🔮😌'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Chúc bạn may mắn! ✨"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Nay xem tarot, người ta bảo tớ nhắn tin với định mệnh. Tự nhiên tớ lại nhắn với cậu, cậu thấy có hợp lý không? 🔮😌"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_suggest_girl3(user):  # Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "🤖 Tin nhắn của bạn: \n\n"
                            "👉 'Cậu thích kiểu người nói chuyện thú vị hay đáng yêu hơn? "
                            "Vì mình giỏi cả hai nên hơi phân vân! 😊💬'\n\n"
                            "✔️ Đã được gửi tới người ghép nối với bạn. Hy vọng cuộc trò chuyện thú vị sẽ bắt đầu! 💬"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
    payload = {
        "recipient": {"id": user.partner_id},
        "message": {"text": "Cậu thích kiểu người nói chuyện thú vị hay đáng yêu hơn? Vì mình giỏi cả hai nên hơi phân vân! 😊💬"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

#def postback_suggest_boy(user):
#    messages = [
#        "Dành cho Nam nè",
#        "1.Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ? Nếu không thì cho mình thử nhé 😎✨",
#        "2.Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian không? Vậy nên đền bù cho tớ bằng cách trò chuyện hôm nay đi! 😏🕒",
#        "3.Mình đang làm khảo sát: Bạn thích uống trà sữa với đường hay với mình hơn? Đừng chọn sai nhé 😉🧋"
#    ]
#    payload = {
#        "recipient": {"id": user.id},
#        "message": {"text": "\n\n".join(messages)},
#        "messaging_type": "RESPONSE"
#    }
#    out(payload)

def postback_send_button(user):
    test_message = "Đây là một tin nhắn test tự động từ chatbot!"
    send_message(user.id, test_message)  # Gửi tin nhắn trước

    payload = {
        "recipient": {"id": user.id},
        "messaging_type": "RESPONSE"
    }
    out(payload)  # Gửi payload nếu cần


def postback_still_chat(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Hãy từ từ để ta có thể tìm hiểu rõ về nhau hơn nhé \n "},
        "messaging_type": "RESPONSE"
    }
    out(payload)

#Postback retry

def postback_retry(user):
    """Kiểm tra thông tin người dùng và chuyển tiếp đến bước tiếp theo nếu đầy đủ."""
    missing_info = []

    # Kiểm tra thiếu nickname
    if user.nickname.startswith("#CDA") or not user.nickname:
        missing_info.append("nickname")

    # Kiểm tra thiếu giới thiệu
    if user.introduce == "Chưa có" or not user.introduce:
        missing_info.append("giới thiệu")

    if missing_info:
        # Hiển thị thông tin còn thiếu
        missing_text = " và ".join(missing_info)
        text = f'''⚠️ Bạn chưa hoàn thiện thông tin. Bạn còn thiếu *{missing_text}*.
📌 Vui lòng nhập thông tin để tiếp tục:

💬 Câu lệnh: /gioithieu giới thiệu ngắn về mình
✨ Ví dụ: `/gioithieu Mình là fan MU 20 năm 🚀`

👉 Hãy hoàn thiện thông tin và bắt đầu kết nối ngay nhé! 💖
'''
        payload = {
            "recipient": {"id": user.id},
            "message": {"text": text}
        }
    else:
        # Nếu đầy đủ, chuyển người dùng sang bước chọn giới tính
        text = "Thông tin của bạn đã đầy đủ! Hãy tiếp tục đến bước chọn giới tính."
        payload = {
            "recipient": {"id": user.id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "CHỌN GIỚI TÍNH",
                                "payload": "#NEXT"
                            }
                        ]
                    }
                }
            }
        }
    out(payload)


#Postback retry

def postback_error(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Bạn đang bị lỗi bất thường do server, vui lòng gõ /end, thoát và sau đó gõ /fix. Cảm ơn"},
        "messaging_type": "RESPONSE"
    }
    out(payload)