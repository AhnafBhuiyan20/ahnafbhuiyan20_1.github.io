#!/usr/bin/python3

import cgi
import sqlite3

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()

task_id = form.getvalue("id")

conn = sqlite3.connect("neighborhelp.db")
cursor = conn.cursor()


if form.getvalue("helper_name"):

    helper_name = form.getvalue("helper_name")
    helper_email = form.getvalue("helper_email")
    helper_phone = form.getvalue("helper_phone")

    cursor.execute("""
    UPDATE requests
    SET
        helper_name = ?,
        helper_email = ?,
        helper_phone = ?,
        status = ?
    WHERE id = ?
    AND status = ?
    """, (
        helper_name,
        helper_email,
        helper_phone,
        "Claimed",
        task_id,
        "Open"
    ))

    conn.commit()


cursor.execute("""
SELECT * FROM requests
WHERE id = ?
""", (task_id,))

task = cursor.fetchone()


if task is None:

    print("""
    <html>
    <body>

    <h2>Request not found.</h2>

    <a href="index.py">
        Return Home
    </a>

    </body>
    </html>
    """)

else:

    status = task[10]

    if form.getvalue("helper_name") and status == "Claimed":

        print("""
        <!DOCTYPE html>

        <html>

        <head>

        <title>Help Confirmed</title>

        <link rel="stylesheet" href="styles.css">

        </head>

        <body>

        <section>

        <h2>You are helping!</h2>
        """)

        print("<h3>" + task[1] + "</h3>")

        print("""
        <h3>
        Requester's Contact Information
        </h3>
        """)

        print(
            "<p><strong>Name:</strong> " +
            task[4] +
            "</p>"
        )

        print(
            "<p><strong>Email:</strong> " +
            task[5] +
            "</p>"
        )

        if task[6]:

            print(
                "<p><strong>Phone:</strong> " +
                task[6] +
                "</p>"
            )

        print("""
        <a href="index.py">
            <button>Return Home</button>
        </a>

        </section>

        </body>

        </html>
        """)

    elif status == "Claimed":

        print("""
        <html>

        <body>

        <h2>
        Someone has already offered to help with this request.
        </h2>

        <a href="index.py">
            Return Home
        </a>

        </body>

        </html>
        """)

    else:

        print("""
        <!DOCTYPE html>

        <html>

        <head>

        <title>Offer Help</title>

        <link rel="stylesheet" href="styles.css">

        </head>

        <body>

        <section>

        <h2>Offer Help</h2>
        """)

        print("<h3>" + task[1] + "</h3>")

        print("<p>" + task[3] + "</p>")

        print("""
        <form method="POST" action="offer.py">

        <input
        type="hidden"
        name="id"
        value="
        """ + str(task_id) + """
        ">


        <label>Your Name</label>

        <input
        type="text"
        name="helper_name"
        required
        >


        <label>Email</label>

        <input
        type="email"
        name="helper_email"
        required
        >


        <label>Phone Number</label>

        <input
        type="text"
        name="helper_phone"
        >


        <button type="submit">
        Confirm and Offer Help
        </button>

        </form>

        </section>

        </body>

        </html>
        """)


conn.close()
