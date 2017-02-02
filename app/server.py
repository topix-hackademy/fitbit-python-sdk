from flask import Flask, render_template, redirect, request, url_for, jsonify, session

from fitbit.fitbitsdk import Fitbit

app = Flask(__name__)
app.secret_key = 'fitbit_consumer'

fitbit = Fitbit()


@app.route('/')
def index():
    if 'user' in session.keys():
        return render_template('index.html')
    else:
        return render_template('index.html', permission_url=fitbit.get_permission_screen_url())


@app.route('/callback', methods=['GET'])
def handle_redirect():
    code = request.args.get('code')
    token_dict = fitbit.do_fitbit_auth(code)
    session['user'] = token_dict
    return redirect(url_for('index'))


@app.route('/device', methods=['GET'])
def get_device():
    return jsonify(
        devices=fitbit.get_device_info(session['user']['access_token'])
    )


@app.route('/heart', methods=['GET'])
def get_heart():
    return jsonify(
        heart_data=fitbit.get_heart_data(session['user']['access_token'])
    )


@app.route('/steps', methods=['GET'])
def get_steps():
    return jsonify(
        steps=fitbit.get_steps_data(session['user']['access_token'])
    )


@app.route('/sleep', methods=['GET'])
def get_sleep():
    return jsonify(
        sleep=fitbit.get_sleep_data(session['user']['access_token'])
    )


@app.route('/activities', methods=['GET'])
def get_activities():
    return jsonify(
        activities=fitbit.get_activities_data(session['user']['access_token'])
    )

if __name__ == '__main__':
    app.run()