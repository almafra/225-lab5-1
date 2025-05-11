import sqlite3
import sys

# Database file path
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database with error handling."""
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def count_test_contacts():
    """Count how many test contacts exist in the database."""
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM contacts WHERE name LIKE 'Test Name %'")
    count = cursor.fetchone()[0]
    db.close()
    return count

def clear_test_contacts():
    """Clear only the test contacts from the database with confirmation."""
    test_count = count_test_contacts()
    
    if test_count == 0:
        print("No test contacts found in the database.")
        return
    
    print(f"Found {test_count} test contacts to delete.")
    confirmation = input("Are you sure you want to delete these? (y/n): ")
    
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        return
    
    db = connect_db()
    try:
        db.execute("DELETE FROM contacts WHERE name LIKE 'Test Name %'")
        db.commit()
        print(f"Successfully deleted {test_count} test contacts.")
    except sqlite3.Error as e:
        print(f"Error deleting test contacts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    clear_test_contacts()
