from flask import Flask, request, render_template, redirect, session, flash
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'logindb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key= "Secret&Safe"
@app.route('/', methods=['GET'])
def index():
 return render_template('lrindex.html')
#this is thelogin route

@app.route('/login', methods=['POST'])
def login():

    # validated as a boolean. if != valid, return "X"; else return(/success)
    #retrieive the info from the form
    print ("success!")
    email = request.form['email_address']
    session['email'] = request.form['email_address']
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    session['password'] = request.form['password']
    print email, pw_hash
    #getting first and last names in session to add to result page
    # name_query
    # the following lines willl be used in the next route. storing here for now.
    #   session['email'] = request.form['email_address']
        # names= mysql.query_db(query)
        # display = names[0]['first_name'] + " " + names[0]['last_name']
    user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = { 'email':request.form['email_address'] }
    user = mysql.query_db(user_query, query_data) # user will be returned in a list
    print user
    if bcrypt.check_password_hash(user[0]['pw_hash'], request.form['password']):
        return redirect('/login/success')
    else:
        flash("incorrect login information")
        return redirect('/')
#on successful login:
@app.route('/login/success', methods=['GET'])
def loginSuccess():
    return render_template('lrsuccess.html')


#this is the registration route
@app.route('/register', methods=['POST'])
def register():
# validated as a boolean. if != valid, return "X"; else return(/success)
    valid = True
    if len(request.form['first_name']) < 2:
        flash("please enter a proper first name")
        valid = False
        print valid
    if not str(request.form['first_name']).isalpha():
        flash("please only use letters in your first name")
        valid = False
        print valid
    if len(request.form['last_name']) < 2:
        flash("please enter a proper last name")
        valid = False
        print valid
    if not str(request.form['first_name']).isalpha():
        flash("please only use letters in your last name")
        valid = False
        print valid
    if len(request.form['email_address']) < 1:
        valid = False
        print valid
        flash("please enter a valid email address")
    if not EMAIL_REGEX.match(request.form['email_address']):
        valid = False
        flash("Please enter a valid email address!")
        print valid
    if len(request.form['password']) <8:
        valid = False
        print valid
        flash("Please enter a password of at least 8 characters")
    if len(request.form['confirm_password']) <8:
        valid = False
        print valid
        flash("Your password submissions do not match")
    if request.form['password'] != request.form['confirm_password']:
        valid = False
        flash("Your password submissions do not match")
    if valid == False:
        print valid
        return redirect('/')
    else:
        # password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        query = '''INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at)
        VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW()) '''
        print str(query)
        data = { "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email" : request.form['email_address'],
        "pw_hash" : pw_hash
        }
        userID = mysql.query_db(query,data)
        print str(userID)
        return redirect('/success/{}'.format(userID))


#this loads the success page for registration
@app.route('/success/<user_id>', methods=['GET'])
def registerSuccess(user_id):
    #this prints the full name of the new user at the top of their result page
    query="SELECT first_name, last_name FROM users ORDER BY id DESC LIMIT 1"
    names= mysql.query_db(query)
    display = names[0]['first_name'] + " " + names[0]['last_name']
    print display
    return render_template('lrsuccess.html'.format(names), names=display, user_id=user_id)


app.run(debug=True)
