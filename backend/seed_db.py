from models import db, Student

# Example function to seed the database
def seed_database():
    # Add initial data
    student1 = Student(name='John Doe', age=16, risk_level='Medium')
    student2 = Student(name='Jane Smith', age=17, risk_level='High')

    db.session.add(student1)
    db.session.add(student2)
    db.session.commit()

    print("Database seeded with initial data.")

if __name__ == "__main__":
    seed_database() 