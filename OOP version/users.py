# models.py
class User:
    def __init__(self, user_id, name, contact, password):
        self.user_id = user_id
        self.name = name
        self.contact = contact
        self.password = password

class Student(User):
    def __init__(self, user_id, name, contact, password, year_level, section):
        super().__init__(user_id, name, contact, password)
        self.year_level = year_level
        self.section = section

    def save(self, db):
        cursor = db.connect().cursor()
        query = """
            INSERT INTO students (student_id, name, year_level, section, contact, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.user_id, self.name, self.year_level, self.section, self.contact, self.password))
        cursor.connection.commit()
        cursor.close()

    @classmethod
    def login(cls, db, user_id, password):
        cursor = db.connect().cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE student_id=%s AND password=%s", (user_id, password))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return cls(
                user_id=data['student_id'],
                name=data['name'],
                contact=data['contact'],
                password=data['password'],
                year_level=data['year_level'],
                section=data['section']
            )
        return None

class Officer(User):
    def __init__(self, user_id, name, contact, password, position, year_level, section):
        super().__init__(user_id, name, contact, password)
        self.position = position
        self.year_level = year_level
        self.section = section

    def save(self, db):
        cursor = db.connect().cursor()
        query = """
            INSERT INTO officers (officer_id, name, position, contact_number, year_level, section, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (self.user_id, self.name, self.position, self.contact, self.year_level, self.section, self.password))
        cursor.connection.commit()
        cursor.close()

    @classmethod
    def login(cls, db, user_id, password):
        cursor = db.connect().cursor(dictionary=True)
        cursor.execute("SELECT * FROM officers WHERE officer_id=%s AND password=%s", (user_id, password))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return cls(
                user_id=data['officer_id'],
                name=data['name'],
                contact=data['contact_number'],
                password=data['password'],
                position=data['position'],
                year_level=data['year_level'],
                section=data['section']
            )
        return None
