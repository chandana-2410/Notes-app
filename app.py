from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect('notes.db')  # Connect to database (creates if not exists)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run the DB setup once
init_db()

# ---------- ROUTES ----------
@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        note = c.fetchone()
        conn.close()
        return render_template('edit.html', note=note)


if __name__ == '__main__':
    app.run(debug=True)
