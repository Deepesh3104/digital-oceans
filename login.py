from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a random secret key

# Mongo DB connnection Strings
connection_string = "mongodb+srv://Deepesh2104:Deepesh2228@cluster0.7mgj9te.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.get_database('Deepesh2104')  # Database name 
users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        else:
            return render_template('login1.html', error='Invalid credentials')

    return render_template('login1.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return render_template('register.html', error='Email already exists')

        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password
        }
        users_collection.insert_one(user_data)

        return redirect(url_for('login1'))

    return render_template('login1.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login1.html'))

if __name__ == '__main__':
    app.run(debug=True)
