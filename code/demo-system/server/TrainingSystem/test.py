from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("Hello, World!")
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="localhost", port=5500, debug=True)