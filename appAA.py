from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

#dashboard route
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

#Sign Up route
@app.route('/sign_up')
def signUp():
    return render_template('sign_up.html')

#Login route
@app.route('/login', methods=['GET', 'POST'])
def welcome():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            #not currently working - should redirect to dashboard page on submit
            return redirect(url_for('dashboard'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
