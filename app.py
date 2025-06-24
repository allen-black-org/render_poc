from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return (
        "Welcome to my Flask BI project!<br><br>"
        "This is a personal, AI-assisted learning app built to explore Python, Flask, and cloud deployment.<br><br>"
        "The goals of this project include:<br>"
        "- Building interactive web applications using Flask<br>"
        "- Connecting to and querying a PostgreSQL database<br>"
        "- Transforming and presenting data using Python<br>"
        "- Deploying apps to the cloud via Render<br><br>"
        "Check back as new features and routes are added over time."
    )

# Additional route that returns structured JSON
@app.route('/api/data')
def data():
    return jsonify({
        "name": "Allen",
        "role": "Business Intelligence Developer",
        "tools": ["Python", "Flask", "SQL", "Dash"]
    })


if __name__ == '__main__':
    app.run()
