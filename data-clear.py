import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_contacts():
    """Clear test contacts with basic error handling."""
    try:
        db = connect_db()
        cursor = db.cursor()
        # Count before deleting
        cursor.execute("SELECT COUNT(*) FROM contacts WHERE name LIKE 'Test Name %'")
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute("DELETE FROM contacts WHERE name LIKE 'Test Name %'")
            db.commit()
            print(f'Deleted {count} test contacts.')
        else:
            print('No test contacts found.')
            
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    finally:
        if db:
            db.close()

if __name__ == '__main__':
    clear_test_contacts()
