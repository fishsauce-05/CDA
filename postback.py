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
def postback_welcome(user): #Template hiện ra lúc chào đón
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = '''Xin chào bạn đến với sự kiện Crush in Ptit
Sự kiện để cho bạn tìm kiếm có cơ hội tìm tình yêu trong đời mk
H trước tiên, bạn hãy ấn váo nút 3 gạch ngang ở bên tay phải thanh nhắn tin
Tiếp theo, bạn ấn váo nút "BẮT ĐẦU"
'''
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        { #Cục đầu tiên
                            "title": "CHAT ẨN DANH NÀO!",
                            "image_url": "https://scontent.fhan5-9.fna.fbcdn.net/v/t39.30808-6/375596172_876783230787846_2912688737487120703_n.png?_nc_cat=109&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeGnmMGldbXLaqbYyCTKWw_TfBMnLcq6ceR8Eyctyrpx5FfLuPf1Qy6UjaEhe3z71SaXpR4mnzcjBqM9OyL7w3vb&_nc_ohc=MWH29r0qwwoQ7kNvgFWWpGv&_nc_zt=23&_nc_ht=scontent.fhan5-9.fna&_nc_gid=AFjUetjTLuB8729BhuhF1mg&oh=00_AYDyYbWplN_Mm6Efk3h98lHN5CG8DFAoeWSCS3_NI1mtoQ&oe=677F4BED",  # Thay thế bằng URL hình ảnh bạn muốn,
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
                        { #Cục thứ 2
                            "title": "ĐANG CÓ GÌ DIỄN RA VẬY?",
                            "image_url": "https://scontent.fhan5-11.fna.fbcdn.net/v/t39.30808-6/366683630_144682238678402_7554415388400685595_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeHqu4RPoy__AHrnLR4zSs-jsxe4Ibj_YGWzF7ghuP9gZT2ujoYig1dOVKbysTzAjFF0tikNzRg2KYfKWdMwebLM&_nc_ohc=xK7K1Orii7wQ7kNvgFYHCQ-&_nc_zt=23&_nc_ht=scontent.fhan5-11.fna&_nc_gid=AG4J78jvFXawC_d58gFyLEo&oh=00_AYC66JN2HGV26-i9Gr0CTnAAPB-Qfv4ATgVsixr8SBtLow&oe=677F59C2", # Thay thế bằng URL hình ảnh bạn muốn,
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
                        { #Cục thứ 3
                            "title": "ALO, TÔI NGHE",
                            "image_url": "https://bibungbia.pythonanywhere.com/assets/fire.png",  # Thay thế bằng URL hình ảnh bạn muốn
                            "buttons": [
                                {
                                    "type":"web_url",
                                    "title": "Báo lỗi",
                                    "url":"https://www.messenger.com/t/226475877409994"
                                },
                                {
                                    "type": "web_url",
                                    "title": "Liên hệ admin",
                                    "payload": "https://www.messenger.com/t/226475877409994"
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
    out(payload)

def postback_first_come(user):
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = f'''Bạn chưa nhập đủ thông tin. Vui lòng thêm thông tin để tiếp tục:
Nickname hiện tại: {user.nickname if user.nickname else 'Chưa nhập'}
Giới thiệu hiện tại: {user.introduce if user.introduce else 'Chưa nhập'}

Để thay đổi, gõ /nickname và /gioithieu
Ví dụ:
/nickname vì_tinh_tú_97
/gioithieu Cậu có phải là đom đóm không? Tớ thích đom đóm lắm nè
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
        text = f'''Nickname hiện tại: {user.nickname}
Giới thiệu hiện tại: {user.introduce}

Bạn đã sẵn sàng tiếp tục!
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


def postback_remind_nickname(user):
    if user.nickname.startswith("#CDA") or user.introduce == "Chưa có" or user.nickname == "" or user.introduce == "":
        text = '''Bạn chưa nhập đủ thông tin cần thiết.
Vui lòng nhập:
/nickname để đổi biệt danh
Ví dụ: /nickname mai_khanhh

/gioithieu để giới thiệu ngắn về mình
Ví dụ:
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
        text = '''Bạn chưa nhập đủ thông tin. Vui lòng nhập thông tin trước khi tiếp tục.
Câu lệnh:
/nickname để đổi biệt danh
/gioithieu để giới thiệu ngắn về mình
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
                gender = 'Nam'
            case 'FEMALE':
                gender = 'Nữ'
            case 'BI':
                gender = 'Bí mật'
        match user.partner_gender:
            case 'MALE':
                partner = 'Nam'
            case 'FEMALE':
                partner = 'Nữ'
            case 'BI':
                partner = 'Nhạc nào cũng nhảy'

        text = f'''Nickname của bạn: {user.nickname}
Giới tính bạn chọn: {gender}
Gu bạn chọn: {partner}
Giới thiệu ngắn gọn: '{user.introduce}'
Bạn có muốn thay đổi hay tìm kiếm luôn?
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
                        {"type": "postback", "title": "Nam", "payload": "#ME_MALE"},
                        {"type": "postback", "title": "Nữ", "payload": "#ME_FEMALE"},
                        {"type": "postback", "title": "Bí mật", "payload": "#ME_BI"}
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
                            "title": "Nam",
                            "payload": "#YOU_MALE"
                        },
                        {
                            "type": "postback",
                            "title": "Nữ",
                            "payload": "#YOU_FEMALE"
                        },
                        {
                            "type": "postback",
                            "title": "Nhạc nào cũng nhảy",
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
                    "text": "BOTBOT đang tìm kiếm...\nĐợi chút nhé",
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

def postback_found(user, partner, wait_time):
    #Code ne
    diff = datetime.now() - partner.last_action_time if partner.last_action_time else timedelta(seconds=0)
    wait_seconds = diff.total_seconds()  #Thay time

    #dk
    if wait_seconds < 60:
        text_user = f'''BOTBOT đã tìm thấy!
Bạn đã được mai mối với: {partner.nickname}
1 xíu về họ: {partner.introduce}

{partner.nickname} chỉ mới chờ {wait_time}, duyên số tìm đến 2 bạn trước khi cupid kịp giương cung rồi đó!
Hãy cùng bắt đầu cuộc trò chuyện ngay nào!
        '''
    else:
        text_user = f'''BOTBOT đã tìm thấy!
Bạn đã được mai mối với: {partner.nickname}
1 xíu về họ: {partner.introduce}

{partner.nickname} đã đợi bạn {wait_time} nên có thể họ đang chưa để ý tin nhắn. Gặp nhau là duyên số, hãy kiên nhẫn chút nhé!
Nếu thấy {partner.nickname} quá lâu không phản hồi thì bạn có thể /end và tìm lại.
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
1 xíu về họ: {user.introduce}

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
                        }
                    ]
                }
            }
        }
    }
    out(payload)


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
        "message": {"text": '''Đơn giản thôi không có gì khó khăn với bạn đâu
1. Đầu tiên, bạn hãy lựa chọn giới tính của bản thân(giới tính mà tâm hồn bạn đang mang)
2. Tiếp theo, bạn hãy chọn gu giới tính người bạn muốn làm quen
3. Sau đó, bạn ấn tìm kiếm để chúng tôi có thể giúp bạn gặp được người phù hợp với mong muốn của bạn
4. Nếu bạn muốn đổi nickname hoặc giới thiệu bản thân thì hãy dùng:
/nickname hoặc /gioithieu  nhé !
5. Nếu không biết phải mở lời với đối phương như nào hay trong tình trạng hết văn thì hãy ấn vào "Gợi ý mở lời", chúng tôi sẽ giúp đỡ bạn một phần nào đấy để các bạn có thể dễ dàng tiếp cận nhau hơn :3
6. Nếu cảm thấy đối phương không phù hợp với bản thân và muốn kết thúc cuộc trò chuyện thì hãy gõ /end hoặc ấn cái nút ❌KẾT THÚC ở MENU  để  kết thúc ccâu chuyện với người đó và có thể tiếp tục tìm kiếm những người phù hợp với mong muốn  của bạn

Hãy gõ /lenh để hiển thị tất cả những câu lệnh bạn có thể sử dụng
'''},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_introduction(user): #Giới thiệu về ứng dụng
    payload= {}
    out(payload)

def initiate_reply(user, message_id):
    """Yêu cầu người dùng nhập nội dung phản hồi."""
    user.temp_message_id = message_id  # Lưu ID tin nhắn tạm thời
    update_temp_message_id(user.id, message_id)  # Lưu vào database (nếu cần)
    send_message(user.id, "Vui lòng nhập nội dung phản hồi của bạn:")



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
    count_suit += 3
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
    #gõ /nickname để đổi biệt danh
    # /gioithieu để đổi giới thiệu về bạn
    # /gioitinh Nam, Nu, Bi để đổi giới tính
    # /gu Nam, Nu, Bi để đổi gu:
    payload= {}
    out(payload)

def postback_suggest(user): #Hiện ra khi người dùng muốn gợi ý văn để bắt chuyện
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Chào bạn, bạn ăn cơm chưa \n Bạn ơi, bộ luật mới có quy định nào cấm làm quen với người dễ thương không nhỉ ? Nếu không thì cho mình thử nhé :3 \n Trời lạnh như này mình hỏi nhỏ, cậu có cần ai nhắc mặc ấm hong \n Cậu có biết là để nghĩ cách bắt chuyện với cậu tớ mất bao nhiêu thời gian của cuộc đời không, vậy nên hãy đền bù bằng cách trò chuyện với tớ hôm nay đi \n Cậu ơi mình đang làm một bài khảo sát : Cậu thích uống trà sữa với đường hay với tớ hơn vậy \n Nay xem tarot người ta bảo tớ nhắn tin với định mệnh mà tình cờ thế nào nay tớ lại nhắn với mỗi cậu nhỉ "},
        "messaging_type": "RESPONSE"
    }
    out(payload)
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
        text = f'''Bạn chưa hoàn thiện thông tin. Bạn còn thiếu {missing_text}.
Vui lòng nhập:
- /nickname để đổi biệt danh
- /gioithieu để giới thiệu ngắn về mình
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