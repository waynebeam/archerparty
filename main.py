from flask import Flask, redirect, url_for, request
from database import validate_user

app = Flask(__name__)


@app.route('/')
def index():
    return "Archer's Blue's Clues Party!"

@app.route("/invite/<nickname>/<password>")
def show_invite(nickname, password):
  response = validate_user(nickname, password)
  if response:
    name = response[1]
    id = response[0]
    return f'Hello {name}!'
  return redirect(url_for('index'))

@app.post('/rsvp')
def rsvp():
  data = request.form
  id = data['id']
  is_coming = data['rsvp']
  #we get this data from the page form, then here we will pass to the db
  

app.run(host='0.0.0.0', port=81)
