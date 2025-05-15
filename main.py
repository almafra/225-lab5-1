from flask import Flask, request, render_template_string
import os
from db_utils import connect_db, init_db

app = Flask(__name__)

def get_db():
    return connect_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            db.close()
            message = 'Contact deleted successfully.'
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)', 
                           (name, phone, email, address))
                db.commit()
                db.close()
                message = 'Contact added successfully.'
            else:
                message = 'Name and phone number are required.'

    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()
    db.close()

    return render_template_string(..., message=message, contacts=contacts)  # (Keep the same template code)

        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #e7eb8d;
                }
                h2 { color: #333; }
                form { margin-bottom: 20px; }
                label { font-weight: bold; }
                input[type="text"] {
                    padding: 8px;
                    width: 250px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                input[type="submit"] {
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th { background-color: #f2f2f2; }
                tr:hover { background-color: #f1f1f1; }
                .message { color: green; font-weight: bold; }
                small { color: #666; font-size: 11px; }
            </style>
        </head>
        <body>
            <h2>Add Contacts Test for Lab 5-1</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>

                <label for="phone">Phone Number:</label><br>
                <input type="text" id="phone" name="phone" required><br>

                <label for="email">Email Address:</label><br>
                <input type="text" id="email" name="email"><br>

                <label for="address">Home Address:</label><br>
                <input type="text" id="address" name="address"><br><br>

                <input type="submit" value="Submit">
            </form>

            <p class="message">{{ message }}</p>

            {% if contacts %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Email Address</th>
                        <th>Home Address</th>
                        <th>Delete</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['phone'] }}</td>
                            <td>{{ contact['email'] or '' }}</td>
                            <td>{{ contact['address'] or '' }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete" style="background-color: #ff4d4d;">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
