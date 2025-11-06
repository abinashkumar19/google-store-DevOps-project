from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    "host": "database-1.cjy48iyci4zm.ap-northeast-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Cloud1234",
    "database": "registrationdb"  # ✅ your DB name
}

def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- SAVE USER ----------------
@app.route("/api/save", methods=["POST"])
def save_user():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, email, password))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- GET ALL USERS ----------------
@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
