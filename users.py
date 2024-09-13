import mysql.connector

# Establish connection to MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Redminote#9",  # Replace with your MySQL password
        database="employee_db"
    )

# Login function to verify user credentials
def login():
    db = connect_to_db()
    cursor = db.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    db.close()

    if result:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Try again.")
        return False

# Create new employee record
def add_employee():
    db = connect_to_db()
    cursor = db.cursor()

    name = input("Enter employee name: ")
    age = int(input("Enter employee age: "))
    department = input("Enter department: ")
    salary = float(input("Enter employee salary: "))

    query = "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, age, department, salary))
    db.commit()

    print("Employee added successfully!")
    db.close()

# Fetch and display all employee records
def view_employees():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM employees")
    records = cursor.fetchall()

    print("ID | Name | Age | Department | Salary")
    print("-------------------------------------")
    for row in records:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

    db.close()

# Update employee record
def update_employee():
    db = connect_to_db()
    cursor = db.cursor()

    emp_id = int(input("Enter employee ID to update: "))
    new_salary = float(input("Enter new salary: "))

    query = "UPDATE employees SET salary = %s WHERE id = %s"
    cursor.execute(query, (new_salary, emp_id))
    db.commit()

    print("Employee salary updated successfully!")
    db.close()

# Delete employee record
def delete_employee():
    db = connect_to_db()
    cursor = db.cursor()

    emp_id = int(input("Enter employee ID to delete: "))

    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (emp_id,))
    db.commit()

    print("Employee deleted successfully!")
    db.close()


# ATTENDANCE
# Employee Clock-In function
def clock_in():
    db = connect_to_db()
    cursor = db.cursor()

    emp_id = int(input("Enter your Employee ID to clock in: "))

    # Check if the employee has already clocked in and not clocked out yet
    query = "SELECT * FROM attendance WHERE employee_id = %s AND clock_out IS NULL"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()

    if result:
        print(f"Employee {emp_id} is already clocked in. Please clock out before clocking in again.")
    else:
        query = "INSERT INTO attendance (employee_id) VALUES (%s)"
        cursor.execute(query, (emp_id,))
        db.commit()
        print(f"Employee {emp_id} clocked in successfully!")

    db.close()

# Employee Clock-Out function
def clock_out():
    db = connect_to_db()
    cursor = db.cursor()

    emp_id = int(input("Enter your Employee ID to clock out: "))

    # Check if the employee has clocked in
    query = "SELECT * FROM attendance WHERE employee_id = %s AND clock_out IS NULL"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()

    if result:
        # If the employee is clocked in, update the clock_out time
        query = "UPDATE attendance SET clock_out = CURRENT_TIMESTAMP WHERE employee_id = %s AND clock_out IS NULL"
        cursor.execute(query, (emp_id,))
        db.commit()
        print(f"Employee {emp_id} clocked out successfully!")
    else:
        print(f"Employee {emp_id} has not clocked in yet or has already clocked out.")

    db.close()

# View attendance records for a specific employee
def view_attendance():
    db = connect_to_db()
    cursor = db.cursor()

    emp_id = int(input("Enter Employee ID to view attendance: "))

    query = "SELECT * FROM attendance WHERE employee_id = %s"
    cursor.execute(query, (emp_id,))
    records = cursor.fetchall()

    print("Attendance Records:")
    print("ID | Employee ID | Clock In Time | Clock Out Time")
    print("-----------------------------------------------")
    for row in records:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

    db.close()



# Menu-driven system
def menu():
    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Clock In")
        print("6. Clock Out")
        print("7. View Attendance")
        print("8. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_employee()
        elif choice == 2:
            view_employees()
        elif choice == 3:
            update_employee()
        elif choice == 4:
            delete_employee()
        elif choice == 5:
            clock_in()
        elif choice == 6:
            clock_out()
        elif choice == 7:
            view_attendance()
        elif choice == 8:
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")



# Main function that runs the login system first
def main():
    print("Welcome to the Employee Management System")
    login_attempts = 3
    while login_attempts > 0:
        if login():
            menu()
            break
        else:
            login_attempts -= 1
            print(f"Remaining attempts: {login_attempts}")
    else:
        print("Too many failed login attempts. Exiting system.")

# Run the program
if __name__ == "__main__":
    main()
