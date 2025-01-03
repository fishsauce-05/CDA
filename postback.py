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
                            "image_url": "https://cdn.tuoitre.vn/thumb_w/480/471584752817336320/2023/3/5/cau-do-2-16779929961011467051251.jpg",  # Thay thế bằng URL hình ảnh bạn muốn
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
                            "image_url": "https://cdn.tuoitre.vn/thumb_w/480/471584752817336320/2023/3/5/cau-do-1-16779929960982066590826.jpg",  # Thay thế bằng URL hình ảnh bạn muốn
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
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": f'''Bạn chưa có thông tin. Chúng ta cùng nhau thêm thông tin nhé!
Nickname mặc định là: {user.nickname}
Giới thiệu mặc định là: {user.introduce}
Giới thiệu ngắn gọn và gợi chủ đề giúp các bạn không bị bí ý tưởng, dễ bắt chuyện mở lời hơn

Để thay đổi, gõ /nickname và /gioithieu
Ví dụ:
/nickname vì_tinh_tú_97
/gioithieu Cậu có phải là đom đóm không? Tớ thích đom đóm lắm nè

Mỗi tin nhắn chỉ đọc được 1 lệnh duy nhất, đừng viết liền lệnh trong 1 tin nhắn
''',
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
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":'''Đừng quên câu lệnh
/nickname để đổi biệt danh
Ví dụ:
/nickname mai_khanhh

/gioithieu để đổi giới thiệu ngắn về mình nhé!
Ví dụ:
/gioithieu cần người gấp màn hộ, nhiều muỗi mà bung màn ra không bít gấp 🥺
''',
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

def postback_setting(user): #Hiện ra khi người dùng bấm vào (BẮT ĐẦU: payload = #START)
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
                    "text":text,
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


def postback_setgender(user): #Hiện ra để người dùng chọn giới tính
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":"Chọn giới tính của bạn",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Nam",
                            "payload": "#ME_MALE"
                        },
                        {
                            "type": "postback",
                            "title": "Nữ",
                            "payload": "#ME_FEMALE"
                        },
                        {
                            "type": "postback",
                            "title": "Bí mật",
                            "payload": "#ME_BI"
                        },
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

def postback_found(user, partner, wait_time): #Thông báo là đã tìm thấy đối tượng phù hợp, bắt đầu chat
    #nhớ hiện cảnh báo cho user là partner đã đợi được bao lâu và nếu họ không phản hồi thì nên tìm người khác
    text_user = f'''BOTBOT đã tìm thấy!
Bạn đã được mai mối với: {partner.nickname}
1 xíu về họ: {partner.introduce}

{partner.nickname} đã đợi bạn {wait_time} nên có thể họ đang chưa để ý tin nhắn. Gặp nhau là duyên số, hãy kiên nhẫn chút nhé!
Nếu thấy {partner.nickname} quá lâu không phản hồi thì bạn có thể /end và tìm lại.
        '''
    payload = {
        "recipient": {"id": user.id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text":text_user,
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
                    "text":text_partner,
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
        "message": {"text": '''Dễ vãilồn đếo cần hướng dẫn ai cũng biết
1. Mày chọn giới tính, Nam hoặc Nữ hoặc Buêđuê (không chia Bột tôm với Tóp Mỡ)
2. Mày chọn gu mày, Nam hoặc Nữ hoặc Có lỗ là được
3. Tìm kiếm, hợp thì hệ thống nó tự ghép
4. Muốn đổi nickname hoặc about me cho nó ngầu thì dùng:
/nickname hoặc /gioithieu
5. Ngu văn thì ấn vào cái "Gợi ý mở lời" để tao tán hộ cho
6. Tán nhau văn minh lịch sự, bình thường admin không đọc được đâu nhưng gõ /report nó tải tin nhắn về bọn tao đọc được, ban chết cụ mày
7. Không biết nhắn gì nữa thì gõ /end hoặc ấn cái nút ❌KẾT THÚC ở MENU để đổi đào

Muốn biết có những lệnh gì thì ấn /lenh mà đọc
Thi thoảng có mấy câu lệnh hay hay như kiểu /vinhdanh hoặc /thongke thì gõ vào mà nghịch, bọn tao giấu bitcoin trong đấy
'''},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_introduction(user): #Giới thiệu về ứng dụng
    payload= {}
    out(payload)

def postback_view_queue(user): #Xem hàng đợi, toàn là code SQL, nên để anh viết
    count_male = sum(1 for x in wait_list if x.gender == "MALE") + 3
    count_female = sum(1 for x in wait_list if x.gender == "FEMALE") + 5
    count_bi = sum(1 for x in wait_list if x.gender == "BI") + 7
    count_suit = sum(1 for x in wait_list if check_match(user, x) & (user.id != x.id))
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": f'''Hiện đang có:
{count_male} Nam
{count_female} Nữ
{count_bi} Bí mật trong hàng chờ

{count_suit} người phù hợp gu của bạn
Để biết thêm những thông tin thú vị khác, hãy gõ /thongke
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
        "message": {"text": "Hay là mình cứ bất chấp hết yêu nhau đi anh...\nSau các em tự thêm nội dung vào đây, làm thành nhiều cái nút để họ bấm rồi gửi câu văn đi cũng được"},
        "messaging_type": "RESPONSE"
    }
    out(payload)
def postback_still_chat(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Lì ghê ha, redflag 🚩 vậy mà vẫn đâm đầu\n Ngu như chó"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

def postback_error(user):
    payload = {
        "recipient": {"id": user.id},
        "message": {"text": "Bạn đang bị lỗi bất thường do server, vui lòng gõ /end, thoát và sau đó gõ /fix. Cảm ơn"},
        "messaging_type": "RESPONSE"
    }
    out(payload)

