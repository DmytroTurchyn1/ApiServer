from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)



def get_user(user_id):
    con = sqlite3.connect("identifier.sqlite")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM Users WHERE id = ?", (user_id,)).fetchall()
    con.close()
    return res

def add_user(name, unit, email, password):
    con = sqlite3.connect("identifier.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO Users (name, unit, email, password) VALUES (?, ?, ?, ?)",
                (name, unit, email, password))
    con.commit()
    con.close()

def check_user(email, password):
    con = sqlite3.connect("identifier.sqlite")
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM Users WHERE email = ? AND password = ?",
                       (email, password)).fetchall()
    con.close()
    return len(rows) != 0

@app.route('/')
def hello():
    print("Hello World")
    return "Hello World"

@app.route('/get-user/<user_id>')
def home(user_id):
    user = get_user(user_id)
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
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if check_user(data['email'], data['password']):
        return jsonify({"error": "User already exists"}), 400

    add_user(data['name'], data['unit'], data['email'], data['password'])
    return jsonify("User added"), 201

if __name__ == '__main__':
    app.run()
