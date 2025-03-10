import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create table
    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int,
            fullname varchar(255),
            telegram_id varchar(20) UNIQUE,
            language varchar(3),
            role varchar(50),
            PRIMARY KEY (id)
            );
"""
        try:
            self.execute(sql, commit=True)
            print("Users jadvali yaratildi!")
        except sqlite3.Error as e:
            print(f"Xatolik: {e}")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, role: str, telegram_id: str = None, language: str = 'uz' ):
        sql = """
        INSERT INTO Users(id, fullname, telegram_id, language, role) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, telegram_id, language, role), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    def update_user_fullname(self, email, telegram_id):

        sql = f"""
        UPDATE Users SET fullname=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(fullname, id), commit=True)
    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def get_fullname(self, telegram_id: int):
        sql = """
        SELECT * FROM Users WHERE telegram_id = ?
        """
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def create_table_class(self):
        sql = """
        CREATE TABLE Classes (
            id int,
            class_id int,
            class_name varchar(255),
            teacher_id int,
            teacher_name varchar(255),
            PRIMARY KEY (id,teacher_id)
);"""

        self.execute(sql, commit=True)

    def add_class(self, id:int, class_id:int, class_name: str, teacher_id: int, teacher_name: str,):
        sql = """
         INSERT INTO Classes(id, class_id, class_name, teacher_id, teacher_name) VALUES(?, ?, ?, ?,?)
         """
        self.execute(sql, parameters=(id, class_id, class_name, teacher_id, teacher_name,), commit=True)

    def select_all_class(self):
        sql = """
        SELECT * FROM Classes
        """
        return self.execute(sql, fetchall=True)

    def select_all_classes(self, class_id:int):
        sql = """
        SELECT * FROM Classes WHERE class_id = ?"""

        return self.execute(sql, parameters=(class_id,), fetchone=True)

    def count_classes(self):
        return self.execute("SELECT COUNT(*) FROM Classes;",fetchone=True)[0]

    def create_table_attendance(self):
        sql = """
        CREATE TABLE Attendance (
            id int,
            class_id int,
            student_id int,
            student_name varchar(255),
            created_at timestamp,
            status varchar(255)
        );
        """
        try:
            self.execute(sql, commit=True)
        except sqlite3.Error as e:
            print(f'Xatooooooooooo:{e}')
    def add_attendance(self, id:int, class_id: int, student_id: int,created_at:str, status: str):

        sql ="""
        INSERT INTO Attendance(id,class_id,student_id,created_at,status) VALUES(?,?,?,?,?)
        """

        self.execute(sql, parameters=(id,class_id,student_id,created_at,status), commit=True)

    def add_only_data(self, created_at:str):

        sql="""
        INSERT INTO Attendance(created_at) VALUES(?)"""

        self.execute(sql, parameters=(created_at,), commit=True)

    def create_table_tasks(self):
        sql = """
            CREATE TABLE Tasks(
            id int,
            task_title varchar(255),
            task_description varchar(255),
            created_at timestamp,
            class_id int,
            PRIMARY KEY(id)
            );
            """
        self.execute(sql, commit=True)

    def add_tasks(self, id: int, task_title: str, task_description: str, created_at:int, class_id:int):

        sql = """
        INSERT INTO Tasks(id,task_title,task_description,created_at,class_id) VALUES(?,?,?,?,?)
        """

        self.execute(sql, parameters=(id,task_title,task_description,created_at,class_id), commit=True)

    def select_all_task(self):
        sql = "SELECT * FROM Tasks"
        return self.execute(sql, fetchall=True)

    def select_task(self, class_id:int):
        sql = "SELECT * FROM Tasks WHERE class_id = ?"
        return self.execute(sql,parameters=(class_id,), fetchone=True)


    def create_table_submission(self):
        sql = """
            CREATE TABLE Submission(
            id int,
            student_id int,
            student_name varchar(255),
            task_id int,
            class_id int,
            teacher_id int,
            status varchar(255),
            file_url varchar(255),
            PRIMARY KEY(id)
            );
            """

        self.execute(sql, commit=True)

    def add_submission(self, id, student_id: int, student_name: str, task_id: int, class_id: int, teacher_id: int,
                       file_url: str):
        sql = """
        INSERT INTO Submission(id,student_id, student_name, task_id, class_id, teacher_id, status, file_url) 
        VALUES (?,?, ?, ?, ?, ?, 'submitted', ?)
        """
        self.execute(sql, parameters=(id,student_id, student_name, task_id, class_id, teacher_id, file_url), commit=True)

    def update_submission_status(self, student_id: int, task_id: int):
        sql = """
        UPDATE Submission 
        SET status = 'submitted'
        WHERE student_id = ? AND task_id = ?
        """
        self.execute(sql, parameters=(student_id, task_id), commit=True)

    def select_all_submission(self):
        sql = """SELECT * FROM Submission"""

        return self.execute(sql,fetchall=True)

    def select_submission_from_id(self, id:int):
        sql = "SELECT * FROM Submission WHERE id = ?"

        return self.execute(sql, parameters=(id,),fetchone=True)

    def select_submission_from_student_id(self,student_id:int):
        sql = "SELECT * FROM Submission WHERE student_id = ?"

        return self.execute(sql,parameters=(student_id,), fetchone=True)

    def create_table_checking(self):
        sql = """
            CREATE TABLE Taskcheck(
            id int,
            teacher_id int,
            teacher_name varchar(255),
            student_id int,
            student_name varchar(255),
            checked varchar(255),
            feedback varchar(255),
            grade int,
            status varchar(255),
            PRIMARY KEY(id)
            );
            """

        try:
            self.execute(sql, commit=True)
            print("Taskcheck jadvali yaratildi yoki mavjud.")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")

    def add_taskcheck(self, id:int , teacher_id:int, teacher_name:str, student_id:int, student_name:str, checked:str, feedback:str,grade:int,status:str):
        sql = """
        INSERT INTO Taskcheck(id, teacher_id, teacher_name, student_id, student_name, checked, feedback,grade,status) VALUES(?,?,?,?,?,?,?,?,?)
        """

        self.execute(sql, parameters=(id, teacher_id, teacher_name, student_id, student_name, checked, feedback,grade,status), commit=True)

    def create_table_notification(self):
        sql = """
            CREATE TABLE Notification(
            id int,
            telegram_id int,
            teacher_id int,
            notify_user varchar(255),
            is_read varchar(255),
            PRIMARY KEY(id)
            );
            """

        self.execute(sql, commit=True)

    def add_notification(self, id: int, telegram_id: int, teacher_id: int, notify_user: str, is_read: str):
        sql = """
        INSERT INTO Notification(id, telegram_id, teacher_id, notify_user, is_read) 
        VALUES(?, ?, ?, ?, ?)
        """

        self.execute(sql, parameters=(id, telegram_id, teacher_id, notify_user, is_read), commit=True)

    def create_table_message(self):
        sql = """
            CREATE TABLE Messages(
            id int,
            sender_id int,
            receiver_id int,
            message varchar(255),
            PRIMARY KEY(id)
            );
            """
        self.execute(sql, commit=True)

    def add_message(self, id: int, sender_id: int, receiver_id: int, message: str):
        sql = """
        INSERT INTO Messages(id, sender_id, receiver_id, message) 
        VALUES(?, ?, ?, ?)
        """

        self.execute(sql, parameters=(id, sender_id, receiver_id, message), commit=True)

    def create_table_files(self):
        sql = """
        CREATE TABLE Files(
        id int,
        file_url varchar(255),
        created_at timestamp,
        PRIMARY KEY(id)
        );"""

        self.execute(sql, commit=True)

    def add_file(self, id: int, file_url: str, created_at: str):
        sql = """
        INSERT INTO Files(id, file_url, created_at) 
        VALUES(?, ?, ?)
        """

        self.execute(sql, parameters=(id, file_url, created_at), commit=True)

    def create_table_rating(self):
        sql = """
        CREATE TABLE Rating(
        id int,
        class_id int,
        student_id int,
        rating_groups int,
        rating_students int,
        PRIMARY KEY(id)
        );"""

        self.execute(sql, commit=True)

    def add_rating(self, id: int, class_id: int, student_id: int, rating_groups: int, rating_students: int):
        sql = """
        INSERT INTO Rating(id, class_id, student_id, rating_groups, rating_students) 
        VALUES(?, ?, ?, ?, ?)
        """

        self.execute(sql, parameters=(id, class_id, student_id, rating_groups, rating_students), commit=True)

    def create_table_sinfo(self):
        sql = """
        CREATE TABLE Student(
        id int,
        group_id int,
        group_name varchar(255),
        teacher_name varchar(255),
        student_id int,
        student_name varchar(255),
        PRIMARY KEY(id)
        );"""

        self.execute(sql, commit=True)

    def add_student(self, id: int, group_id:int, group_name: str, student_id: int, student_name: str, teacher_name:str):
        sql = """
        INSERT INTO Student(id,group_id, group_name, student_id, student_name, teacher_name) 
        VALUES(?, ?, ?, ?,?,?)
        """

        self.execute(sql, parameters=(id,group_id, group_name, student_id, student_name,teacher_name), commit=True)

    def select_info(self, student_id:int):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Student WHERE student_id = ? "
        return self.execute(sql, parameters=(student_id,), fetchone=True)

    def select_id_from_student(self, id:int):

        sql = """
        SELECT * FROM Student WHERE id = ?
        """

        return self.execute(sql, parameters=(id,), fetchone=True)

    def get_group_name(self):
        sql = "SELECT * FROM Student"
        return self.execute(sql, fetchall=True)

    def delete_info(self):
        self.execute("DELETE FROM Student WHERE TRUE", commit=True)

    def get_student_count(self):
        sql = "SELECT COUNT(id) FROM Student"
        result = self.execute(sql, fetchone=True)
        return result[0] if result else 0

    def get_students_by_group(self):
        sql = """
        SELECT student_id, student_name, group_id, group_name
        FROM Student
        ORDER BY group_id, student_name;
        """
        return self.execute(sql, fetchall=True)

    def count_students(self):
        return self.execute("SELECT COUNT(*) FROM Student;", fetchone=True)[0]


