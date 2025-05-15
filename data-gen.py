from db_utils import connect_db, init_db

def generate_test_data(num_contacts):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_contacts):
        name = f'Test Name {i}'
        phone = f'123-456-789{i}'
        db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    db.commit()
    print(f'{num_contacts} test contacts added to the database.')
    db.close()

if __name__ == '__main__':
    init_db()
    generate_test_data(10)
