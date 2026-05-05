import mysql.connector
import random
from datetime import datetime, timedelta

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678", 
        database="schoolmanagement"
    )

def random_null(value, probability=0.10):
    """Returns None with a given probability to simulate missing data."""
    return None if random.random() < probability else value

def generate_random_date():
    """Generates a random birth date for students."""
    start_date = datetime(2008, 1, 1)
    end_date = datetime(2011, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

# ==========================================
# 2. MAIN DATA GENERATION LOGIC
# ==========================================
def generate_sample_data():
    try:
        db = connect_db()
        cursor = db.cursor()

        # Temporarily disable foreign key checks to allow bulk truncate and insert
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Clear existing data to ensure exactly 510 rows
        print("Cleaning old data...")
        tables = ["Grades", "Students", "Classes", "Teachers", "Subjects"]
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table};")
        
        print("Generating 510 sample rows for each table...")

        # 1. Generate 510 Subjects
        subjects_data = [(f"Subject {i}",) for i in range(1, 511)]
        cursor.executemany("INSERT INTO Subjects (SubjectName) VALUES (%s)", subjects_data)
        print("✓ Subjects generated (510 rows).")

        # 2. Generate 510 Teachers (With missing emails)
        teachers_data = []
        for i in range(1, 511):
            name = f"Teacher {i}"
            sub_id = random_null(random.randint(1, 510), 0.05) 
            email = random_null(f"teacher{i}@school.edu", 0.15)
            teachers_data.append((name, sub_id, email))
        cursor.executemany("INSERT INTO Teachers (TeacherName, SubjectID, Email) VALUES (%s, %s, %s)", teachers_data)
        print("✓ Teachers generated (510 rows with Missing Data).")

        # 3. Generate 510 Classes (With unassigned teachers)
        classes_data = []
        for i in range(1, 511):
            class_name = f"Class {i}"
            teacher_id = random_null(random.randint(1, 510), 0.1)
            classes_data.append((class_name, teacher_id))
        cursor.executemany("INSERT INTO Classes (ClassName, TeacherID) VALUES (%s, %s)", classes_data)
        print("✓ Classes generated (510 rows with Missing Data).")

        # 4. Generate 510 Students (With missing details)
        students_data = []
        for i in range(1, 511):
            name = f"Student {i}"
            birth_date = random_null(generate_random_date(), 0.1)
            class_id = random_null(random.randint(1, 510), 0.05)
            address = random_null(f"City District {random.randint(1, 50)}", 0.15)
            students_data.append((name, birth_date, class_id, address))
        cursor.executemany("INSERT INTO Students (StudentName, BirthDate, ClassID, Address) VALUES (%s, %s, %s, %s)", students_data)
        print("✓ Students generated (510 rows with Missing Data).")

        # 5. Generate 510 Grades (With Data Anomalies / False Data)
        grades_data = []
        for i in range(1, 511):
            std_id = random.randint(1, 510)
            sub_id = random.randint(1, 510)
            
            # Inject False Data (5%) and Missing Data (10%)
            rand_val = random.random()
            if rand_val < 0.05:
                score = random.choice([-2.0, 15.0]) # Data Anomalies
            elif rand_val < 0.15:
                score = None # Missing Grade
            else:
                score = round(random.uniform(4.0, 10.0), 1) # Valid Grade
                
            grades_data.append((std_id, sub_id, score))
        cursor.executemany("INSERT INTO Grades (StudentID, SubjectID, Score) VALUES (%s, %s, %s)", grades_data)
        print("✓ Grades generated (510 rows with Data Anomalies).")

        # Re-enable foreign key checks and commit
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        db.commit()
        print("\nSUCCESS! All tables now contain exactly 510 rows as per project requirements.")

    except Exception as e:
        print(f"Error during data generation: {e}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    generate_sample_data()