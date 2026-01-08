"""
Htun Htun Aung
683040750-7
"""

from Library_Items import Book, TextBook, Magazine

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
