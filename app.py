from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("students.db")

# Create table if not exists
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        course TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()

    return render_template_string("""
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body { font-family: Arial; background:#0f172a; color:white; text-align:center; }
            table { margin:auto; border-collapse: collapse; width:70%; }
            th, td { padding:10px; border:1px solid white; }
            input { padding:8px; margin:5px; }
            button { padding:8px 15px; background:#38bdf8; border:none; }
        </style>
    </head>
    <body>
        <h1>🎓 Student Management System</h1>

        <form method="POST" action="/add">
            <input name="name" placeholder="Name" required>
            <input name="age" placeholder="Age" required>
            <input name="course" placeholder="Course" required>
            <button type="submit">Add Student</button>
        </form>

        <br>

        <table>
            <tr>
                <th>ID</th><th>Name</th><th>Age</th><th>Course</th><th>Action</th>
            </tr>
            {% for s in students %}
            <tr>
                <td>{{s[0]}}</td>
                <td>{{s[1]}}</td>
                <td>{{s[2]}}</td>
                <td>{{s[3]}}</td>
                <td><a href="/delete/{{s[0]}}" style="color:red;">Delete</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, students=students)

@app.route('/add', methods=['POST'])
def add():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                (request.form['name'], request.form['age'], request.form['course']))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)