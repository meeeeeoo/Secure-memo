import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_NAME = "secure_memo.db"

def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")
    connection.commit()
    connection.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def save_memo():
    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning("알림", "제목을 입력해주세요.")
        return

    if not content:
        messagebox.showwarning("알림", "메모 내용을 입력해주세요.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO memos (title, content) VALUES (?, ?)",
        (title, content)
    )

    connection.commit()
    connection.close()

    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

    load_memo_list()

    messagebox.showinfo("저장 완료", "메모가 저장되었습니다.")

def load_memo_list():
    memo_list.delete(0, tk.END)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, title FROM memos ORDER BY id DESC")
    memos = cursor.fetchall()

    connection.close()

    for memo_id, title in memos:
        memo_list.insert(tk.END, title)

def load_selected_memo(event=None):
    selection = memo_list.curselection()

    if not selection:
        return
    
    selected_index = selection[0]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM memos ORDER BY id DESC")
    memos = cursor.fetchall()

    if selected_index >= len(memos):
        connection.close()
        return

    memo_id = memos[selected_index][0]

    cursor.execute(
        "SELECT title, content FROM memos WHERE id = ?",
        (memo_id,)
    )

    memo = cursor.fetchone()

    connection.close()

    if memo:
        title, content = memo
        
        title_entry.delete(0,tk.END)
        title_entry.insert(0, title)

        content_text.delete("1.0", tk.END)
        content_text.insert("1.0", content)

def delete_memo():
    selection = memo_list.curselection()

    if not selection:
        messagebox.showwarning("알림", "삭제할 메모를 선택해주세요.")
        return

    selected_index = selection[0]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM memos ORDER BY id DESC")
    memos = cursor.fetchall()

    if selected_index >= len(memos):
        connection.close()
        return

    memo_id = memos[selected_index][0]

    connection.close()

    result = messagebox.askyesno(
        "삭제 확인", "선택한 메모를 삭제할까요?"
        )

    if not result:
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM memos WHERE id = ?",
        (memo_id,)
    )

    connection.commit()
    connection.close()

    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

    load_memo_list()
    messagebox.showinfo("삭제 완료", "메모가 삭제되었습니다.")

def update_memo():
    selection = memo_list.curselection()

    if not selection:
        messagebox.showwarning("알림", "수정할 메모를 선택해주세요.")
        return

    selected_index = selection[0]
    
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM memos ORDER BY id DESC"
    )

    memos = cursor.fetchall()

    if selected_index >= len(memos):
        connection.close()
        return

    memo_id = memos[selected_index][0]

    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning("알림", "제목을 입력해주세요.")
        return

    if not content:
        messagebox.showwarning("알림", "메모 내용을 입력해주세요.")
        return

    cursor.execute(
        "UPDATE memos SET title = ?, content = ? WHERE id = ?",
        (title, content, memo_id)
    )

    connection.commit()
    connection.close()

    load_memo_list()

    messagebox.showinfo("수정 완료", "메모가 수정되었습니다.")

def new_memo():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    memo_list.selection_clear(0, tk.END)
    title_entry.focus()

create_database()

window = tk.Tk()
window.title("Secure Memo")
window.geometry("800x600")

left_frame = tk.Frame(window)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

list_label = tk.Label(left_frame, text="메모 목록")
list_label.pack()

memo_list = tk.Listbox(left_frame, width=25, height=22)
memo_list.pack(pady=5)

memo_list.bind("<<ListboxSelect>>", load_selected_memo)

new_button = tk.Button(left_frame, text="+ 새 메모", command=new_memo)
new_button.pack(pady=5)

delete_button = tk.Button(left_frame, text="삭제", command=delete_memo)
delete_button.pack(pady=5)

update_button = tk.Button(left_frame, text="수정", command=update_memo)
update_button.pack(pady=5)

right_frame = tk.Frame(window)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

title_label = tk.Label(right_frame, text="제목")
title_label.pack(anchor="w")

title_entry = tk.Entry(right_frame)
title_entry.pack(fill="x", pady=5)

content_label = tk.Label(right_frame, text="내용")
content_label.pack(anchor="w")

content_text = tk.Text(right_frame, height=20)
content_text.pack(fill="both", expand=True, pady=5)

save_button = tk.Button(right_frame, text="저장", command=save_memo)
save_button.pack(pady=5)

load_memo_list()

window.mainloop()