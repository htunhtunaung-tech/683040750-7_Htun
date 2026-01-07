"""
Htun Htun Aung
683040750-7
"""

from datetime import datetime

# ===================== BASE CLASS =====================

class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id                 # weakly private
        self.__checked_out = False         # truly private

    def get_status(self):
        return "Checked out" if self.__checked_out else "Available"

    def check_out(self):
        if not self.__checked_out:
            self.__checked_out = True
            return True
        return False

    def return_item(self):
        if self.__checked_out:
            self.__checked_out = False
            return True
        return False



# ===================== BOOK CLASS =====================

class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0               # non-parameter attribute

    def set_pages(self, pages):
        self.pages_count = pages

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Status: {self.get_status()}")



# ===================== TEXTBOOK CLASS =====================

class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level

    def display_course_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print(f"Status: {self.get_status()}")



# ===================== MAGAZINE CLASS =====================

class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number

        now = datetime.now()
        self.month = now.month            # default current
        self.year = now.year

    def display_issue(self):
        print(f"Title: {self.title}")
        print(f"Issue No: {self.issue_number}")
        print(f"Date: {self.month}/{self.year}")
        print(f"Status: {self.get_status()}")



# ===================== TEST PROGRAM =====================

if __name__ == "__main__":

    print("--- LibraryItem Test ---")
    item = LibraryItem("Generic Item", "L001")
    print(item.get_status())

    item.check_out()
    print(item.get_status())

    item.return_item()
    print(item.get_status())


    print("\n--- Book Test ---")
    book = Book("Harry Potter", "B001", "J.K. Rowling")
    book.set_pages(350)

    book.display_info()

    book.check_out()
    book.display_info()

    book.return_item()
    book.display_info()


    print("\n--- TextBook Test ---")
    tb = TextBook("Linear Algebra", "T001",
                  "Howard Anton", "Math", "Year 1")

    tb.set_pages(500)
    tb.display_course_info()

    tb.check_out()
    tb.display_course_info()


    print("\n--- Magazine Test ---")
    mag = Magazine("Tech Monthly", "M001", 25)

    mag.display_issue()

    mag.check_out()
    mag.display_issue()
