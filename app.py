from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return ('Hello from Render! More to come...')


if __name__ == '__main__':
    app.run()
