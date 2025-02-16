from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html', socket_port = sys.argv[2])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit()
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
