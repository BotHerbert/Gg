from flask import Flask, render_template, request, redirect, url_for
import telethon.sync
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient

app = Flask(__name__)

# Replace these with your own API_ID, API_HASH, and SESSION_PATH
API_ID = 988074
API_HASH = 'a5ec8b7b6dbeedc2514ca7e4ba200c13'
SESSION_PATH = '/session'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the phone number entered by the user
        phone = request.form.get('phone')

        # Initialize the Telegram client
        client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

        # Start the client and send the code to the user's phone number
        with client:
            # Send the code to the user's phone number
            try:
                client.send_code_request(phone)
                return redirect(url_for('enter_code', phone=phone))
            except Exception as e:
                return render_template('index.html', error=str(e))

    return render_template('index.html')

@app.route('/enter_code', methods=['GET', 'POST'])
def enter_code():
    phone = request.args.get('phone')

    if request.method == 'POST':
        # Get the code entered by the user
        code = request.form.get('code')

        # Initialize the Telegram client
        client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

        # Enter the code and save the session
        with client:
            try:
                client.sign_in(phone, code)
            except SessionPasswordNeededError:
                # If the account has a password, prompt the user to enter it
                password = request.form.get('password')
                client.sign_in(password=password)

            # Save the session to the SESSION_PATH
            client.session.save()

        return redirect(url_for('success'))

    return render_template('enter_code.html', phone=phone)

@app.route('/success')
def success():
    return 'Successfully logged in!'

if __name__ == '__main__':
    app.run(debug=True)
