import tkinter as tk
import tkinter.messagebox as tkm
import sqlite3
from datetime import datetime


DB_NAME = "msg.db"


def init_db_table():
    # set converter
    detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    sql_statement = "CREATE TABLE IF NOT EXISTS msg (id INTEGER PRIMARY KEY, message TEXT, created_at datetime)"
    cur.execute(sql_statement)
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("select * from msg")
    raws = cur.fetchall()
    conn.close()
    return raws


def insert(message):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    sql_statement = "insert into msg values(NULL, ?, ?)"
    cur.execute(sql_statement, (message, datetime.now()))
    conn.commit()
    conn.close()


def save_msg(message):
    insert(message)
    tkm.showinfo("Save", "Save message")


def view_msg(listbox):
    listbox.delete(0, tk.END)
    for row in view():
        data = "ID: " + str(row[0]) + ", Message: " + row[1] + ", CreatedAt:" + str(row[2])
        listbox.insert(tk.END, data)


init_db_table()

# Initilize GUI
root = tk.Tk()

label = tk.Label(root, text="Your message")
label.pack()

text_form = tk.Entry(root)
text_form.pack()


save_button = tk.Button(root, text="Save to SQLite", width=20, command=lambda: save_msg(text_form.get()))
save_button.pack()

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack()

view_button = tk.Button(root, text="View all data", width=20, command=lambda: view_msg(listbox))
view_button.pack()

root.title("sqlite3 sample")
root.geometry("600x400")
root.mainloop()