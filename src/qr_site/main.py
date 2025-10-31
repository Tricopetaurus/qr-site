import sys
from pathlib import Path
import random
import string

import qr_site.config as config
from werkzeug.utils import secure_filename

from .logs import get_logger

from flask import Flask, render_template, session, redirect, url_for, request

log = get_logger(__name__)
app = Flask(__name__)


def check_token():
    """Lets a user forward if either of the conditions are met:
     - Access token present in URL, and is accurate
     - Access token present in cookies, and is accurate"""
    access_token = request.args.get('access_token')
    if access_token:
        session['access_token'] = access_token

    if 'access_token' in session:
        return session['access_token'] == config.c.access_token
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['display_name'] = request.form['username']
        # Create a separate variable, username, that's unlikely to hit collision.
        # This will be the one that's actually used for disk.
        session['username'] = f'{request.form['username']}_{get_rand()}'
        session['progress'] = dict()
        return redirect(url_for('index'))

    # GET Case
    else:
        if check_token():
            return render_template('login.html')
        else:
            return redirect(url_for('request_access'))

@app.route('/logout')
def logout():
    # Clear out everything, including the access token.
    # They will need to re-scan the QR Code to get back in.
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if not check_token():
        return redirect(url_for('request_access'))

    if 'username' in session and 'display_name' in session:
        print(session.get('progress'))
        return render_template(
            'index.html',
            name=session['display_name'],
            routes=config.c.routes,
            progress=session.get('progress'),
            upload=request.args.get('upload')
        )
    else:
        return redirect(url_for('login'))

@app.route('/request_access')
def request_access():
    if not check_token():
        return render_template('request_access.html')
    else:
        return redirect(url_for('index'))

def generic_post():
    if not check_token():
        return render_template('request_access.html')

    folder = Path(f'pictures/{request.path}')
    if not folder.exists():
        log.error(f'Folder {folder} does not exist')
        return 404
    if 'username' not in session:
        log.error('User is not logged in!')
        return redirect(url_for('login'))
    safe_user = secure_filename(session['username'])
    user_folder = folder / safe_user
    if not user_folder.exists():
        user_folder.mkdir()

    upload_count = 0
    for category in ['selfie', 'uploaded']:
        files = request.files.getlist(category)
        for file in files:
            if file:
                # prepend a random string to prevent collision
                base_fname = secure_filename(file.filename)
                file.save(user_folder / f'{category}_{get_rand()+base_fname}')
                upload_count += 1

    route = request.path.lstrip('/')
    if route not in session['progress']:
        session['progress'][route] = upload_count
    else:
        session['progress'][route] += upload_count
    session.modified = True

    return redirect(url_for('index', upload='success'))

def get_rand():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def build_routes():
    # We need to loop over the routes in our config
    # Each entry becomes a postable form that eats pictures.
    # Pictures will be stored in pictures/route/user folders.
    for route in config.c.routes:
        folder = Path(f'pictures/{route["route"]}')
        if not folder.exists():
            folder.mkdir(parents=True)
        app.add_url_rule(f'/{route["route"]}', view_func=generic_post, methods=['POST'])

def main(config_file: Path, host: str = '127.0.0.1', port: int = 8080):
    config.load_config(config_file)
    app.secret_key = bytes.fromhex(config.c.secret)
    if not config.is_valid():
        sys.exit(1)
    build_routes()
    app.run(host=host, port=port, debug=True)
