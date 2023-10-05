from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "REPLACE ME LATER"


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/newuser', methods=["POST"])
def register_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('A user with that email already exists. Please try again.')
    else:
        db.session.add(crud.create_user(email, username, password))
        db.session.commit()
        flash('Account successfully created!')

    return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        if password == user.password:
            session['user'] = user.user_id
            flash('Logged in!')
            # making sure user id is stored in session
            print(session['user'])
            return redirect('/')
        else: 
            flash('Your login credentials are incorrect. Please try again.')
            return redirect('/')
    else:
        flash('Your login credentials are incorrect. Please try again.')
        return redirect('/')







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=False)