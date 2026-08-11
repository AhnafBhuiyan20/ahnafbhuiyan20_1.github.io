from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("neighborhelp.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,

            requester_name TEXT NOT NULL,
            requester_email TEXT NOT NULL,
            requester_phone TEXT,

            helper_name TEXT,
            helper_email TEXT,
            helper_phone TEXT,

            status TEXT DEFAULT 'Open'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()

    tasks = conn.execute("""
        SELECT * FROM requests
        WHERE status = 'Open'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/submit", methods=["POST"])
def submit():
    title = request.form.get("title")
    category = request.form.get("category")
    description = request.form.get("description")

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    conn = get_db()

    conn.execute("""
        INSERT INTO requests (
            title,
            category,
            description,
            requester_name,
            requester_email,
            requester_phone,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        category,
        description,
        name,
        email,
        phone,
        "Open"
    ))

    conn.commit()
    conn.close()

    return redirect("/#help")


@app.route("/offer/<int:task_id>", methods=["GET", "POST"])
def offer(task_id):
    conn = get_db()

    task = conn.execute("""
        SELECT * FROM requests
        WHERE id = ?
    """, (task_id,)).fetchone()

    if task is None:
        conn.close()
        return "Request not found."

    if request.method == "POST":

        if task["status"] != "Open":
            conn.close()
            return "Someone has already offered to help."

        helper_name = request.form.get("helper_name")
        helper_email = request.form.get("helper_email")
        helper_phone = request.form.get("helper_phone")

        conn.execute("""
            UPDATE requests
            SET helper_name = ?,
                helper_email = ?,
                helper_phone = ?,
                status = ?
            WHERE id = ?
        """, (
            helper_name,
            helper_email,
            helper_phone,
            "Claimed",
            task_id
        ))

        conn.commit()

        task = conn.execute("""
            SELECT * FROM requests
            WHERE id = ?
        """, (task_id,)).fetchone()

        conn.close()

        return render_template(
            "offer.html",
            task=task,
            confirmed=True
        )

    conn.close()

    return render_template(
        "offer.html",
        task=task,
        confirmed=False
    )


create_table()


if __name__ == "__main__":
    app.run(debug=True)
