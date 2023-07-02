from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def test_page():
    return render_template("index.html")

@app.route('/slave')
def slave_page():
    return render_template("slave.html")

@app.route('/slave2')
def second_slave_page():
    return render_template("slave2.html")

@app.route('/slave2/subpage')
def subpage():
    return render_template("subpage.html")
