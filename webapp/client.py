from flask import Flask, render_template, request, url_for

app = Flask(__name__)
users = [{'uid': 0} , {'uid': 1} ] 
h = 0 
@app.route('/')
def index():
    menu = ['signup']
    return render_template('index.html', menu=menu)

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')



@app.route('/info', methods=['GET', 'POST'])
def info():
    data = request.get_json() 
    name = data['name'] 
    name += str(h)
    return name
