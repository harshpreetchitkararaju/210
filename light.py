from flask import Flask, render_template_string
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  
pins = [11, 13, 19]    
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


app = Flask(__name__)

html = """
<!doctype html>
<title>Raspberry Pi LED Control</title>
<h1>LED Control</h1>
{% for i in range(led_count) %}
  <p>LED {{i+1}} 
  <a href="/on/{{i}}"><button>ON</button></a>
  <a href="/off/{{i}}"><button>OFF</button></a></p>
{% endfor %}
"""

@app.route('/')
def index():
    return render_template_string(html, led_count=len(pins))

@app.route('/on/<int:led>')
def led_on(led):
    if 0 <= led < len(pins):
        GPIO.output(pins[led], GPIO.HIGH)
    return render_template_string(html, led_count=len(pins))

@app.route('/off/<int:led>')
def led_off(led):
    if 0 <= led < len(pins):
        GPIO.output(pins[led], GPIO.LOW)
    return render_template_string(html, led_count=len(pins))


@app.route('/shutdown')
def shutdown():
    GPIO.cleanup()
    return "GPIO Cleaned up! You can safely exit."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
