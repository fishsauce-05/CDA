from user import User
from db_connection import *
from postback import *
from handle_waitlist import *
from datetime import datetime, timedelta
from constant import *


state_postback = { #MU vo dich nhe anh em
    'WELCOME':          ['#WELCOME', '#START', 'MENU_INTRODUCTION', 'MENU_GUIDE', 'MENU_VIEW_QUEUE', '#RETRY', '#END'],
    'SETTING':          ['#CHANGE', '#SEARCH', '#NEXT', '#RETRY', '#WELCOME', '#END'],
    'SET_GENDER':       ['#ME_MALE', '#ME_FEMALE', '#ME_BI', '#RETRY', '#END'],
    'PARTNER_GENDER':   ['#YOU_MALE', '#YOU_FEMALE', '#YOU_BI', '#CONFIRM_INFO', '#RETRY', '#END'],
    'SEARCH':           ['#SEARCH', '#STOP_SEARCH', '#RETRY', '#END'],
    'MATCH':            ['#AGREE', '#DISAGREE'],  # Tạm thời bỏ
    'AGREED':           [],  # Tạm thời bỏ
    'REFUSED':          [],  # Tạm thời bỏ
    'TALK':             ['#KEEP', '#CONFIRM_END', '#RETRY', '#END'],
    'END':              ['#WELCOME', '#START', '#FEEDBACK', '#AGAIN', '#RETRY', '#END'],
}



def handle_postback(user, payload, users):
    """Xử lý các hành động postback."""
    if payload.startswith('#'):
        if payload in state_postback.get(user.state):
            return_postback(user, payload, users)
        else:
            payload = {
            "recipient": {"id": user.id},
            "message": {"text": "Payload không có trong state"},
            "messaging_type": "RESPONSE"
            }
            out(payload)
    else:
        return_postback(user, payload, users)



def return_postback(user, payload, users):
    if payload.startswith('#'):
        match payload:
            case '#WELCOME':
                user.state = 'WELCOME'
                postback_welcome(user) #vào welcome
            case '#RETRY':
                postback_retry(user)
            case '#START':
                if (user.gender != "") & (user.partner_gender != ""):
                    user.state = 'SETTING'
                    update_state(user.id, user.state)
                    postback_setting(user)
                else:
                    postback_first_come(user)
                    user.state = 'SETTING'
                    update_state(user.id, user.state)

            case '#NEXT':
                user.state = 'SET_GENDER'
                update_state(user.id, user.state)
                postback_setgender(user)

            case '#CHANGE':
                #kiểm tra xem có trong hàng chờ không, có thì cút
                # if user.id in list_wait:
                #     list_wait.remove(user.id)
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_remind_nickname(user)

            case '#ME_MALE':
                user.gender = 'MALE'
                update_gender(user.id,'MALE')
                user.state = 'PARTNER_GENDER'
                update_state(user.id, user.state)
                postback_partnergender(user)

            case '#ME_FEMALE':
                user.gender = 'FEMALE'
                update_gender(user.id,'FEMALE')
                user.state = 'PARTNER_GENDER'
                update_state(user.id, user.state)
                postback_partnergender(user)

            case '#ME_BI':
                user.gender = 'BI'
                update_gender(user.id,'BI')
                user.state = 'PARTNER_GENDER'
                update_state(user.id, user.state)
                postback_partnergender(user)

            case '#YOU_MALE':
                user.partner_gender = 'MALE'
                update_partner_gender(user.id, 'MALE')
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_setting(user)

            case '#YOU_FEMALE':
                user.partner_gender = 'FEMALE'
                update_partner_gender(user.id, 'FEMALE')
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_setting(user)

            case '#YOU_BI':
                user.partner_gender = 'BI'
                update_partner_gender(user.id, 'BI')
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_setting(user)

            # case '#WAIT':
            #     #xử lý sau đi
            #     print('in wait')
            case '#STOP_SEARCH':
                if user in wait_list:
                    wait_list.remove(user)
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_setting(user)
            case '#SEARCH':
                postback_search(user)
                user.state = 'SEARCH'
                update_state(user.id, user.state)
                partner = control_list(user)
                if partner != None: #nếu trả về partner hợp lệ
                    user.partner_id = partner.id
                    partner.partner_id = user.id
                    #1. Tính thời gian người trước đã đợi
                    wait_time = "7749 kiếp"
                    if partner.last_action_time:
                        if isinstance(partner.last_action_time, str):
                            # Chuyển chuỗi datetime có micro giây thành datetime object
                            partner.last_action_time = datetime.strptime(partner.last_action_time, '%Y-%m-%d %H:%M:%S.%f')

                        # Tính toán sự khác biệt thời gian
                        diff = datetime.now() - partner.last_action_time

                        # Chuyển đổi sang ngày, giờ, phút, giây
                        days = diff.days
                        seconds = diff.total_seconds()
                        hours = int(seconds // 3600 % 24)
                        minutes = int(seconds // 60 % 60)
                        remaining_seconds = int(seconds % 60)


                        # Định dạng chuỗi kết quả
                        if days > 0:
                            wait_time = f"{days} ngày, {hours} giờ, {minutes} phút"
                        elif hours > 0:
                            wait_time = f"{hours} giờ, {minutes} phút"
                        else:
                            wait_time = f"{minutes} phút, {remaining_seconds} giây"

                    postback_found(user, partner, wait_time)

                    #Đặt state của cả 2 là TALK
                    user.state = 'TALK'
                    partner.state = 'TALK'

                    #Update state lên cơ sở dữ liệu
                    update_state(user.id, user.state)
                    update_state(partner.id, partner.state)

                    #Update partner_id của cả 2 người


                    #Update partner_id lên cơ sở dữ liệu
                    update_partner_id(user.id,partner.id)
                    update_partner_id(partner.id,user.id)

                    partner.last_action_time = ""
                    user.last_action_time = ""

            # case '#AGREE':
            #     user.state = 'AGREED'
            #     #kiểm tra state đối phương
            #     if partner.state == 'AGREED':
            #         user.state = 'TALK'
            #         partner.state = 'TALK'
            #         postback_talk() #gửi cho cả 2
            #     else:
            #         pass
            #         #wait

            # case '#DISAGREED':
            #     user.state = 'END'
            #     partner.state = 'SEARCH'
            #     postback_end(user)
            #     postback_refused(partner)
            case '#END':
                if user in wait_list:
                    wait_list.remove(user)
                if user.state == 'TALK':
                    if users.get(user.partner_id) != "":
                        partner = users.get(user.partner_id)
                        postback_end_chat(user)
                        postback_partner_end(user.partner_id)
                        update_partner_id(user.partner_id, "")
                        update_partner_id(user.id, "")
                        # postback_feedback(user)

                        partner.state = 'END'
                        update_state(partner.id, partner.state)
                    else:
                        postback_error(user)

                else:
                    postback_end(user)
                user.state = 'END'
                update_state(user.id, user.state)

            case '#AGAIN':
                user.state = 'SETTING'
                update_state(user.id, user.state)
                postback_setting(user)



    # Những cái không liên quan đến state
    else:
        match payload:
            case 'MENU_END' | 'Minh muon thoat':
                postback_confirm_end(user) #ở đây phải có #END
            case 'MENU_INTRODUCTION':
                postback_introduction(user)
            case 'MENU_GUIDE'|'677740b1-<5309-?4ed7->a884-?4dc412535a98->Huong dan':
                postback_guide(user)
            case 'MENU_VIEW_QUEUE':
                postback_view_queue(user)
            case 'MENU_CHANGE_INFO':
                postback_change_info(user) #gõ /nickname để đổi biệt danh, /gioithieu để đổi giới thiệu về bạn, /gioitinh Nam, Nu, Bi để đổi giới tính, /gu Nam, Nu, Bi để đổi gu
            case 'SUGGEST':
                postback_suggest(user) #gNoợi ý những câu mở đầu
            case 'NOTHING':
                postback_still_chat(user)