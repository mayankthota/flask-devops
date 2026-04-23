from flask import Flask, request, redirect

app = Flask(__name__)

students = []

@app.route('/')
def home():
    student_list = ""
    for i, student in enumerate(students):
        student_list += f"""
        <tr>
            <td>{student['name']}</td>
            <td>{student['age']}</td>
            <td>{student['course']}</td>
            <td><a href='/delete/{i}' style='color:red;'>Delete</a></td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
            }}
            table {{
                margin: auto;
                border-collapse: collapse;
                width: 60%;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid white;
            }}
            input {{
                padding: 8px;
                margin: 5px;
            }}
            button {{
                padding: 8px 15px;
                background: #38bdf8;
                border: none;
            }}
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
                <th>Name</th>
                <th>Age</th>
                <th>Course</th>
                <th>Action</th>
            </tr>
            {student_list}
        </table>
    </body>
    </html>
    """

@app.route('/add', methods=['POST'])
def add():
    students.append({
        "name": request.form['name'],
        "age": request.form['age'],
        "course": request.form['course']
    })
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)