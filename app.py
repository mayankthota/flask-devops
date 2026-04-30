from flask import Flask, request, redirect, render_template, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

# ---------- DB ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # 🔥 change this
        database="student_db"
    )

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid login"

    return render_template("login.html")


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------- HOME ----------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]

    conn.close()

    return render_template("index.html", students=students, count=count)


# ---------- ADD ----------
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
        (name, age, course)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect('/')


# ---------- EDIT ----------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        cur.execute(
            "UPDATE students SET name=%s, age=%s, course=%s WHERE id=%s",
            (name, age, course, id)
        )

        conn.commit()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    conn.close()

    return render_template("edit.html", student=student)


# ---------- SEARCH ----------
@app.route('/search')
def search():
    query = request.args.get('q')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE name LIKE %s", ('%' + query + '%',))
    students = cur.fetchall()

    conn.close()

    return render_template("index.html", students=students, count=len(students))


# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
