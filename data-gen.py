import sqlite3
import os
import random

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test data for the contacts table using real names."""
    db = connect_db()

    real_names = [
        'Alice Johnson', 'Bob Smith', 'Charlie Nguyen', 'Diana Lee', 'Ethan Patel',
        'Fiona Garcia', 'George Kim', 'Hannah Brown', 'Isaac Wilson', 'Julia Chen',
        'Kevin White', 'Laura Martinez', 'Mohammed Ali', 'Natalie Green', 'Oscar Turner'
    ]

    for i in range(num_contacts):
        name = real_names[i % len(real_names)]
        phone = f'123-456-78{random.randint(10, 99)}'
        email = f"{name.split()[0].lower()}.{name.split()[1].lower()}@example.com"
        address = f"{random.randint(100, 999)} Main St, City {i+1}"

        db.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)',
                   (name, phone, email, address))

    db.commit()
    print(f'{num_contacts} real contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 real contacts
