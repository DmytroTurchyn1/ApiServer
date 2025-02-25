import logging
from flask import Flask, jsonify, render_template, request
import sqlite3




app = Flask(__name__)

logging.basicConfig(
    filename='logs.log',               # Specify the log file name
    level=logging.INFO,               # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log message format
)


logging.info('Server Started')

def get_user_from_db(user_id):
    con = sqlite3.connect("/app/identifier.sqlite")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM Users WHERE ID = ?", (user_id,)).fetchall()
    con.close()
    return res

def add_user(name, unit, email, password):
    con = sqlite3.connect("/app/identifier.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO Users (Name, Unit, Email, Password) VALUES (?, ?, ?, ?)",
                (name, unit, email, password))
    con.commit()
    con.close()

def check_user(email, password):
    con = sqlite3.connect("/app/identifier.sqlite")
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM Users WHERE Email = ? AND Password = ?",
                       (email, password)).fetchall()
    con.close()
    return len(rows) != 0
    #chmod 777 /app/identifier.sqlite
    #chown appuser:appuser /app/identifier.sqlite
@app.route('/')
def home():
    return render_template("index.jinja2")

@app.route('/get-user/<user_id>')
def get_user(user_id):
    user = get_user_from_db(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_data = {
        "user_id": user_id,
        "name": user[0][1],
        "unit": user[0][2]
    }
    return jsonify(user_data), 200

@app.route("/post-user/create-user", methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or data['email']=="" and data['password']=="" and data['unit']=="" and data['name'] == "":
        return jsonify({"error": "No data provided"}), 400

    if check_user(data['email'], data['password']):
        return jsonify({"error": "User already exists"}), 400

    add_user(data['name'], data['unit'], data['email'], data['password'])
    return render_template("user_added.jinja2", name=data['name'], password=data['password'], email=data['email'], unit=data['unit']), 201

@app.route('/approved', methods = ['GET'])
def approved():
    return render_template("user_added.jinja2", name="hello", password="password")


if __name__ == '__main__':
    app.run()
