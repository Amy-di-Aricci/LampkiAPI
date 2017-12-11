#!/usr/bin/sudo python
from flask import Flask, jsonify, abort, request
from neopixel import *

app = Flask(__name__)

LED_COUNT = 8       # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

lights = {key: "#ffffff" for key in range(LED_COUNT)}


def convert_hex_to_color(hex_value):
    value = hex_value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/lights', methods=['GET'])
def get_all_colors():
    return jsonify({'lights': lights})


@app.route('/lights/<int:diode_id>', methods=['GET'])
def get_one_color(diode_id):
    if diode_id not in lights.keys():
        abort(404)
    return jsonify({'light': lights[diode_id]})


@app.route('/lights/<int:diode_id>', methods=['PUT'])
def set_one_color(diode_id):
    if diode_id not in lights.keys():
        abort(404)
    if not request.json:
        print("No JSON")
        abort(400)
    if 'color' not in request.json:
        print("NO COLOR in JSON")
        abort(400)
    if type(request.json['color']) is not unicode:
        print("Bad type of color")
        abort(400)
    strip.setPixelColor(diode_id, Color(*convert_hex_to_color(request.json['color'])))
    strip.show()
    lights[diode_id] = request.json['color']
    return 'OK'


@app.route('/lights', methods=['PUT'])
def set_all_colors():
    if not request.json:
        print("No JSON")
        abort(400)
    if 'color' not in request.json:
        print("NO COLOR in JSON")
        abort(400)
    if type(request.json['color']) is not unicode:
        print("Bad type of color")
        abort(400)
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(
            *convert_hex_to_color(request.json['color'])))
        lights[i] = request.json['color']
    strip.show()
    return 'OK'


def main():
    strip.begin()
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(255, 255, 255))
        strip.show()
    app.run(debug=True, host="0.0.0.0")

if __name__ == '__main__':
    main()
