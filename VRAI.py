import sqlite3
import pyttsx3
import datetime
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def db_to_json(db_file, json_file):
    """
    Converts a SQLite database file into a JSON file.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Dictionary to store database content
        db_dict = {}

        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Fetch column names
            column_names = [description[0] for description in cursor.description]
            
            # Store table data as a list of dictionaries
            db_dict[table_name] = [dict(zip(column_names, row)) for row in rows]
        
        # Write database content to JSON file
        with open(json_file, 'w') as f:
            json.dump(db_dict, f, indent=4)
        
        print(f"Database successfully converted to {json_file}")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

def use_json_file(json_file):
    """
    Performs operations using the JSON file.
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Example operation: print the first table's contents
        for table_name, records in data.items():
            print(f"Table: {table_name}")
            for record in records:
                print(record)
            break  # Stop after processing the first table
    
    except FileNotFoundError:
        print(f"File {json_file} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Usage example:

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!") 

    else:
        speak("Good Evening!")  
        print("Good Evening!")

    speak("I am VIRTUAL REACTOR ALFA INTELLIGENCE Sir. Please tell me how may I help you?")  
    print("I am VIRTUAL REACTOR ALFA INTELLIGENCE Sir. Please tell me how may I help you?")     

# Function to establish a database connection and create the table if it doesn't exist
def get_db_connection():
    conn = sqlite3.connect('key_value_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS KeyValuePairs (
            `key` TEXT PRIMARY KEY,
            `value` TEXT
        )
    ''')
    conn.commit()
    return conn

# Function to add a key-value pair
def add_key_value(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO KeyValuePairs (`key`, `value`) VALUES (?, ?)", (key, value))
        conn.commit()
        print(f"Key-Value pair ({key}, {value}) added successfully.")
        speak("Key-Value pair added Successfully!")
    except sqlite3.IntegrityError:
        print(f"Key '{key}' already exists. Please use a unique key.")
        speak("Please use a unique key!")
    finally:
        cursor.close()
        conn.close()

# Function to delete a key-value pair
def delete_key_value(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM KeyValuePairs WHERE `key` = ?", (key,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Key '{key}' deleted successfully.")
        speak("Key deleted successfully!")
    else:
        print(f"Key '{key}' not found.")
        speak("Key not found!")
    cursor.close()
    conn.close()

# Function to get the value by key
def get_value_by_key(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT `value` FROM KeyValuePairs WHERE `key` = ?", (key,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        speak(f"Your {key} is {result[0]}")
    else:
        return f"Key '{key}' not found."

# Main program loop
def main():
    while True:
        print("\nMenu:")
        print("1. Add Key-Value Pair")
        print("2. Delete Key-Value Pair")
        print("3. Get Value by Key")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            key = input("Enter key: ")
            value = input("Enter value: ")
            add_key_value(key, value)
        elif choice == '2':
            key = input("Enter key to delete: ")
            delete_key_value(key)
        elif choice == '3':
            key = input("Enter key to retrieve value: ")
            value = get_value_by_key(key)
            print(f"Value: {value}")

        elif choice == '4':
            print("Exiting the program...")
            speak("Exiting the program...")
            break
        else:
            print("Invalid Choice. Please try again...")
            speak("Invalid Choice. Please try again...")

if __name__ == "__main__":
    wishMe()
    main()
    db_file = "key_value_store.db"  # Replace with your SQLite database file
    json_file = "key_value_store.json"
    db_to_json(db_file, json_file)
    use_json_file(json_file)
    speak()