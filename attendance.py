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
