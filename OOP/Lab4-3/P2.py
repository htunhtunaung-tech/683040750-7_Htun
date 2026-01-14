from datetime import date
from university_system import (
    Professor,
    Administrator,
    UndergraduateStudent,
    GraduateStudent
)

# ---------- Professor ----------
prof = Professor(
    "Dr. Smith", 50, date(1975, 5, 10), "O", True,
    "Computer Science", 2005,
    professorship=3, admin_position=1
)
prof.display_info()
print()

# ---------- Administrator ----------
admin = Administrator(
    "Ms. Johnson", 45, date(1980, 3, 15), "A", False,
    "Administration", 2010,
    admin_position=3
)
admin.display_info()
print()

# ---------- Undergraduate Student ----------
ug = UndergraduateStudent(
    "louis", 20, date(2005, 7, 23), "B", False,
    2023, "Digital Media Engineering", "Undergraduate",
    club="Programming Club"
)
ug.register_course("OOP")
ug.register_course("Data Structures")
ug.display_info()
print()

# ---------- Graduate Student ----------
grad = GraduateStudent(
    "Bob", 25, date(2000, 4, 5), "AB", False,
    2024, "Data Science", "Graduate",
    advisor_name="Dr. Smith"
)
grad.set_thesis("Machine Learning Optimization")
grad.set_proposal_date(date(2025, 1, 10))
grad.display_info()
print("Expected Graduation Year:", grad.get_graduation_date())
