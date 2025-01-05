from db_connection import *
from user import User
from datetime import datetime
from constant import *

wait_list = db_get_all_SEARCH()
print(wait_list)

match_case = {
"MALE - FEMALE": ["FEMALE - MALE", "FEMALE - BI"],
"FEMALE - MALE": ['MALE - FEMALE', 'MALE - BI'],
"MALE - MALE": ['MALE - MALE', 'MALE - BI'],
'FEMALE - FEMALE': ['FEMALE - FEMALE', 'FEMALE - BI'],
'MALE - BI': ['FEMALE - BI','FEMALE - MALE', 'MALE - MALE', 'BI - MALE', 'BI - BI'],
'FEMALE - BI': ['MALE - BI','FEMALE - FEMALE','BI - FEMALE','BI - BI', 'MALE - FEMALE'],
'BI - MALE': ['MALE - BI'],
'BI - FEMALE': ['FEMALE - BI'],
'BI - BI': ['BI - BI', 'MALE - BI', 'FEMALE - BI']
}

user = 1
partner = 2

def check_match(user, partner):
    user_kink = user.gender + " - " + user.partner_gender
    partner_kink = partner.gender + " - " + partner.partner_gender
    # user_kink = "MALE" + " - " + "FEMALE"
    # partner_kink = "FEMALE" + " - " + "FEMALE"

    if(partner_kink in match_case.get(user_kink)):
        return True
    return False

def control_list(user):
    global wait_list
    global match_list
    for x in wait_list:
        if check_match(user, x) & (user.id != x.id):
            wait_list.remove(x)
            return x
    else:
        wait_list.append(user)
        user.last_action_time = datetime.now()
        return None

# print(check_match(user, partner))from db_connection import *
from user import User
from datetime import datetime
from constant import *

wait_list = db_get_all_SEARCH()
print(wait_list)

match_case = {
"MALE - FEMALE": ["FEMALE - MALE", "FEMALE - BI"],
"FEMALE - MALE": ['MALE - FEMALE', 'MALE - BI'],
"MALE - MALE": ['MALE - MALE', 'MALE - BI'],
'FEMALE - FEMALE': ['FEMALE - FEMALE', 'FEMALE - BI'],
'MALE - BI': ['FEMALE - BI','FEMALE - MALE', 'MALE - MALE', 'BI - MALE', 'BI - BI'],
'FEMALE - BI': ['MALE - BI','FEMALE - FEMALE','BI - FEMALE','BI - BI', 'MALE - FEMALE'],
'BI - MALE': ['MALE - BI'],
'BI - FEMALE': ['FEMALE - BI'],
'BI - BI': ['BI - BI', 'MALE - BI', 'FEMALE - BI']
}

user = 1
partner = 2

def check_match(user, partner):
    user_kink = user.gender + " - " + user.partner_gender
    partner_kink = partner.gender + " - " + partner.partner_gender
    # user_kink = "MALE" + " - " + "FEMALE"
    # partner_kink = "FEMALE" + " - " + "FEMALE"

    if(partner_kink in match_case.get(user_kink)):
        return True
    return False

def control_list(user):
    global wait_list
    global match_list
    for x in wait_list:
        if check_match(user, x) & (user.id != x.id):
            wait_list.remove(x)
            return x
    else:
        wait_list.append(user)
        user.last_action_time = datetime.now()
        return None

# print(check_match(user, partner))