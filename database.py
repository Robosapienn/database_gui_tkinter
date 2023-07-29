from tkinter import *
from tkinter import messagebox
import sqlite3

# Basic tkinter setup
root = Tk()
root.geometry("400x400")
root.title("Database Program")


# Create the submit functions for the database
def submit():
    # Create a database connection
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    print(l_name.get())
    # Insert data into the table
    if (f_name.get() is None or l_name.get() is None or address.get() is None
            or city.get() is None or state.get() is None or zipcode.get() is None):
        messagebox.showerror(title="Incomplete entry", message="You must complete all the fields to submit the data!")
    else:
        cursor.execute("""INSERT INTO addresses 
                   VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)""",
                       {
                           'f_name': f_name.get(),
                           'l_name': l_name.get(),
                           'address': address.get(),
                           'city': city.get(),
                           'state': state.get(),
                           'zipcode': f_name.get()
                       })

    # Commit the changes to the database
    connection.commit()
    connection.close()

    # Clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


def query():
    # Create a database connection
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    # Query the database
    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()

    # Loop through results
    print_records = ''
    for record in records:
        print_records += str(record) + " " + str(record[6]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=11, column=0, columnspan=2, pady=10)
    # Commit the changes to the database
    connection.commit()
    connection.close()


# Create a function to delete a database record
def delete():
    # Create a database connection
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    # Execute a record
    cursor.execute("DELETE from addresses WHERE oid=" + delete_box.get())
    delete_box.delete(0, END)

    # Commit the changes to the database
    connection.commit()
    connection.close()


# Create edit the edit function to update a record
def edit():
    global edit_window
    edit_window = Tk()
    edit_window.geometry("300x200")
    edit_window.title("Edit Window")

    # Create a database connection
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    record_id = delete_box.get()
    # Query the database
    cursor.execute("SELECT *, oid FROM addresses WHERE oid=" + record_id)
    records = cursor.fetchall()

    global f_name_editw
    global l_name_editw
    global address_editw
    global city_editw
    global state_editw
    global zipcode_editw
    # Create the text boxes
    f_name_editw = Entry(edit_window, width=30)
    f_name_editw.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name_editw = Entry(edit_window, width=30)
    l_name_editw.grid(row=1, column=1, padx=20)
    address_editw = Entry(edit_window, width=30)
    address_editw.grid(row=2, column=1, padx=20)
    city_editw = Entry(edit_window, width=30)
    city_editw.grid(row=3, column=1, padx=20)
    state_editw = Entry(edit_window, width=30)
    state_editw.grid(row=4, column=1, padx=20)
    zipcode_editw = Entry(edit_window, width=30)
    zipcode_editw.grid(row=5, column=1, padx=20)

    # Create the text box labels
    f_name_label = Label(edit_window, text="First Name")
    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_name_label = Label(edit_window, text="Last Name")
    l_name_label.grid(row=1, column=0)
    address_label = Label(edit_window, text="Address")
    address_label.grid(row=2, column=0)
    city_label = Label(edit_window, text="City")
    city_label.grid(row=3, column=0)
    state_label = Label(edit_window, text="State")
    state_label.grid(row=4, column=0)
    zipcode_label = Label(edit_window, text="Zipcode")
    zipcode_label.grid(row=5, column=0)

    # Loop through results
    for record in records:
        f_name_editw.insert(0, record[0])
        l_name_editw.insert(0, record[1])
        address_editw.insert(0, record[2])
        city_editw.insert(0, record[3])
        state_editw.insert(0, record[4])
        zipcode_editw.insert(0, record[5])

    # Create a button to save the edited record
    edit_button = Button(edit_window, text="Save changes", command=update)
    edit_button.grid(row=6, column=0, columnspan=2, pady=20)


def update():
    # Create a database connection
    connection = sqlite3.connect('address_book.db')
    cursor = connection.cursor()

    record_id = delete_box.get()
    cursor.execute("""UPDATE addresses SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode
        WHERE oid = :oid""",
        {
            'first': f_name_editw.get(),
            'last': l_name_editw.get(),
            'address': address_editw.get(),
            'city': city_editw.get(),
            'state': state_editw.get(),
            'zipcode': zipcode_editw.get(),
            'oid': record_id
        })
    # Commit the changes to the database
    connection.commit()
    connection.close()
    edit_window.destroy()


# Create the text boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)
address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)
city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)
state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)
zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)
delete_box = Entry(root, width=20)
delete_box.grid(row=9, column=1, padx=(0, 100))

# Create the text box labels
f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)
address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)
city_label = Label(root, text="City")
city_label.grid(row=3, column=0)
state_label = Label(root, text="State")
state_label.grid(row=4, column=0)
zipcode_label = Label(root, text="Zipcode")
zipcode_label.grid(row=5, column=0)
delete_box_label = Label(root, text="Select ID Number:", width=20)
delete_box_label.grid(row=9, column=0)

# Create the submit button
submit_button = Button(root, text="Add record to the database", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10)

# Create the query button
query_button = Button(root, text="Show records", command=query)
query_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, ipadx=46)

# Create the delete button
delete_button = Button(root, text="Delete record", width=10, command=delete)
delete_button.place(x=300, y=225)

# Create the update button
update_button = Button(root, text="Edit record", width=10, command=edit)
update_button.place(x=300, y=265)

root.mainloop()
