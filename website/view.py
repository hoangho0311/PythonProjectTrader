from flask import Blueprint, render_template
from .database import mydb

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
