"""
Htun Htun Aung
683040750-7
"""


from datetime import date

# ===================== LEVEL 1 =====================
class Person:
    _counter = 0

    def __init__(self, name, age, birthdate, bloodgroup, is_married):
        self.name = name
        self.age = age
        self._birthdate = birthdate
        self._id = self.__generate_id()
        self.__bloodgroup = bloodgroup
        self.__is_married = is_married

    def __generate_id(self):
        Person._counter += 1
        return f"{date.today().year}{Person._counter:03d}"

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, ID: {self._id}")


# ===================== LEVEL 2 =====================
class Staff(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 department, start_year):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.department = department
        self.start_year = start_year
        self.tenure_year = self.__calculate_tenure()
        self.__salary = 0

    def __calculate_tenure(self):
        return date.today().year - self.start_year

    def set_salary(self, amount):
        self.__salary = amount

    def get_salary(self):
        return self.__salary

    def display_info(self):
        super().display_info()
        print(f"Department: {self.department}, Tenure: {self.tenure_year} years")


class Student(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 start_year, major, level, grade_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.start_year = start_year
        self.major = major
        self.level = level
        self.grade_list = grade_list if grade_list else []
        self.gpa = self.calculate_gpa_instance()
        self.__graduation_date = self.__calculate_graduation_date()

    @staticmethod
    def calculate_gpa(grade_list):
        grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        total_points = sum(c * grade_map[g] for c, g in grade_list)
        total_credits = sum(c for c, _ in grade_list)
        return total_points / total_credits if total_credits else 0

    def calculate_gpa_instance(self):
        return Student.calculate_gpa(self.grade_list)

    def __calculate_graduation_date(self):
        if self.level.lower() == "undergraduate":
            return self.start_year + 4
        return self.start_year + 2

    def display_info(self):
        super().display_info()
        print(f"Major: {self.major}, Level: {self.level}, GPA: {self.gpa:.2f}")


# ===================== LEVEL 3 =====================
class Professor(Staff):
    PROFESSORSHIP = {
        0: "Lecturer",
        1: "Assistant Professor",
        2: "Associate Professor",
        3: "Full Professor",
        4: "Highest Full Professor"
    }

    def __init__(self, *args, professorship, admin_position=0):
        super().__init__(*args)
        self.professorship = professorship
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        salary = (
            30000 +
            self.tenure_year * 1000 +
            self.professorship * 10000 +
            self.admin_position * 10000
        )
        super().set_salary(salary)

    def display_info(self):
        super().display_info()
        print(f"Position: {Professor.PROFESSORSHIP[self.professorship]}, "
              f"Salary: {self.get_salary()}")


class Administrator(Staff):
    ADMIN_LEVEL = {
        0: "Entry",
        1: "Professional",
        2: "Expert",
        3: "Manager",
        4: "Director"
    }

    def __init__(self, *args, admin_position):
        super().__init__(*args)
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        salary = (
            15000 +
            self.tenure_year * 800 +
            self.admin_position * 5000
        )
        super().set_salary(salary)

    def display_info(self):
        super().display_info()
        print(f"Admin Level: {Administrator.ADMIN_LEVEL[self.admin_position]}, "
              f"Salary: {self.get_salary()}")


class UndergraduateStudent(Student):
    def __init__(self, *args, club=None, course_list=None):
        super().__init__(*args)
        self.club = club
        self.course_list = course_list if course_list else []

    def register_course(self, course):
        self.course_list.append(course)

    def display_info(self):
        super().display_info()
        print(f"Club: {self.club}, Courses: {self.course_list}")


class GraduateStudent(Student):
    def __init__(self, *args, advisor_name):
        super().__init__(*args)
        self.advisor_name = advisor_name
        self.thesis_name = None
        self.__proposal_date = None

    def _calculate_graduation_date(self):
        if self.__proposal_date:
            return self.__proposal_date.year + 1
        return date.today().year + 2

    def set_thesis(self, thesis_name):
        self.thesis_name = thesis_name

    def set_proposal_date(self, proposal_date):
        self.__proposal_date = proposal_date
        self._Student__graduation_date = self._calculate_graduation_date()

    def get_proposal_date(self):
        return self.__proposal_date

    def get_graduation_date(self):
        return self._Student__graduation_date

    def display_info(self):
        super().display_info()
        print(f"Advisor: {self.advisor_name}, Thesis: {self.thesis_name}")
