import pymysql


class DBHelper:

    def __init__(self):
        # self.host = "telechatbot.czm6afi2ciew.ap-southeast-1.rds.amazonaws.com"
        # self.user = "admin"
        # self.password = "1234567
        # self.db = "telechatbot"
        self.host = "localhost"
        self.user = "root"
        self.password = "ZheTao99!"
        self.db = "telebot"
        self.port = 3306
    
    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, 
                                    db=self.db, port=self.port, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result
    
    def fetchall(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        self.con.commit()
        self.__disconnect__()
    
    def get_fullname(self, username):
        sql = "SELECT fullname FROM users WHERE (username) = (%s)"
        var = (username)
        result = self.fetchall(sql, var)
        try:
            return result[0]["fullname"]
        except IndexError:
            return None
    
    def create_fullname(self, username, fullname):
        sql = "INSERT INTO users (username, fullname) VALUES (%s,%s)"
        var = (username, fullname)
        self.execute(sql, var)

    
    def add_phone(self, username, phone):
        sql = "UPDATE users SET contact_no = %s WHERE username = %s"
        var = (phone, username)
        self.execute(sql, var)


    def add_email(self, username, email):
        sql = "UPDATE users SET email = %s WHERE username = %s"
        var = (email, username)
        self.execute(sql, var)

    def get_profile(self,username):
        sql = "SELECT fullname, contact_no, email FROM users WHERE username = %s"
        var = (username)
        result = self.fetch(sql, var)
        return result 

    def update_name_profile(self, username, fullname):
        sql = "UPDATE users SET fullname = %s WHERE username = %s"
        var = (fullname, username)
        self.execute(sql, var)
        
    def update_number_profile(self, username, contact_no):
        sql = "UPDATE users SET contact_no = %s WHERE username = %s"
        var = (contact_no, username)
        self.execute(sql, var)

    def update_email_profile(self, username, email):
        sql = "UPDATE users SET email = %s WHERE username = %s"
        var = (email, username)
        self.execute(sql, var)

    def get_links(self, username):
        sql = "SELECT link, link_description FROM user_links WHERE username = %s"
        var = (username)
        result = self.fetch(sql, var)
        return result
    
    def update_link_description(self, username, link_description):
        sql = "UPDATE user_links SET link_description = %s WHERE (username, link_url) = (%s,%s)"
        var = (username, link_description)
        self.execute(sql, var)
    
    def add_link(self, username, link_description, link_url):
        sql = "INSERT INTO user_links(username, link_description, link) VALUES (%s, %s, %s)"
        var = (username, link_description, link_url)
        self.execute(sql, var)
    
    def edit_link(self, username, link_description, link_url):
        sql = "UPDATE user_links SET link_description = %s, link_url = %s WHERE (username, link_description) = (%s,%s)"
        var = (link_description, link_url, username, link_description)
        self.execute(sql, var)
    
    def get_link_url(self, username, link_description):
        sql = "SELECT link FROM user_links WHERE (username, link_description) = (%s,%s)"
        var = (username, link_description)
        self.execute(sql, var)
    
    def get_qna(self, username):
        sql = "SELECT question, answer FROM user_answers WHERE username = %s"
        var = (username)
        result = self.fetchall(sql, var)
        return result


    


def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts

db = DBHelper()

print(db.get_links("zacgxx"))