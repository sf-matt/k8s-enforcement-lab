from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask RCE Demo App — available at /cmd?input="

@app.route('/cmd')
def run_command():
    input_cmd = request.args.get('input')
    if not input_cmd:
        return "Usage: /cmd?input=<command>"
    try:
        os.system(input_cmd)
        return f"Command executed: {input_cmd}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)