from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "mysecret123"

oauth = OAuth(app)

# Configure GitHub OAuth
github = oauth.register(
    name='github',
    client_id='Ov23li2tUUK3xEPpec4l',
    client_secret='155fa9ef1d91e8da2e25a6b66933ba3249dc9858',

    access_token_url='https://github.com/login/oauth/access_token',

    authorize_url='https://github.com/login/oauth/authorize',

    api_base_url='https://api.github.com/',

    client_kwargs={'scope': 'user:email'},
)

# Login Route
@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

# Callback Route
@app.route('/callback')
def callback():
    token = github.authorize_access_token()

    user = github.get('user').json()

    session['user'] = user

    return redirect('/profile')

# Protected API
@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized", 401

    return f"Welcome, {session.get('user').get('login')} <br> <img src={session.get('user').get('avatar_url')}><img> <br> <a href=/logout>logout<a>"

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return f"You've succesfully logout <br> <a href=/login>login<a>"

# Run Application
if __name__ == '__main__':
    app.run(debug=True)