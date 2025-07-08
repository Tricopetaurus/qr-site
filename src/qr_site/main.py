import sys
from pathlib import Path

import qr_site.config as config
from werkzeug.utils import secure_filename

from .logs import get_logger

from flask import Flask, render_template, session, redirect, url_for, request

log = get_logger(__name__)
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' in session:
        return render_template(
            'index.html',
            name=session['username'],
            routes=config.c.routes,
            upload=request.args.get('upload')
        )
    else:
        return redirect(url_for('login'))

def generic_post():
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
    for category in ['selfie', 'uploaded']:
        files = request.files.getlist(category)
        for file in files:
            if file:
                file.save(user_folder / f'{category}_{secure_filename(file.filename)}')
    return redirect(url_for('index', upload='success'))


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
    print(f'Set secret key to {app.secret_key.hex()}')
    if not config:
        sys.exit(1)
    build_routes()
    app.run(host=host, port=port, debug=True)