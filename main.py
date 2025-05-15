from flask import Flask, request, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database setup
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    db = get_db()
    
    if request.method == 'POST':
        # Delete contact
        if 'delete_id' in request.form:
            db.execute('DELETE FROM contacts WHERE id = ?', (request.form['delete_id'],))
            db.commit()
            message = ('success', 'Contact deleted!')
        
        # Add new contact
        elif 'name' in request.form and 'phone' in request.form:
            name = request.form['name'].strip()
            phone = request.form['phone'].strip()
            
            if name and phone:
                db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
                db.commit()
                message = ('success', 'Contact added!')
            else:
                message = ('error', 'Please fill both fields')

    contacts = db.execute('SELECT * FROM contacts ORDER BY date_added DESC').fetchall()
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact Manager</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .alert {
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                }
                .success {
                    background: #dff0d8;
                    color: #3c763d;
                }
                .error {
                    background: #f2dede;
                    color: #a94442;
                }
                form {
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 8px;
                    margin: 8px 0;
                    box-sizing: border-box;
                }
                button {
                    background: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button.delete {
                    background: #f44336;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
                .date {
                    color: #666;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <h1>📒 Contact Manager</h1>
            
            {% if message %}
                <div class="alert {{ message[0] }}">{{ message[1] }}</div>
            {% endif %}
            
            <form method="POST">
                <h2>Add New Contact</h2>
                <input type="text" name="name" placeholder="Name" required>
                <input type="text" name="phone" placeholder="Phone" required>
                <button type="submit">Save Contact</button>
            </form>
            
            {% if contacts %}
                <h2>Your Contacts</h2>
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Added</th>
                        <th>Action</th>
                    </tr>
                    {% for contact in contacts %}
                    <tr>
                        <td>{{ contact['name'] }}</td>
                        <td>{{ contact['phone'] }}</td>
                        <td class="date">{{ contact['date_added'][:10] }}</td>
                        <td>
                            <form method="POST" style="display:inline">
                                <input type="hidden" name="delete_id" value="{{ contact['id'] }}">
                                <button type="submit" class="delete">Delete</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No contacts yet. Add your first contact above!</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(host='0.0.0.0', port=port)
