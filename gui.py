import tkinter as tk
from tkinter import messagebox
from database_handler import (
    check_student_in_txt,
    check_student_in_csv,
    check_student_in_sql,
    log_gym_entry,
)
from utils import validate_student_id

class GymLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Logger")

        # Labels and Entry Fields
        tk.Label(root, text="Student ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.student_id_entry = tk.Entry(root)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Student Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.student_name_entry = tk.Entry(root)
        self.student_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Time (HH:MM):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Locker Number:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.locker_number_entry = tk.Entry(root)
        self.locker_number_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Database Type:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.db_type_var = tk.StringVar(value="txt")
        tk.OptionMenu(root, self.db_type_var, "txt", "csv", "sql").grid(row=4, column=1, padx=10, pady=5)

        tk.Label(root, text="Database Path:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.db_path_entry = tk.Entry(root)
        self.db_path_entry.grid(row=5, column=1, padx=10, pady=5)

        # Log Button
        tk.Button(root, text="Log Entry", command=self.log_entry).grid(row=6, column=0, columnspan=2, pady=10)

    def log_entry(self):
        """Handle logging the gym entry with error handling."""
        try:
            # Get user inputs
            student_id = self.student_id_entry.get().strip()
            student_name = self.student_name_entry.get().strip()
            time = self.time_entry.get().strip()
            locker_number = self.locker_number_entry.get().strip() or "None"
            db_type = self.db_type_var.get().strip()
            db_path = self.db_path_entry.get().strip()

            # Validate Student ID
            if not validate_student_id(student_id):
                raise ValueError("Invalid Student ID. It must start with 'TP' and be 8 characters long.")

            # Check if student exists in the database
            if db_type == "txt":
                exists = check_student_in_txt(student_id, student_name, db_path)
            elif db_type == "csv":
                exists = check_student_in_csv(student_id, student_name, db_path)
            elif db_type == "sql":
                exists = check_student_in_sql(student_id, student_name, db_path)
            else:
                raise ValueError("Invalid database type. Please choose 'txt', 'csv', or 'sql'.")

            if not exists:
                raise ValueError("Student ID and Name do not match any records in the database.")

            # Log the entry
            log_gym_entry(student_id, student_name, time, locker_number)
            messagebox.showinfo("Success", "Gym entry logged successfully!")

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"File not found: {e}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except RuntimeError as e:
            messagebox.showerror("Error", f"Runtime error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
