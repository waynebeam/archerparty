from flask import Flask
from database import validate_user

app = Flask(__name__)


@app.route('/')
def index():
    return "Archer's Blue's Clues Party!"

@app.route("/invite/<nickname>/<password>")
def show_invite(nickname, password):
  response = validate_user(nickname, password)
  if response:
    return f'Hello {response[0]}!'
  return 'invalid link'
  

app.run(host='0.0.0.0', port=81)
