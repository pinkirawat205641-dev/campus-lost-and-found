import pymysql

try:
    # Connect directly to MySQL without selecting a database
    # The password must be exactly 'root' based on user's instruction
    conn = pymysql.connect(host='localhost', user='root', password='root')
    cursor = conn.cursor()
    
    # Create the database securely
    cursor.execute('CREATE DATABASE IF NOT EXISTS lost_and_found_db')
    
    conn.commit()
    conn.close()
    print("Database connected and `lost_and_found_db` ensured accurately.")
except Exception as e:
    print(f"Error accessing MySQL: {e}\nEnsure MySQL is running and password is 'root'.")
