from flask import render_template

from app import app
from database import session
import models

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')