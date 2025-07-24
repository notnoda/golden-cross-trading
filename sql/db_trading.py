import psycopg2

class DbTrading:
    def __init__(self, password):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="trading",
                user="trading",
                password=password
            )

            print(f"PostgreSQL 연결 성공")
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"PostgreSQL 연결 오류: {e}")
            exit()

    def fetchone(self, query, vars=None):
        try:
            self.cursor.execute(query, vars)
            print(f"데이터 조회 성공 (fetchone)")
            dataset = self.cursor.fetchone()
            return dataset
        except psycopg2.Error as e:
            print(f"데이터 조회 오류 (fetchone): {e}")
            return None

    def fetchmany(self, query, vars=None, size=1):
        try:
            self.cursor.execute(query, vars)
            print(f"데이터 조회 성공 (fetchmany)")
            dataset = self.cursor.fetchmany(size)
            return dataset
        except psycopg2.Error as e:
            print(f"데이터 조회 오류 (fetchmany): {e}")
            return None

    def fetchall(self, query, vars=None):
        try:
            self.cursor.execute(query, vars)
            print(f"데이터 조회 성공 (fetchall)")
            dataset = self.cursor.fetchall()
            return dataset
        except psycopg2.Error as e:
            print(f"데이터 조회 오류 (fetchall): {e}")
            return None

    def execute(self, query, vars):
        try:
            self.cursor.execute(query, vars)
            self.connection.commit()
            print("데이터 삽입 성공 (execute)")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"데이터 삽입 오류 (execute): {e}")
            return False

    def executemany(self, query, vars):
        try:
            self.cursor.executemany(query, vars)
            self.connection.commit()
            print("데이터 삽입 성공 (executemany)")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"데이터 삽입 오류 (executemany): {e}")
            return False

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("데이터 종료 성공")
        except psycopg2.Error as e:
            print(f"데이터 종료 오류: {e}")

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test start")
    database = DbTrading("root123")
    data = database.fetchall("select name, nickname from sample")
    database.close()
    print(data)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test end")
