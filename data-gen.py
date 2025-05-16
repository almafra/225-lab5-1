import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_contacts):
    """Generate test data for the contacts table with unique names."""
    db = connect_db()

    # Optional: clear the table to avoid duplicate entries
    # WARNING: Uncomment the next two lines ONLY if you're okay deleting all existing records
    # db.execute('DELETE FROM contacts')
    # db.commit()

    sample_names = [
        'Alice Johnson', 'Bob Smith', 'Charlie Davis', 'Diana Evans',
        'Ethan Brown', 'Fiona Clark', 'George Miller', 'Hannah Lee',
        'Ian Thompson', 'Julia White'
    ]

    for i in range(num_contacts):
        base_name = sample_names[i % len(sample_names)]
        name = f'{base_name} {i}'  # This makes it unique
        phone = f'123-456-789{i}'

        try:
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
        except sqlite3.IntegrityError as e:
            print(f"Failed to insert {name}: {e}")

    db.commit()
    print(f'{num_contacts} test contacts attempted to be added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)
