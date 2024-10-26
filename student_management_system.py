from db_connection import get_connection

next_roll_number = 1


def add_student_dict(student):
    global next_roll_number
    name = input("Enter student name: ")
    marks = float(input("Enter marks: "))
    roll_number = str(next_roll_number)
    if roll_number in student:
        print(f"Student with roll number {roll_number} already exists!")
    else:
        student[roll_number] = {"name": name, "marks": marks}
        print(f"Student {name} added successfully!")
        next_roll_number += 1


def add_student_db(cursor):
    name = input("Enter student name: ")
    marks = float(input("Enter marks: "))
    cursor.execute('INSERT INTO students (name, marks) VALUES (?, ?)', (name, marks))
    cursor.connection.commit()
    print(f"Student {name} added successfully!")


# Function to display students (both dictionary and database)
def display_students(student, cursor):
    if isinstance(student, dict):
        _display_students_dict(student)
    else:
        _display_students_db(cursor)


def _display_students_dict(student):
    if not student:
        print("No student records found.")
        return

    roll_number = input("Enter roll number or enter 'all' to list all students: ")

    if roll_number == "all":
        print("\nStudent Records:")
        for roll_num, details in student.items():
            print(f"Roll Number: {roll_num}, Name: {details['name']}, Marks: {details['marks']}")
    else:
        _display_student_details(student.get(roll_number), roll_number)


def _display_students_db(cursor):
    roll_number = input("Enter roll number or enter 'all' to list all students: ")

    if roll_number == "all":
        cursor.execute('SELECT * FROM students')
        records = cursor.fetchall()
        if not records:
            print("No student records found.")
            return
        print("\nStudent Records:")
        for record in records:
            print(f"Roll Number: {record[0]}, Name: {record[1]}, Marks: {record[2]}")
    else:
        cursor.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,))
        student = cursor.fetchone()
        _display_student_detail(student, roll_number)


def _display_student_detail(student, roll_number):
    if student:
        # Assuming the tuple structure is (roll_number, name, marks)
        print(f"Roll Number: {student[0]}, Name: {student[1]}, Marks: {student[2]}")
    else:
        print(f"Student with roll number {roll_number} not found!")


def _display_student_details(student, roll_number):
    if student:
        print(f"Roll Number: {roll_number}, Name: {student['name']}, Marks: {student['marks']}")
    else:
        print(f"Student with roll number {roll_number} not found!")


# Function to delete a student (both dictionary and database)
def delete_student(student, cursor):
    roll_number = input("Enter roll number to delete student: ")
    if isinstance(student, dict):
        if roll_number in student:
            del student[roll_number]
            print(f"Student with roll number {roll_number} deleted successfully!")
        else:
            print(f"Student with roll number {roll_number} not found!")
    else:
        cursor.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
        cursor.connection.commit()
        if cursor.rowcount > 0:
            print(f"Student with roll number {roll_number} deleted successfully!")
        else:
            print(f"Student with roll number {roll_number} not found!")


# Function to update a student (both dictionary and database)
def update_student(student, cursor):
    roll_number = input("Enter roll number to update student: ")
    if isinstance(student, dict):
        _update_student_dict(student, roll_number)
    else:
        _update_student_db(cursor, roll_number)


def _update_student_dict(student, roll_number):
    if roll_number not in student:
        print(f"Student with roll number {roll_number} not found!")
        return

    name, marks = _get_student_updates()
    if name:
        student[roll_number]["name"] = name
    if marks is not None:
        student[roll_number]["marks"] = marks

    print(f"Student with roll number {roll_number} updated successfully!")


def _update_student_db(cursor, roll_number):
    cursor.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()

    if not student:
        print(f"Student with roll number {roll_number} not found!")
        return

    name, marks = _get_student_updates()
    if name:
        cursor.execute('UPDATE students SET name = ? WHERE roll_number = ?', (name, roll_number))
    if marks is not None:
        cursor.execute('UPDATE students SET marks = ? WHERE roll_number = ?', (marks, roll_number))

    cursor.connection.commit()
    print(f"Student with roll number {roll_number} updated successfully!")


def _get_student_updates():
    name = input("Enter new name (leave blank to keep current): ")
    marks_input = input("Enter new marks (leave blank to keep current): ")
    marks = float(marks_input) if marks_input else None
    return name, marks


def main():
    storage_type = input("Choose storage method (1 for Dictionary, 2 for SQLite): ")

    if storage_type == '1':
        student = {}
        _run_student_management_dict(student)
    elif storage_type == '2':
        conn, cursor = get_connection()
        _run_student_management_db(cursor)
        conn.close()
    else:
        print("Invalid storage type. Please choose 1 or 2.")


def _run_student_management_dict(student):
    while True:
        _display_menu("Dictionary")
        choice = input("Enter your choice: ")
        if not _handle_choice_dict(choice, student):
            break


def _run_student_management_db(cursor):
    while True:
        _display_menu("SQLite")
        choice = input("Enter your choice: ")
        if not _handle_choice_db(choice, cursor):
            break


def _display_menu(storage_type):
    print(f"\nStudent Management System (Using {storage_type})")
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Delete Student")
    print("4. Update Student")
    print("5. Exit")


def _handle_choice_dict(choice, student):
    if choice == '1':
        add_student_dict(student)
    elif choice == '2':
        display_students(student, None)
    elif choice == '3':
        delete_student(student, None)
    elif choice == '4':
        update_student(student, None)
    elif choice == '5':
        print("Exiting the Student Management System.")
        return False
    else:
        print("Invalid choice. Please try again.")
    return True


def _handle_choice_db(choice, cursor):
    if choice == '1':
        add_student_db(cursor)
    elif choice == '2':
        display_students(None, cursor)
    elif choice == '3':
        delete_student(None, cursor)
    elif choice == '4':
        update_student(None, cursor)
    elif choice == '5':
        print("Exiting the Student Management System.")
        return False
    else:
        print("Invalid choice. Please try again.")
    return True


if __name__ == "__main__":
    main()
