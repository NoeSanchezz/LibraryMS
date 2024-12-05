# Library Management System (LMS)

This Library Management System (LMS) project provides a GUI-based interface for managing a library's books, users, and transactions. It connects to a SQLite database for data persistence.

## Features
- Add, update, and delete book records.
- Manage user accounts.
- Record and view loan transactions.
- Intuitive GUI interface.

## Prerequisites
Ensure your system meets the following requirements:
- Python 3.8 or higher installed.
- `pip` (Python package manager) installed.
- SQLite installed (default for most Python installations).
- Required Python libraries:
  - `tkinter` (default library in Python)
  - `sqlite3` (default library in Python)

## Installation

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/NoeSanchezz/LibraryMS.git
cd LibraryMS
```
### 2.Setting Up the Database  
To set up the database, you can generate the `LMS.sql` file by executing the following command in your terminal:  

```bash
sqlite3 LMS.db .dump > LMS.sql
```
### 3.Run GUI Application
To run the GUI you can execute `Python GUI.py`  command in your terminal
## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
