from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/display.html')
def display():
    places = request.args.getlist('place')
    return render_template('display.html', places=places)

if __name__ == '__main__':
    app.run(debug=True, port = 5002)