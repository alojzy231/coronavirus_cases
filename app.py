import os
from flask import Flask, render_template, url_for, request, redirect, send_from_directory
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/' + request.form['country'])
    else:
        return render_template('index.html')


@app.route('/<country>')
def country(country):
    URL = f'https://www.worldometers.info/coronavirus/country/{country.lower()}/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div', class_="maincounter-number")

    if not results:
        return "You have passed wrong name of a country."
    else:
        coronavirus_cases = results[0].span.text
        deaths = results[1].span.text
        recovered = results[2].span.text

        return render_template('country.html', country=country.upper(), coronavirus_cases=coronavirus_cases, deaths=deaths, recovered=recovered)

@app.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()