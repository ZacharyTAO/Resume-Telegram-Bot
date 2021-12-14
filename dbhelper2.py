import pymysql


class DBHelper:

    def __init__(self):
        # self.host = "telechatbot.czm6afi2ciew.ap-southeast-1.rds.amazonaws.com"
        # self.user = "admin"
        # self.password = "1234567
        # self.db = "telechatbot"
        self.host = "localhost"
        self.user = "root"
        self.password = ""
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

