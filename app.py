from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------------
# Database Connection
# ----------------------
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------
# Initialize Database
# ----------------------
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------
# Home - Add Student
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = get_db_connection()
        conn.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                     (name, age, course))
        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('index.html')


# ----------------------
# View Students
# ----------------------
@app.route('/view')
def view():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template('view.html', students=students)


# ----------------------
# Edit Student
# ----------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                     (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect('/view')

    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template('edit.html', student=student)


# ----------------------
# Delete Student
# ----------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/view')


# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)