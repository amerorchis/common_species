from flask import Flask
from gen_html import html

app = Flask(__name__)

@app.route('/')
def display_species_list():
    return html()
