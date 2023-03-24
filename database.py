import os
import psycopg2

db_string = os.environ['DB_CONNECTION']

password = os.environ['PASSWORD']

def test_db_access():
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'SELECT * FROM guests'
      curr.execute(sql)
      print(curr.fetchone())

