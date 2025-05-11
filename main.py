from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__, static_url_path='/static')

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Enables name-based column access
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Contact deleted successfully.'
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
                db.commit()
                message = 'Contact added successfully.'
            else:
                message = 'Missing name or phone number.'

    db = get_db()
    contacts = db.execute('''
        SELECT *, 
        CASE WHEN name LIKE 'Test%' THEN 1 ELSE 0 END AS is_test 
        FROM contacts 
        ORDER BY is_test DESC, name
    ''').fetchall()

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        </head>
        <body>
            <h2>Contacts Manager</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="phone">Phone:</label><br>
                <input type="text" id="phone" name="phone" required><br><br>
                <input type="submit" value="Add Contact">
            </form>
            
            {% if message %}<p style="color: green;">{{ message }}</p>{% endif %}
            
            {% if contacts %}
                <table border="1" cellpadding="8" cellspacing="0" width="100%">
                    <tr>
                        <th>Name</th>
                        <th>Phone Number</th>
                        <th>Actions</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr {% if contact['is_test'] %}class="test-contact"{% endif %}>
                            <td>
                                {% if contact['is_test'] %}
                                    <span class="test-badge">TEST</span><br>
                                {% endif %}
                                {{ contact['name'] }}
                            </td>
                            <td>{{ contact['phone'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete" 
                                        class="delete-button">
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
    app.run(host='0.0.0.0', port=port)
