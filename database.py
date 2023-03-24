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
  if password != correct_password:
    return False
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'SELECT name FROM guests WHERE nickname = %s'
      curr.execute(sql, [nickname])
      return curr.fetchone()

print(validate_user("wayne", "archparty")[0])