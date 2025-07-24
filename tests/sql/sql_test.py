import psycopg2

def getConnection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="trading",
            user="trading",
            password="root123"
        )
        return connection
    except psycopg2.Error as e:
        print(f"PostgreSQL 연결 오류: {e}")
        exit()

def insert(connection, cursor):
    try:
        sql = "INSERT INTO sample (name, nickname) VALUES (%s, %s)"
        values = ("data1", "data2")
        cursor.execute(sql, values)
        connection.commit()
        print("데이터 삽입 성공 (단일 행)")
    except psycopg2.Error as e:
        print(f"데이터 삽입 오류: {e}")
        connection.rollback()

def close(connection, cursor):
    try:
        cursor.close()
        connection.close()
        print("데이터 종료 성공")
    except psycopg2.Error as e:
        print(f"데이터 종료 오류: {e}")

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test start")
    connection = getConnection()
    cursor = connection.cursor()
    insert(connection, cursor)
    close(connection, cursor)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test end")
