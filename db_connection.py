import pymysql
from user import User
from constant import *
# Hàm tạo kết nối đến cơ sở dữ liệu MySQL
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=host_db,
            user=user_db,
            password=pass_db,
            database=data_db
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        return None

def check_and_add_user(user_id):
    """
    Kiểm tra xem người dùng đã có trong cơ sở dữ liệu chưa.
    Nếu chưa, thêm người dùng vào với trạng thái mặc định.
    """
    conn = get_db_connection()
    if not conn:
        return "Database connection failed."

    try:
        cursor = conn.cursor()
        # Kiểm tra xem user đã tồn tại chưa
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()

        if not result:  # Nếu user chưa tồn tại
            default_state = "Welcome"  # Trạng thái mặc định
            cursor.execute(
                "INSERT INTO users (id, state, partner_id) VALUES (%s, %s, %s)",
                (user_id, default_state, None)
            )
            conn.commit()
            return f"User {user_id} added with state {default_state}."
        else:
            return f"User {user_id} already exists."
    except pymysql.MySQLError as e:
        print(f"Database query error: {e}")
        return "Error during database operation."
    finally:
        conn.close()

def get_user_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, state, partner_id FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(row[0],row[1],row[2])
    return None

def save_user_to_db(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id) VALUES (%s, %s, %s,%s,%s, %s, %s, %s, %s, %s)",
        (user.id, user.state, user.partner_id, user.nickname, user.gender, user.partner_gender, user.introduce, user.last_action_time, user.previous_id, user.blocks_id))
    conn.commit()
    conn.close()

# Hàm cập nhật trạng thái (state)
def update_state(user_id, new_state):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET state = %s WHERE id = %s"
            cursor.execute(sql, (new_state, user_id))
            conn.commit()
            print(f"State updated to {new_state} for user {user_id}.")
        except Exception as e:
            print(f"Error updating state: {e}")
        finally:
            conn.close()

# Hàm cập nhật partner_id
def update_partner_id(user_id, partner_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET partner_id = %s WHERE id = %s"
            cursor.execute(sql, (partner_id, user_id))
            conn.commit()
            print(f"Partner ID updated to {partner_id} for user {user_id}.")
        except Exception as e:
            print(f"Error updating partner ID: {e}")
        finally:
            conn.close()

# Hàm cập nhật nickname
def update_nickname(user_id, nickname):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET nickname = %s WHERE id = %s"
            cursor.execute(sql, (nickname, user_id))
            conn.commit()
            print(f"Nickname updated to {nickname} for user {user_id}.")
        except Exception as e:
            print(f"Error updating nickname: {e}")
        finally:
            conn.close()

# Hàm cập nhật giới tính (gender)
def update_gender(user_id, gender):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET gender = %s WHERE id = %s"
            cursor.execute(sql, (gender, user_id))
            conn.commit()
            print(f"Gender updated to {gender} for user {user_id}.")
        except Exception as e:
            print(f"Error updating gender: {e}")
        finally:
            conn.close()

# Hàm cập nhật giới tính đối tượng (partner_gender)
def update_partner_gender(user_id, partner_gender):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET partner_gender = %s WHERE id = %s"
            cursor.execute(sql, (partner_gender, user_id))
            conn.commit()
            print(f"Partner gender updated to {partner_gender} for user {user_id}.")
        except Exception as e:
            print(f"Error updating partner gender: {e}")
        finally:
            conn.close()

# Hàm cập nhật giới thiệu (introduce)
def update_introduce(user_id, introduce):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET introduce = %s WHERE id = %s"
            cursor.execute(sql, (introduce, user_id))
            conn.commit()
            print(f"Introduce updated to {introduce} for user {user_id}.")
        except Exception as e:
            print(f"Error updating introduce: {e}")
        finally:
            conn.close()

def update_last_action_time(user_id, last_action_time):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET last_action_time = %s WHERE id = %s"
            cursor.execute(sql, (last_action_time, user_id))
            conn.commit()
            print(f"Introduce updated to {last_action_time} for user {user_id}.")
        except Exception as e:
            print(f"Error updating last_action_time: {e}")
        finally:
            conn.close()

def update_previous_id(user_id, previous_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET previous_id = %s WHERE id = %s"
            cursor.execute(sql, (previous_id, user_id))
            conn.commit()
            print(f"Introduce updated to {previous_id} for user {user_id}.")
        except Exception as e:
            print(f"Error updating previous_id: {e}")
        finally:
            conn.close()

def update_blocks_id(user_id, blocks_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET blocks_id = %s WHERE id = %s"
            cursor.execute(sql, (blocks_id, user_id))
            conn.commit()
            print(f"Introduce updated to {blocks_id} for user {user_id}.")
        except Exception as e:
            print(f"Error updating blocks_id: {e}")
        finally:
            conn.close()


def get_all_users():
    conn = get_db_connection()
    users_dict = {}
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id FROM users"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                user_id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id = row
                users_dict[user_id] = User(
                    id=user_id,
                    state=state,
                    partner_id=partner_id,
                    nickname=nickname,
                    gender=gender,
                    partner_gender=partner_gender,
                    introduce=introduce,
                    last_action_time = last_action_time,
                    previous_id = previous_id,
                    blocks_id = blocks_id
                )
            print(f"Loaded {len(users_dict)} users from the database.")
        except Exception as e:
            print(f"Error fetching users: {e}")
        finally:
            conn.close()
    return users_dict

def is_nickname_exists(nickname):
    try:
            # Kết nối cơ sở dữ liệu
        conn = pymysql.connect(
                host=host_db,
                user=user_db,
                password=pass_db,
                database=data_db
        )
        with conn.cursor() as cursor:
            # Truy vấn nickname
            sql = "SELECT COUNT(*) AS count FROM users WHERE nickname = %s"
            cursor.execute(sql, (nickname,))
            result = cursor.fetchone()
            return result[0] > 0
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def db_get_all_SEARCH():
    """
    Truy vấn tất cả người dùng có state là 'SEARCH' từ bảng users.
    :return: List chứa thông tin người dùng có state là 'SEARCH'.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Truy vấn tất cả người dùng có state là 'SEARCH'
            query = "SELECT id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id FROM users WHERE state = %s"
            cursor.execute(query, ("SEARCH",))
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành list
            users = []
            for row in result:
                user_id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id = row
                user = User(
                    id=user_id,
                    state=state,
                    partner_id=partner_id,
                    nickname=nickname,
                    gender=gender,
                    partner_gender=partner_gender,
                    introduce=introduce,
                    last_action_time = last_action_time,
                    previous_id = previous_id,
                    blocks_id = blocks_id
                )
                users.append(user)

            return users
    except Exception as e:
        print(f"Error retrieving users in state 'SEARCH': {e}")
        return []
    finally:
        connection.close()

def db_get_all_MATCH():
    """
    Truy vấn tất cả người dùng có state là 'SEARCH' từ bảng users.
    :return: List chứa thông tin người dùng có state là 'SEARCH'.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Truy vấn tất cả người dùng có state là 'SEARCH'
            query = "SELECT id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id FROM users WHERE state = %s"
            cursor.execute(query, ("TALK",))
            result = cursor.fetchall()

            # Chuyển đổi kết quả thành list
            users = []
            for row in result:
                user_id, state, partner_id, nickname, gender, partner_gender, introduce, last_action_time, previous_id, blocks_id = row
                user = User(
                    id=user_id,
                    state=state,
                    partner_id=partner_id,
                    nickname=nickname,
                    gender=gender,
                    partner_gender=partner_gender,
                    introduce=introduce,
                    last_action_time = last_action_time,
                    previous_id = previous_id,
                    blocks_id = blocks_id
                )
                users.append(user)

            return users
    except Exception as e:
        print(f"Error retrieving users in state 'SEARCH': {e}")
        return []
    finally:
        connection.close()

def update_last_action_time(user_id):
    """
    Cập nhật mốc thời gian thực hiện tác vụ cuối cùng cho một người dùng.
    :param user_id: ID của người dùng
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Lấy thời gian hiện tại
            current_time = datetime.now()

            # Cập nhật thời gian vào bảng users
            query = """
                UPDATE users
                SET last_action_time = %s
                WHERE id = %s
            """
            cursor.execute(query, (current_time, user_id))
            connection.commit()
            print(f"Updated last_action_time for user {user_id} to {current_time}.")
    except Exception as e:
        print(f"Error updating last_action_time for user {user_id}: {e}")
    finally:
        connection.close()

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE IF EXISTS users;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            state VARCHAR(255) NOT NULL,
            partner_id VARCHAR(255),
            nickname VARCHAR(255),
            introduce VARCHAR(255),
            gender VARCHAR(255),
            partner_gender VARCHAR(255),
            last_action_time VARCHAR(255),
            previous_id VARCHAR(255),
            blocks_id VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ''')
    conn.commit()
    conn.close()

# Gọi hàm để tạo bảng
create_users_table()