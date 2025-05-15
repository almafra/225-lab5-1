from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

# Database file path
DATABASE = '/nfs/demo.db'

# Sample fun facts about contacts
FUN_FACTS = [
    "The average person has 300 contacts in their phone",
    "The first phone book was published in 1878",
    "The longest phone call lasted over 56 hours",
    "Over 100 billion spam calls are made each year",
    "The most expensive phone number was sold for $2.7 million"
]

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            );
        ''')
        # Create a stats table to track operations
        db.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        db.commit()

def log_operation(operation):
    db = get_db()
    db.execute('INSERT INTO stats (operation) VALUES (?)', (operation,))
    db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    fun_fact = random.choice(FUN_FACTS)  # Get a random fun fact
    
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            log_operation('delete')
            message = '✅ Contact deleted successfully!'
        elif request.form.get('action') == 'edit':
            # Handle edit functionality
            contact_id = request.form.get('contact_id')
            new_name = request.form.get('new_name')
            new_phone = request.form.get('new_phone')
            if new_name and new_phone:
                db = get_db()
                db.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', 
                          (new_name, new_phone, contact_id))
                db.commit()
                log_operation('edit')
                message = '✏️ Contact updated successfully!'
        else:
            # Handle add contact
            name = request.form.get('name')
            phone = request.form.get('phone')
            notes = request.form.get('notes', '')
            
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone, notes) VALUES (?, ?, ?)', 
                           (name, phone, notes))
                db.commit()
                log_operation('add')
                message = '👋 Contact added successfully!'
            else:
                message = '⚠️ Missing name or phone number!'

    # Get contacts and stats
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts ORDER BY date_added DESC').fetchall()
    
    # Get some stats
    total_contacts = db.execute('SELECT COUNT(*) FROM contacts').fetchone()[0]
    last_added = db.execute('SELECT name FROM contacts ORDER BY date_added DESC LIMIT 1').fetchone()
    last_added = last_added['name'] if last_added else "None"

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts Manager</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    background-color: #f4f4f9;
                    color: #333;
                }
                h2 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                }
                .card {
                    background: white;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .stats-card {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .stat-item {
                    text-align: center;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 5px;
                    flex: 1;
                    margin: 0 10px;
                }
                form {
                    margin-bottom: 20px;
                }
                label {
                    font-weight: bold;
                    display: block;
                    margin-top: 10px;
                }
                input[type="text"], textarea {
                    padding: 10px;
                    width: 100%;
                    margin-bottom: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                textarea {
                    height: 80px;
                    resize: vertical;
                }
                button, input[type="submit"] {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: bold;
                    margin-right: 10px;
                    transition: all 0.3s;
                }
                .add-btn {
                    background-color: #2ecc71;
                    color: white;
                }
                .add-btn:hover {
                    background-color: #27ae60;
                }
                .delete-btn {
                    background-color: #e74c3c;
                    color: white;
                }
                .delete-btn:hover {
                    background-color: #c0392b;
                }
                .edit-btn {
                    background-color: #3498db;
                    color: white;
                }
                .edit-btn:hover {
                    background-color: #2980b9;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #3498db;
                    color: white;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
                .message {
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                }
                .success {
                    background-color: #d4edda;
                    color: #155724;
                }
                .error {
                    background-color: #f8d7da;
                    color: #721c24;
                }
                .fun-fact {
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 15px;
                    border-radius: 4px;
                    margin-bottom: 20px;
                    font-style: italic;
                }
                .contact-actions {
                    display: flex;
                    gap: 5px;
                }
                .notes {
                    font-size: 0.9em;
                    color: #666;
                    margin-top: 5px;
                }
                .edit-form {
                    display: none;
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h2>📱 Contacts Manager</h2>
                    
                    <div class="fun-fact">
                        <strong>Did you know?</strong> {{ fun_fact }}
                    </div>
                    
                    <div class="stats-card">
                        <div class="stat-item">
                            <h3>📊 Total Contacts</h3>
                            <p>{{ total_contacts }}</p>
                        </div>
                        <div class="stat-item">
                            <h3>🆕 Last Added</h3>
                            <p>{{ last_added }}</p>
                        </div>
                    </div>
                    
                    {% if message %}
                        <div class="message {{ 'success' if 'success' in message else 'error' }}">
                            {{ message }}
                        </div>
                    {% endif %}
                    
                    <form method="POST" action="/">
                        <h3>➕ Add New Contact</h3>
                        <label for="name">Name:</label>
                        <input type="text" id="name" name="name" required>
                        
                        <label for="phone">Phone Number:</label>
                        <input type="text" id="phone" name="phone" required>
                        
                        <label for="notes">Notes:</label>
                        <textarea id="notes" name="notes"></textarea>
                        
                        <input type="submit" class="add-btn" value="Add Contact">
                    </form>
                    
                    {% if contacts %}
                        <h3>👥 Your Contacts</h3>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Date Added</th>
                                <th>Actions</th>
                            </tr>
                            {% for contact in contacts %}
                                <tr>
                                    <td>
                                        <strong>{{ contact['name'] }}</strong>
                                        {% if contact['notes'] %}
                                            <div class="notes">📝 {{ contact['notes'] }}</div>
                                        {% endif %}
                                    </td>
                                    <td>{{ contact['phone'] }}</td>
                                    <td>{{ contact['date_added'] }}</td>
                                    <td class="contact-actions">
                                        <form method="POST" action="/" style="display:inline;">
                                            <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                            <input type="hidden" name="action" value="delete">
                                            <input type="submit" class="delete-btn" value="Delete" 
                                                   onclick="return confirm('Are you sure you want to delete this contact?');">
                                        </form>
                                        <button class="edit-btn" onclick="toggleEditForm({{ contact['id'] }})">Edit</button>
                                        <div id="edit-form-{{ contact['id'] }}" class="edit-form">
                                            <form method="POST" action="/">
                                                <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                                <input type="hidden" name="action" value="edit">
                                                <input type="text" name="new_name" value="{{ contact['name'] }}" required>
                                                <input type="text" name="new_phone" value="{{ contact['phone'] }}" required>
                                                <input type="submit" class="edit-btn" value="Save">
                                            </form>
                                        </div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </table>
                    {% else %}
                        <div class="card">
                            <p>No contacts found. Add your first contact above!</p>
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <script>
                function toggleEditForm(id) {
                    const form = document.getElementById('edit-form-' + id);
                    form.style.display = form.style.display === 'block' ? 'none' : 'block';
                }
            </script>
        </body>
        </html>
    ''', message=message, contacts=contacts, fun_fact=fun_fact, 
       total_contacts=total_contacts, last_added=last_added)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
