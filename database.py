import os
import psycopg2

db_string = os.environ['DB_CONNECTION']

correct_password = os.environ['PASSWORD']

def test_db_access():
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'SELECT * FROM guests'
      curr.execute(sql)
      print(curr.fetchone())


def validate_user(nickname, password):
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'SELECT id, name, password FROM guests WHERE nickname = %s'
      curr.execute(sql, [nickname])
      response = curr.fetchone()
      if not response:
        return False
      if response[2] == password:
        return response
      return False

print(validate_user("wayne", "e9d05fa6-c315-462a-b2cf-254b046bfbe1"))