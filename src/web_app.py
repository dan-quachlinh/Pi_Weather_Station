from flask import Flask, request, render_template
from sendEmail import send_email
from sense_hat import SenseHat
import os

app = Flask(__name__)


@app.route('/')
def index():
    sense = SenseHat()
    sense.clear()

    acceleration = sense.get_accelerometer_raw()
    celcius      = round(sense.get_temperature(), 1)
    kwargs = dict(
        celcius     = celcius,
        fahrenheit  = round(1.8 * celcius + 32, 1),
        humidity    = round(sense.get_humidity(), 1),
        pressure    = round(sense.get_pressure(), 1),
        x = round(acceleration['x'], 2),
        y = round(acceleration['y'], 2),
        z = round(acceleration['z'], 2),
    )
    return render_template('weather.html', **kwargs)


@app.route('/alerts/', methods=['POST', 'GET'])
def alerts():
    if request.method == 'POST':
        e_subject = request.form['subject']
        e_message = request.form['message']
        send_email(e_subject, e_message)
    return render_template('alerts.html')


@app.route('/logs/')
def logs_web():
    csv_path = os.path.join(os.path.dirname(__file__), 'weather_logs.csv')
    with open(csv_path, 'r') as f:
        content = f.read()
    return render_template('logs.html', content=content)


while __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
