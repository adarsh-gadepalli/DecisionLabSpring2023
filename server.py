from flask import Flask, render_template, request, redirect
from Algorithm import VRP0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    addresses = dict(request.form)
    path = VRP0(addresses)
    print("VRP Path:", path)  
    return render_template('output.html', path=path)

if __name__ == '__main__':
    app.run(debug=True)
