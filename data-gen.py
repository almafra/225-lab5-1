import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test data for the contacts table with unique names."""
    db = connect_db()
    sample_names = [
        'Alice Johnson', 'Bob Smith', 'Charlie Davis', 'Diana Evans',
        'Ethan Brown', 'Fiona Clark', 'George Miller', 'Hannah Lee',
        'Ian Thompson', 'Julia White'
    ]

    for i in range(num_contacts):
        # Append index to make names unique
        base_name = sample_names[i % len(sample_names)]
        name = f'{base_name} {i}'
        phone = f'123-456-789{i}'
        db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))

    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.
