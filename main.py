from flask import Flask, redirect, url_for, request, render_template, session
from database import validate_user, get_all_guests, add_invite_to_db,rsvp_to_db
import os
import json
import re

CORRECT_PASSWORD = os.environ['PASSWORD']

base_url = 'https://archerparty.waynebeam.repl.co'

app = Flask(__name__)

app.secret_key = os.environ['FLASK_SECRET_KEY']

@app.route('/')
def index():
  party_info = load_party_info()
  return render_template('index.html', party_info=party_info)

@app.route("/invite/<nickname>/<password>")
def show_invite(nickname, password):
  response = validate_user(nickname, password)
  if response:
    name = response[1]
    id = response[0]
    session['name'] = name
    session['id'] = id
    return render_template("invite-letter.html", name=name, id=id)
  return redirect(url_for('index'))

@app.post('/rsvp')
def rsvp():
  data = request.form
  id = data['id']
  is_coming = False
  if data['rsvp'] == "yes":
    is_coming = True

  rsvp_to_db(id, is_coming)
  session.pop('id')
  session.pop('name')
  return "Thanks!"
  

@app.get('/login')  
def show_login_page():
  return render_template("login.html")

@app.route('/open-letter')
def open_letter():
  if session['id']:
    party_info = load_party_info()
    return render_template("invite.html", name=session['name'], id=session['id'], party_info=party_info)
  return 'bad link'

@app.post('/login')
def login():
  data = request.form
  if data['password'] == CORRECT_PASSWORD:
    session["user"] = "tiff"
    return redirect(url_for('show_guest_list'),)

  return redirect(url_for("show_login_page"))

@app.route('/logout')
def logout():
  if 'user' in session:
    session.pop('user')
  return redirect(url_for("show_login_page"))

@app.route('/guest-list')
def show_guest_list():
  if 'user' in session:
    guests = get_all_guests()
    rsvp_yes = [x for x in guests if x[2] is True]
    rsvp_no = [x for x in guests if x[2] is False]
    rsvp_not_yet = [x for x in guests if x[2] is None]
    party_info = load_party_info()
    return render_template("guestlist.html", rsvp_yes=rsvp_yes, rsvp_no=rsvp_no, rsvp_not_yet=rsvp_not_yet, base_url=base_url, party_info=party_info)
  return redirect(url_for("show_login_page"))

@app.post('/update-party-info')
def update_party_info():
  raw_data = request.form
  data = json.dumps(raw_data)
  with open('party_info.txt', 'w') as f:
    f.write(data)
  return redirect(url_for('show_guest_list'))
  

def load_party_info():
  with open("party_info.txt", 'r') as f:
    data = json.loads(f.read())
    return data

@app.post('/add-invite')
def add_invite():
  data = request.form
  name = data['name']
  nickname = get_nickname(name)
  add_invite_to_db(name,nickname, data['email'])
  return redirect(url_for('show_guest_list'))

def get_nickname(name):
  pattern = r'\w*'
  nickname = name.split()[0]
  nickname = re.search(pattern, name)
  nickname =  nickname.group(0).lower()
  return nickname

app.run(host='0.0.0.0', port=81)


#TODO need to make the party info, and maybe even the guest list(?)
#an API endpoint. Should be easy to do, just need to do it. Also the styling on the invite and main page. Field sets, and the radio buttons. 
#note book always seems pushed to the right. not sure why it doesnt center better. also radios look differwnt on phone and browswer. so careful with the styling. may need to make all containers smaller to fit phone better