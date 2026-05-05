import mysql.connector

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678", 
        database="schoolmanagement"
    )


def view_students():
    try:
        db = connect_db()
        cursor = db.cursor()
        query = """
            SELECT StudentID, StudentName, 
                   COALESCE(BirthDate, 'Unknown'),
                   COALESCE(Address, 'Not Updated'),
                   COALESCE(ClassID, 'Unassigned')
            FROM Students
        """
        cursor.execute(query)
        print("\n--- STUDENT LIST ---")
        for row in cursor.fetchall():
            print(f"ID: {row[0]:<2} | Name: {row[1]:<12} | Class: {row[4]:<12} | DOB: {row[2]:<12} | Address: {row[3]}")
        db.close()
    except Exception as e:
        print(f"System Error: {e}")

def view_subjects():
    try:
        db = connect_db()
        cursor = db.cursor()
        # Truy vấn lấy mã môn và tên môn
        query = "SELECT SubjectID, SubjectName FROM Subjects LIMIT 50" 
        cursor.execute(query)
        
        print("\n" + "="*30)
        print("      SUBJECT DIRECTORY")
        print("="*30)
        for row in cursor.fetchall():
            print(f"ID: {row[0]:<4} | Subject Name: {row[1]}")
        db.close()
    except Exception as e:
        print(f"Error: {e}")


def view_teachers():
    try:
        db = connect_db()
        cursor = db.cursor()
        query = """
            SELECT t.TeacherID, t.TeacherName, 
                   COALESCE(s.SubjectName, 'Unassigned'),
                   COALESCE(t.Email, 'No Email')
            FROM Teachers t
            LEFT JOIN Subjects s ON t.SubjectID = s.SubjectID
        """
        cursor.execute(query)
        print("\n--- TEACHER LIST ---")
        for row in cursor.fetchall():
            print(f"ID: {row[0]:<2} | Name: {row[1]:<15} | Subject: {row[2]:<12} | Email: {row[3]}")
        db.close()
    except Exception as e:
        print(f"Error: {e}")

# ==========================================
# 4. GRADING MODULE (Calling Stored Procedure)
# ==========================================
def add_new_grade():
    try:
        std_id = int(input("Enter Student ID: "))
        sub_id = int(input("Enter Subject ID: "))
        score = float(input("Enter Score: "))
        
        db = connect_db()
        cursor = db.cursor()
        # Call the automated procedure created in MySQL
        cursor.callproc('AddNewGrade', [std_id, sub_id, score])
        db.commit()
        print("=> Grade added successfully! Class performance stats updated automatically via Trigger.")
        db.close()
    except ValueError:
        print("Error: Please enter a valid number!")
    except Exception as e:
        print(f"Database Error: {e}")

# ==========================================
# 5. REPORTING MODULE (Calling View)
# ==========================================
def view_class_performance():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.ClassName, p.TotalGrades, p.AverageScore 
            FROM ClassPerformance p 
            JOIN Classes c ON p.ClassID = c.ClassID
        """)
        print("\n--- CLASS PERFORMANCE REPORT ---")
        for row in cursor.fetchall():
            print(f"Class: {row[0]:<5} | Total Grades: {row[1]:<3} | Average Score: {row[2]}")
        db.close()
    except Exception as e:
        print(f"Error: {e}")

def update_student_info():
    try:
        db = connect_db()
        cursor = db.cursor()
        
        print("\n--- UPDATE STUDENT PROFILE ---")
        std_id = input("Enter Student ID to update: ")
        
        # Nhập thông tin mới (nếu không muốn đổi thì ấn Enter bỏ qua)
        new_address = input("Enter new Address (Press Enter to skip): ")
        new_dob = input("Enter new BirthDate (YYYY-MM-DD, Press Enter to skip): ")
        
        updated = False
        
        if new_address:
            cursor.execute("UPDATE Students SET Address = %s WHERE StudentID = %s", (new_address, std_id))
            updated = True
            
        if new_dob:
            cursor.execute("UPDATE Students SET BirthDate = %s WHERE StudentID = %s", (new_dob, std_id))
            updated = True
            
        if updated:
            db.commit() # Lưu thay đổi vào Database
            print(f"=> Successfully updated profile for Student ID {std_id}!")
        else:
            print("=> No changes were made.")
            
        db.close()
    except Exception as e:
        print(f"Error updating record: {e}")

def view_student_transcript():
    try:
        db = connect_db()
        cursor = db.cursor()
        
        print("\n--- VIEW STUDENT TRANSCRIPT ---")
        std_id = input("Enter Student ID: ")
        
        # Dùng JOIN để lấy Tên môn học, Tên giáo viên và Điểm của học sinh đó
        query = """
            SELECT sub.SubjectName, t.TeacherName, g.Score
            FROM Grades g
            JOIN Subjects sub ON g.SubjectID = sub.SubjectID
            JOIN Teachers t ON sub.SubjectID = t.SubjectID
            WHERE g.StudentID = %s
            ORDER BY sub.SubjectName
        """
        cursor.execute(query, (std_id,))
        results = cursor.fetchall()
        
        if results:
            print("\n" + "="*55)
            print(f" DETAILED TRANSCRIPT FOR STUDENT ID: {std_id}")
            print("="*55)
            print(f"{'Subject':<20} | {'Teacher':<20} | {'Score'}")
            print("-" * 55)
            for row in results:
                print(f"{row[0]:<20} | {row[1]:<20} | {row[2]}")
            print("="*55)
        else:
            print(f"=> No grades found for Student ID {std_id}. (This student might be Missing Data!)")
            
        db.close()
    except Exception as e:
        print(f"Error fetching transcript: {e}")

def update_teacher_info():
    try:
        db = connect_db()
        cursor = db.cursor()
        
        print("\n--- UPDATE TEACHER PROFILE ---")
        teacher_id = input("Enter Teacher ID to update: ")
        
        # Nhập thông tin mới (nếu không đổi thì ấn Enter bỏ qua)
        new_email = input("Enter new Email (Press Enter to skip): ")
        new_subject_id = input("Enter new Subject ID for reassignment (Press Enter to skip): ")
        
        updated = False
        
        if new_email:
            cursor.execute("UPDATE Teachers SET Email = %s WHERE TeacherID = %s", (new_email, teacher_id))
            updated = True
            
        if new_subject_id:
            cursor.execute("UPDATE Teachers SET SubjectID = %s WHERE TeacherID = %s", (new_subject_id, teacher_id))
            updated = True
            
        if updated:
            db.commit() # Lưu thay đổi
            print(f"=> Successfully updated profile for Teacher ID {teacher_id}!")
        else:
            print("=> No changes were made.")
            
        db.close()
    except Exception as e:
        print(f"Error updating teacher record: {e} - Note: Make sure the Subject ID exists!")

def view_students_by_teacher():
    try:
        db = connect_db()
        cursor = db.cursor()
        
        print("\n--- VIEW STUDENTS TAUGHT BY TEACHER ---")
        teacher_id = input("Enter Teacher ID: ")
        
        # Truy vấn tìm môn giáo viên dạy -> tìm điểm của môn đó -> suy ra học sinh
        query = """
            SELECT s.StudentID, s.StudentName, c.ClassName, g.Score
            FROM Teachers t
            JOIN Subjects sub ON t.SubjectID = sub.SubjectID
            JOIN Grades g ON sub.SubjectID = g.SubjectID
            JOIN Students s ON g.StudentID = s.StudentID
            JOIN Classes c ON s.ClassID = c.ClassID
            WHERE t.TeacherID = %s
            ORDER BY s.StudentName
        """
        cursor.execute(query, (teacher_id,))
        results = cursor.fetchall()
        
        if results:
            print("\n" + "="*60)
            print(f" STUDENTS TAUGHT BY TEACHER ID: {teacher_id}")
            print("="*60)
            print(f"{'Student ID':<12} | {'Student Name':<20} | {'Class':<10} | {'Score'}")
            print("-" * 60)
            for row in results:
                print(f"{row[0]:<12} | {row[1]:<20} | {row[2]:<10} | {row[3]}")
            print("="*60)
            print(f"Total students found: {len(results)}")
        else:
            print(f"=> No students found for Teacher ID {teacher_id}. (Maybe they haven't graded anyone yet!)")
            
        db.close()
    except Exception as e:
        print(f"Error fetching data: {e}")

def main():
    while True:
        print("\n" + "="*50)
        print(" SCHOOL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. View Student List (Handles Missing Data)")
        print("2. View Teacher List (Subject Assignments)")
        print("3. View Subject List (To get Subject ID)")
        print("4. Enter New Grade (Automated via Procedure)")
        print("5. View Class Performance Report")
        print("6. Update Student Information") 
        print("7. Update Teacher Information") 
        print("8. View Student Detailed Transcript") 
        print("9. View Students by Teacher") # <-- Chức năng mới thêm
        print("10. Exit System") # Đổi thành 10
        print("="*50)
        
        choice = input("\nEnter your choice (1-10): ")

        if choice == '1':
            view_students()
        elif choice == '2':
            view_teachers()
        elif choice == '3':
            view_subjects()
        elif choice == '4':
            add_new_grade()
        elif choice == '5':
            view_class_performance()
        elif choice == '6':
            update_student_info()
        elif choice == '7':
            update_teacher_info() # Gọi hàm update giáo viên
        elif choice == '8':
            view_student_transcript() 
        elif choice == '9':
            view_students_by_teacher() # Gọi hàm tra học sinh từ giáo viên
        elif choice == '10':
            print("Exiting system...")
            break
        
if __name__ == "__main__":
    main()