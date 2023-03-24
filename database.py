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

def get_all_guests():
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'SELECT name, email, rsvp, nickname, password FROM guests'
      curr.execute(sql)
      response = curr.fetchall()
    
      return response

def add_invite_to_db(name, nickname, email):
  with psycopg2.connect(db_string) as conn:
    with conn.cursor() as curr:
      sql = 'INSERT INTO guests (name, nickname, email) VALUES (%s, %s, %s)'
      curr.execute(sql, [name, nickname, email])


#get_all_guests()