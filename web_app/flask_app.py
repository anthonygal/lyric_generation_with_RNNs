from flask import Flask, request, render_template
from model_interface import writeSomeBars

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html', value='hi')
    if request.method == 'POST':
        artist = request.form['artist']
        first_bar = request.form['first_bar']
    next_bars = writeSomeBars(artist, first_bar)
    return render_template('results.html', next_bars = next_bars)

if __name__ == '__main__':
    app.run(debug=True)
