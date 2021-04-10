from flask import Flask, render_template, request

app = Flask(__name__)
users = [{'uid': 0} , {'uid': 1} ] 

@app.route('/')
def index():
    return render_template('index.html', users=users)


@app.route('/info', methods=['GET', 'POST'])
def info():
    data = request.get_json() 
    name = data['name']
    return name
