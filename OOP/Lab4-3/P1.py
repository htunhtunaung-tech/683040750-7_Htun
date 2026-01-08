"""
Htun Htun Aung
683040750-7
"""

from datetime import datetime

# ===================== BASE CLASS =====================
class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False

    def get_status(self):
        return "Checked out" if self._checked_out else "Available"

    def check_out(self):
        if not self._checked_out:
            self._checked_out = True
            return True
        return False

    def return_item(self):
        if self._checked_out:
            self._checked_out = False
            return True
        return False

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"ID: {self._id}")
        print(f"Status: {self.get_status()}")


# ===================== BOOK CLASS =====================
class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0

    def set_pages_count(self, pages):
        self.pages_count = pages

    def display_info(self):
        super().display_info()      # polymorphism
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")


# ===================== TEXTBOOK CLASS =====================
class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level

    def display_info(self):
        super().display_info()      # polymorphism
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")


# ===================== MAGAZINE CLASS =====================
class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number

        now = datetime.now()
        self.month = now.month
        self.year = now.year

    def display_info(self):
        super().display_info()      # polymorphism
        print(f"Issue Number: {self.issue_number}")
        print(f"Month: {self.month}")
        print(f"Year: {self.year}")


# ===================== POLYMORPHISM TEST =====================
items = [
    Book("Harry Potter", "B001", "J.K. Rowling"),
    TextBook("Physics", "T101", "Resnick", "Science", "Grade 10"),
    Magazine("National Geographic", "M202", 45)
]

items[0].set_pages_count(350)
items[1].set_pages_count(500)

for item in items:
    print("\n--- Item Info ---")
    item.display_info()
