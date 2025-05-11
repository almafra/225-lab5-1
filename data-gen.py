import sqlite3
import random

DATABASE = '/nfs/demo.db'
DEFAULT_COUNT = 10  # Made configurable

def connect_db():
    """Connect to the SQLite database with error handling."""
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        raise

def generate_test_data(num_contacts=DEFAULT_COUNT):
    """Generate more realistic test data."""
    first_names = ['Alex', 'Jamie', 'Taylor', 'Morgan', 'Casey']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
    
    with connect_db() as db:
        for i in range(num_contacts):
            # Generate more varied test data
            first = random.choice(first_names)
            last = random.choice(last_names)
            name = f"Test {first} {last} {i}"
            phone = f"{random.randint(200,999)}-{random.randint(100,999)}-{i:04d}"
            
            db.execute(
                'INSERT INTO contacts (name, phone) VALUES (?, ?)',
                (name, phone)
            )
        print(f"Added {num_contacts} test contacts")

if __name__ == '__main__':
    generate_test_data()  # Uses default count
