import csv
import sqlite3
import os

def check_student_in_txt(student_id, student_name, file_path):
    """Check if the student exists in a text file."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as file:
            for line in file:
                stored_id, stored_name = line.strip().split(',')
                if stored_id == student_id and stored_name == student_name:
                    return True
        return False
    except Exception as e:
        raise RuntimeError(f"Error reading text file: {e}")

def check_student_in_csv(student_id, student_name, file_path):
    """Check if the student exists in a CSV file."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == student_id and row[1] == student_name:
                    return True
        return False
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {e}")

def check_student_in_sql(student_id, student_name, db_path):
    """Check if the student exists in an SQLite database."""
    try:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database not found: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ? AND student_name = ?", (student_id, student_name))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        raise RuntimeError(f"Error querying SQLite database: {e}")

def log_gym_entry(student_id, student_name, time, locker_number, log_file="gym_log.txt"):
    """Log the gym entry into a file."""
    try:
        with open(log_file, 'a') as file:
            file.write(f"{student_id},{student_name},{time},{locker_number}\n")
    except Exception as e:
        raise RuntimeError(f"Error writing to log file: {e}")
