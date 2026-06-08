from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

DATABASE = "students.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        course TEXT
    )
    """)

    cursor.execute("PRAGMA table_info(students)")
    columns = {column[1] for column in cursor.fetchall()}

    if "age" not in columns:
        cursor.execute("ALTER TABLE students ADD COLUMN age INTEGER")

    if "course" not in columns:
        cursor.execute("ALTER TABLE students ADD COLUMN course TEXT")

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.after_request
def disable_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/students", methods=["GET"])
def get_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, age, course FROM students")

    rows = cursor.fetchall()

    conn.close()

    students = []

    for row in rows:
        students.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3]
        })

    return jsonify(students)


@app.route("/students", methods=["POST"])
def add_student():

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
        (data["name"], data["age"], data["course"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student Added"})


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=?, age=?, course=?
        WHERE id=?
        """,
        (data["name"], data["age"], data["course"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student Updated"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student Deleted"})


if __name__ == "__main__":
    init_db()
    print("CRUD Operations running at http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
