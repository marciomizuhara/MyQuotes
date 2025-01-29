# 📚 My Quotes - Quote Management System

**My Quotes** is a web-based application designed to manage, organize, and visualize Kindle Highlights efficiently.

---

## 🖼️ Application Previews

### Quotes Table
![Quotes Table](static/images/Screenshot_383.png)

### Characters Page
![Characters Page](static/images/Screenshot_385.png)

### Book Gallery
![Book Gallery](static/images/Screenshot_384.png)

### Detailed Book View
![Detailed Book View](static/images/Screenshot_386.png)

---

## 🚀 Key Features

- **Random Quotes:** Display random quotes from your collection.
- **All Quotes:** Browse your complete library of saved quotes.
- **Books View:** Explore quotes grouped by book covers in a visual gallery.
- **Search Functionality:** Quickly search quotes, books, or authors.
- **Type Filters:** Filter quotes by categories (e.g., green, red, blue, yellow).
- **Notes Management:** Add, edit, or delete personal notes for each quote.
- **Interactive Table View:** View and manage quotes in an organized table format.
- **Dynamic Grid View:** Visualize book covers in a clean and modern grid layout.

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Libraries:** Pandas (for data processing), SQLAlchemy (ORM)

## 📥 Data Import

- Supports importing Kindle highlights from a `.txt` file.
- Automatically processes and categorizes quotes.
- Prevents duplicate entries in the database.

## 💾 Data Organization

- **Books Table:** Stores book titles, authors, and cover URLs.
- **Quotes Table:** Stores quotes, page numbers, types, and notes.
- **Relationships:** Quotes are linked to their respective books.

## ⚙️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/marciomizuhara/MyQuotes.git
   cd your-repo
