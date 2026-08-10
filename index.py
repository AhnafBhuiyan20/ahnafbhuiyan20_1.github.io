#!/usr/bin/python3

import cgi
import sqlite3

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()

conn = sqlite3.connect("neighborhelp.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    description TEXT,
    requester_name TEXT,
    requester_email TEXT,
    requester_phone TEXT,
    helper_name TEXT,
    helper_email TEXT,
    helper_phone TEXT,
    status TEXT
)
""")

if form.getvalue("title"):

    title = form.getvalue("title")
    category = form.getvalue("category")
    description = form.getvalue("description")
    name = form.getvalue("name")
    email = form.getvalue("email")
    phone = form.getvalue("phone")

    cursor.execute("""
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

cursor.execute("""
SELECT * FROM requests
ORDER BY id DESC
""")

requests = cursor.fetchall()

print("""
<!DOCTYPE html>
<html>

<head>

<title>NeighborHelp</title>

<link rel="stylesheet" href="styles.css">

</head>

<body>

<header>
    <h2>NeighborHelp</h2>
</header>

<div class="hero">

    <h1>Neighbors Helping Neighbors</h1>

    <p>
        Ask for help or volunteer to help someone in your community.
    </p>

</div>


<section>

<h2>Recent Requests</h2>

<div class="cards">
""")

for task in requests:

    task_id = task[0]
    title = task[1]
    category = task[2]
    description = task[3]
    requester_name = task[4]
    status = task[10]

    print('<div class="card">')

    print("<h3>" + title + "</h3>")

    print("<p><strong>Category:</strong> " + category + "</p>")

    print("<p>" + description + "</p>")

    print("<p>Requested by: " + requester_name + "</p>")

    if status == "Open":

        print("<p>Available</p>")

        print(
            '<a href="offer.py?id=' +
            str(task_id) +
            '"><button>Offer Help</button></a>'
        )

    else:

        print("<p>Someone is helping</p>")

    print("</div>")


print("""
</div>

</section>


<section>

<h2>Ask for Help</h2>

<form method="POST" action="index.py">

<label>Your Name</label>

<input
type="text"
name="name"
required
>


<label>Email</label>

<input
type="email"
name="email"
required
>


<label>Phone Number</label>

<input
type="text"
name="phone"
>


<label>Request Title</label>

<input
type="text"
name="title"
required
>


<label>Category</label>

<select name="category">

<option>Lawn Care</option>

<option>Errands</option>

<option>Transportation</option>

<option>Moving Help</option>

<option>Rent Assistance</option>

<option>Other</option>

</select>


<label>Description</label>

<textarea
name="description"
required>
</textarea>


<button type="submit">
Submit Request
</button>

</form>

</section>


<footer>

<p>
NeighborHelp | Building stronger communities
</p>

</footer>

</body>
</html>
""")

conn.close()
