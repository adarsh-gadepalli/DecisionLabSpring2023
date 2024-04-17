from flask import Flask, render_template, request, redirect, session
from Algorithm import VRP0

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    addresses = {}
    for value in request.form.values():
        key, value = value.split(':') if ':' in value else (value, '')
        addresses[key] = value.strip()

    path = VRP0(addresses)
    addressPath = []
    for p in path:
        addressPath.append(addresses[p])

    session['path'] = addressPath  # Store the path in the session
    return redirect('/map')

@app.route('/map')
def map():
    path = session.get('path', [])
    print(path)
    return render_template('map2.html', path=path)

if __name__ == '__main__':
    app.run(debug=True)
