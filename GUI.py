
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


print("Connected to the DB Successfully")

root = Tk()
root.title('LMS')
root.geometry('800x800')
root.configure(bg = '#333333')


style = ttk.Style()

style.theme_use('default')
style.configure('TNotebook',background = '#333333',borderwidth =0)
style.configure('TNotebook.Tab',background = '#444444',fg ='white',padding = [10,5])
style.map('TNotebook.Tab', background = [('selected','#555555')])


notebook = ttk.Notebook(root)
notebook.pack(fill='both',expand=True)


tab1=Frame(notebook,bg ='#333333')
notebook.add(tab1,text='Introduction')


Title =Label(tab1,text="Library Management System (LMS)",font=("Arial",16),bg ='#333333',fg = 'white').pack(expand=True)
Button(tab1,text="End", width=25,command= root.destroy).pack(pady=10)
# ****** Check Out Book Section ******
tab2=Frame(notebook,bg ='#333333')
notebook.add(tab2,text='Check Out Book')

Label(tab2,text="Check Out a book",font=("Arial",16),bg ='#333333',foreground = 'white').pack(pady=10)

Label(tab2,text="Borrower ID",bg ='#333333',foreground = 'white').pack()
borrower_id_entry = Entry(tab2)
borrower_id_entry.pack(pady=10)

Label(tab2,text="Book ID",bg ='#333333',foreground = 'white').pack(pady=10)
book_id_entry_tab2 = Entry(tab2)
book_id_entry_tab2.pack()


def checkout_book():
    conn = sqlite3.connect('LMS.db', timeout=10)
    cursor= conn.cursor()
    
    book_id = book_id_entry_tab2.get()
    borrower_id = borrower_id_entry.get()
    print(f"The book ID: {book_id}")
    print(f"Checking out book for Borrower ID: {borrower_id}")
    

     
    cursor.execute(
        "SELECT COUNT(*) FROM BOOK_LOANS WHERE book_id = ? AND branch_id = 1 AND card_no = ?",
        (book_id, borrower_id)
    )
    result = cursor.fetchone()
    print(result[0])
        
    if result[0] > 0:
        messagebox.showerror("Loan Error", "This book is already loaned out to this borrower.")
        return
    
    
    cursor.execute(
        "INSERT INTO BOOK_LOANS (book_id, branch_id, card_no, date_out, due_date, Returned_date) "
        "VALUES (?, 1, ?, DATE('now'), DATE('now', '+14 days'), NULL)",
        (book_id, borrower_id)
    )

    
    cursor.execute("SELECT * FROM BOOK_COPIES WHERE book_id = ?", (book_id,))
    records = cursor.fetchall()

    
    if records:
        print_records = "Book ID\tBranch ID\t [Updated] Number of Copies\n"
        print_records += "\n".join([f"{record[0]}\t{record[1]}\t {record[2]}" for record in records])
        print_records += "\n_____________________________________________"
    else:
        print_records = "No Records found."

        
    table = Label(tab2, text=print_records, bg='#333333', fg='white', justify='left', anchor='w')
    table.pack(pady=10)
    

        
    
    conn.commit()
    messagebox.showinfo("Success", "Book checked out successfully!")
    if conn:
        conn.close()
   

Button(tab2,text="Check Book",bg ='#333333',foreground = 'white',command=checkout_book).pack(pady=10)

# ****** Check Out Book Section ******

# ****** New Borrower Section ******
tab3=Frame(notebook,bg ='#333333')
notebook.add(tab3,text='New Borrower')

Label(tab3,text="Register a new library card",bg ='#333333',foreground = 'white').pack()

Label(tab3,text="Name",bg ='#333333',foreground = 'white').pack(pady=10)
name_entry = Entry(tab3)
name_entry.pack()

Label(tab3,text="Address",bg ='#333333',foreground = 'white').pack(pady=10)
Address_entry = Entry(tab3)
Address_entry.pack()

Label(tab3,text="Phone",bg ='#333333',foreground = 'white').pack(pady=10)
Phone_entry = Entry(tab3)
Phone_entry.pack()

def new_borrower():
    conn = sqlite3.connect('LMS.db', timeout=10)
    cursor= conn.cursor()
    
    Name = name_entry.get().lower()
    Address = Address_entry.get()
    Phone = Phone_entry.get()
    
     
    cursor.execute("""
                   SELECT COUNT(*) 
                   FROM BORROWER AS BR
                   WHERE FName = ?;
                   """,(Name,))
    Name_exist = cursor.fetchone()[0]
    if Name_exist > 0:
        messagebox.showerror("OOPS!", "That name is already taken")
        return
    
    
    cursor.execute("""
                   SELECT COUNT(*)
                   FROM BORROWER AS BR 
                   WHERE Phone = ?;  
                   """,(Phone,))
    Phone_exist = cursor.fetchone()[0]
    if Phone_exist > 0:
        messagebox.showerror("OOPS!", "That phone number is already registered")
        return
    
       
    cursor.execute("""
        SELECT COUNT(*)
        FROM BORROWER 
        WHERE B_Address = ?;
    """, (Address,))
    Address_exist = cursor.fetchone()[0]
    
    if Address_exist > 0:
        messagebox.showinfo("Note", "This address is already registered. Proceeding with new borrower registration.")
    
    
    def check_card_exists():
        while True:
            card_no = randint(10000, 100000)
            cursor.execute("""
                SELECT COUNT(*)
                FROM BORROWER
                WHERE Card_No = ?;
            """, (card_no,))
            if cursor.fetchone()[0] == 0:
                return card_no

    card_no = check_card_exists()

    
    cursor.execute("""
        INSERT INTO BORROWER (Card_No, FName, B_Address, Phone)
        VALUES (?, ?, ?, ?)
        """, (card_no, Name, Address, Phone))
    
    conn.commit()

    
    cursor.execute("""
        SELECT Card_No, FName, B_Address, Phone
        FROM BORROWER
        WHERE Card_No = ?;
    """, (card_no,))
    
    result = cursor.fetchall()
    if result:
        result_str = "Library Card\n"
        for LibraryID, Borrower_Name, Borrower_Address, Borrower_Phone in result:
            result_str += f"Borrwer:{Borrower_Name}\nAddress:{Borrower_Address}\nPhone:{Borrower_Phone}\n\nCard Number: {LibraryID}"
            result_str += "\n---------------------------------------\n"
            messagebox.showinfo("Library Card", result_str)
    else:
        messagebox.showerror("Error!", "Invalid register information")
        
    conn.commit()
    conn.close() 
    messagebox.showinfo("Success!", "You have been successfully registered")

Button(tab3,text="Submit",bg ='#333333',foreground = 'white',command=new_borrower).pack(pady=10)
    
# ****** New Borrower Section ******

# ****** New Book W/ publisher Section ******

tab4=Frame(notebook,bg ='#333333')
notebook.add(tab4,text='New Book W/ publisher')

Label(tab4,text="Book ID",bg ='#333333',foreground = 'white').pack(pady=10)
book_id_entry_tab4 = Entry(tab4)
book_id_entry_tab4.pack()

Label(tab4,text="Book's Name",bg ='#333333',foreground = 'white').pack(pady=10)
Book_name_entry = Entry(tab4)
Book_name_entry.pack()

Label(tab4,text="Author's Name",bg ='#333333',foreground = 'white').pack(pady=10)
author_name_entry = Entry(tab4)
author_name_entry.pack()

Label(tab4,text="Publisher's Name",bg ='#333333',foreground = 'white').pack(pady=10)
Publisher_name_entry = Entry(tab4)
Publisher_name_entry.pack()

def New_Book_Pub():
    conn = sqlite3.connect('LMS.db', timeout=10)
    cursor= conn.cursor()
    Book_id_New = book_id_entry_tab4.get()
    Book_name = Book_name_entry.get()
    Publisher_name = Publisher_name_entry.get().lower()
    author_name = author_name_entry.get()

    
    cursor.execute("SELECT COUNT(*) FROM BOOK WHERE Book_id = ?",(Book_id_New,))
    book_id_exist = cursor.fetchone()[0]
    if book_id_exist >0:
        messagebox.showerror("Book Id ERROR","This Book Id already exist in the database")
        return
    

     
    cursor.execute("SELECT COUNT(*) FROM PUBLISHER WHERE LOWER(Publisher_name) = ?",(Publisher_name,))
    publisher_exist = cursor.fetchone()[0]
    if not publisher_exist:
        messagebox.showerror("Publisher ERROR","The publisher does not exist in the database.")
        conn.close()
        return
    
    cursor.execute("INSERT INTO BOOK (Book_id, Title,Publisher_name) VALUES (?,?,?) ",(Book_id_New,Book_name,Publisher_name,))

    
    cursor.execute("INSERT INTO BOOK_AUTHORS (Book_id, Author_name) VALUES (?,?)",(Book_id_New,author_name,))
    
    for branch_id in range(1,6):
        cursor.execute("SELECT COUNT(*) FROM BOOK_COPIES WHERE Book_id = ? AND Branch_id = ?",(Book_id_New,branch_id))
        book_copy_exists = cursor.fetchone()[0]
        if not book_copy_exists:
            cursor.execute("INSERT INTO BOOK_COPIES (Book_id, Branch_id, No_of_copies) VALUES(?,?,?)", 
                           (Book_id_New, branch_id, 5))
        result = cursor.fetchall()
        
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "New book with copies added to all branches successfully")

Button(tab4,text="Submit",bg ='#333333',foreground = 'white',command = New_Book_Pub ).pack(pady=10)
# ****** New Book W/ publisher Section ******

# ****** Book Inventory Section ******

tab5=Frame(notebook,bg ='#333333')
notebook.add(tab5,text='Book Loan')

Label(tab5,text="Book Title",bg ='#333333',foreground = 'white').pack(pady=10)
book_Title_entry = Entry(tab5)
book_Title_entry.pack()

def Book_title_inv():
    conn = sqlite3.connect('LMS.db', timeout=10)
    cursor= conn.cursor()
    book_title = book_Title_entry.get().lower()
    
    cursor.execute("SELECT COUNT(*) FROM BOOK WHERE LOWER(Title) = ?",(book_title,))
    book_Title_exist = cursor.fetchone()[0]
    
    if book_Title_exist == 0:
        messagebox.showerror("Book Title ERROR","This Book does not exist in this database")
        return
    else:
        cursor.execute(
            """
            SELECT bl.Branch_id, COUNT(bl.Book_id)
            FROM BOOK_LOANS AS bl 
            JOIN BOOK AS b ON bl.Book_id = b.Book_id 
            JOIN BOOK_COPIES AS BC on bl.Book_id = BC.Book_id AND bl.Branch_id = BC.Branch_id 
            WHERE LOWER(b.Title) = ? 
            GROUP BY bl.Branch_id """,
            (book_title,))
        results = cursor.fetchall()
        
    if results:
        result_str = "Number of copies loaned out per branch:\n"
        for branch_id, count in results:
            result_str += f"Branch {branch_id}: {count} copies\n"
        messagebox.showinfo("Results", result_str)
    else:
        messagebox.showinfo("No Results", "No loans found for this book title.")
        
    conn.commit()
    conn.close()
Button(tab5,text="Submit",bg ='#333333',foreground = 'white',command=Book_title_inv).pack(pady=10)

# ****** Book Inventory Section ******

# ****** Late Loans Section ******
tab6=Frame(notebook,bg ='#333333')
notebook.add(tab6,text='Late Loans')

Label(tab6,text="Start date",bg ='#333333',foreground = 'white').pack(pady=10)
Label(tab6,text="Please use (yyyy-mm-dd) format",bg ='#333333',foreground = 'white').pack(pady=10)

Start_entry = Entry(tab6)
Start_entry.pack()

Label(tab6,text="End date",bg ='#333333',foreground = 'white').pack(pady=10)
End_entry = Entry(tab6)
End_entry.pack()

def get_late():
    conn=sqlite3.connect('LMS.db', timeout=10)
    cursor = conn.cursor()
    start_date = Start_entry.get()
    End_date = End_entry.get()

    
    cursor.execute("SELECT CASE WHEN ? > ? THEN 1 ELSE 0 END",(start_date,End_date,))
    invalid_flag =cursor.fetchone()[0]

    if invalid_flag == 1:
        messagebox.showerror("Date Error","The start date cannot be later than the due date")
        return
    
   
    cursor.execute(
        """
        SELECT bl.book_id, bl.branch_id, bl.card_no, bl.date_out, bl.due_date,
        CASE 
            WHEN bl.Returned_date > bl.due_date THEN JULIANDAY(bl.Returned_date) - JULIANDAY(bl.due_date)
        ELSE 0 
        END AS Late_days
        FROM BOOK_LOANS AS bl 
        WHERE  bl.Returned_date IS NOT NULL AND bl.Returned_date > bl.due_date AND bl.due_date BETWEEN ? AND ?""",
        (start_date,End_date))
    results = cursor.fetchall()
    
    if results:
        results_str = "Late Book Loans within the Due Date Range \n"
        for book_id, branch_id, card_no, date_out, due_date, late_days in results:
                results_str += f" Book ID: {book_id}\nBranch ID: {branch_id}\nCard ID: {card_no}\nDate Out: {date_out}\nDue Date: {due_date}\nLate Days: {late_days}\n----------------------------------\n"
        messagebox.showinfo("Late Book Loans",results_str)
    else:
        messagebox.showinfo("No results", "No late book loans found within the Date Range\n")
    conn.commit()
    conn.close()

Button(tab6,text="Submit",bg ='#333333',foreground = 'white',command=get_late).pack(pady=10)


# ****** Late Loans Section ******

# ****** Late Fee Balances Section ******

tab7=Frame(notebook,bg ='#333333')
notebook.add(tab7,text='View Balance Statement')

    # Late Fee Balances:
Label(tab7,text="Late Fee Balance",bg ='#333333',foreground = 'white')

Label(tab7,text="Borrower's ID",bg ='#333333',foreground = 'white').pack(pady=10)
borrower_id_entry_tab7 = Entry(tab7)
borrower_id_entry_tab7.pack()

Label(tab7,text="Borrower's Name",bg ='#333333',foreground = 'white').pack(pady=10)
borrower_name_entry_tab7 = Entry(tab7)
borrower_name_entry_tab7.pack()

def BR_late_fee_balance():
    conn = sqlite3.connect('LMS.db',timeout=10)
    cursor = conn.cursor()
    Borrower_ID = borrower_id_entry_tab7.get()
    Borrower_NAME = borrower_name_entry_tab7.get().lower()
    
    if Borrower_ID and not Borrower_NAME:
        cursor.execute("SELECT Card_No,FName,LateFeeBalance FROM vBookLoanInfo WHERE Card_no = ?", (Borrower_ID,))
        results = cursor.fetchall()
    elif not Borrower_ID and Borrower_NAME:
        cursor.execute("SELECT Card_No,FName,LateFeeBalance FROM vBookLoanInfo WHERE FName Like ?", (f"%{Borrower_NAME}%",))
        results = cursor.fetchall()
    elif Borrower_ID and Borrower_NAME:
        cursor.execute("SELECT Card_No,FName,LateFeeBalance FROM vBookLoanInfo WHERE FName Like ? and Card_No = ?", (f"%{Borrower_NAME}%", Borrower_ID))
        results = cursor.fetchall()
    else:
        cursor.execute("SELECT Card_No,FName,LateFeeBalance FROM vBookLoanInfo ORDER BY LateFeeBalance;")
        results = cursor.fetchall()
    
    if results:  
        results_str = "Book Loan Info\n"
        for Card_No, FName, LateFeeBalance in results:
            
        
            if LateFeeBalance is None or LateFeeBalance == 0:
                LateFeeBalance = 0.00
        
            results_str += (f"Borrower ID: {Card_No}\nBorrower Name: {FName}\nBalance Due: ${LateFeeBalance:.2f}\n--------------------------------------\n")
        messagebox.showinfo("Balance Statement", results_str)
    else:
        messagebox.showinfo("Balance Statement", "No records found.")
    conn.commit()
    conn.close()

Button(tab7,text="Submit",bg ='#333333',foreground = 'white',command=BR_late_fee_balance).pack(pady=10)


#  **** Sect 6 View Book Information ****
tab8=Frame(notebook,bg ='#333333')
notebook.add(tab8,text='View Book Information')

Label(tab8,text="Book Info",bg ='#333333',foreground = 'white').pack()
Label(tab8,text="provide with a registered Borrower ID",bg ='#333333',foreground = 'white').pack(pady=10)

Label(tab8,text="Borrower's ID",bg ='#333333',foreground = 'white').pack(pady=10)
borrower_id_entry_tab8 = Entry(tab8)
borrower_id_entry_tab8.pack()

Label(tab8,text="Book ID",bg ='#333333',foreground = 'white').pack(pady=10)
book_id_entry_tab8 = Entry(tab8)
book_id_entry_tab8.pack()
    
Label(tab8,text="Book Title",bg ='#333333',foreground = 'white').pack(pady=10)
book_title_entry_tab8 = Entry(tab8)
book_title_entry_tab8.pack()

def View_Book_Info():
    conn = sqlite3.connect('LMS.db',timeout=10)
    cursor = conn.cursor()
    Borrower_ID = borrower_id_entry_tab8.get()
    Book_ID = book_id_entry_tab8.get()
    Book_Name = book_title_entry_tab8.get().lower()
    
    cursor.execute("SELECT COUNT(*) FROM vBookLoanInfo WHERE Card_no = ?", (Borrower_ID,))
    borrower_id_exist = cursor.fetchone()[0]
    if borrower_id_exist == 0:
        messagebox.showerror("Error, provide a valid Borrower ID or register a new Borrower ID")
        return
    
    
    Usersearch_params = [Borrower_ID]
    query = """
        SELECT BL.Card_no AS BorrowerID, B.title AS BookTitle,BL.Book_id AS BookID,
        CASE 
            WHEN LB.LateFee IS NULL THEN 'Non-Applicable'
            ELSE LB.LateFee
        END AS LateFee
        FROM BOOK_LOANS AS BL
        JOIN BOOK AS B ON BL.Book_id = B.book_id
        JOIN LIBRARY_BRANCH AS LB ON BL.Branch_id = LB.Branch_Id
        WHERE BL.Card_no = ?
        """

    if Book_ID:
        query += " AND BL.Book_id = ?"
        Usersearch_params.append(Book_ID)
    if Book_Name:
        query += " AND LOWER(B.title) LIKE ?"       
        Usersearch_params.append(f"%{Book_Name.lower()}%")

    if not Book_ID and not Book_Name:
        query += " ORDER BY LB.LateFee DESC"

    cursor.execute(query, Usersearch_params)
    result = cursor.fetchall()

    if result:
        results_str = "Book Information:\n"
        for BorrowerID, BookTitle, BookID, LateFee in result:
            if LateFee == 'Non-Applicable':
                results_str += (f"Borrower ID: {BorrowerID}\nBook Title: {BookTitle}\nBook ID: {BookID}\nLate Fee per day: {LateFee}\n--------------------------------------\n")
            else:
                results_str += (f"Borrower ID: {BorrowerID}\nBook Title: {BookTitle}\nBook ID: {BookID}\nLate Fee per day: ${LateFee:.2f}\n--------------------------------------\n")

        messagebox.showinfo("Book Information", results_str)
    else:
        messagebox.showinfo("Book Information", "No records found.")

    conn.commit()
    conn.close()

Button(tab8,text="Submit",bg ='#333333',foreground = 'white',command=View_Book_Info).pack(pady=10)


# ****** Sect 6 View Book Information ******

root.mainloop()