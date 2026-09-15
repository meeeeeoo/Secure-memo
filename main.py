import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Secure Memo")
window.geometry("500x400")

def save_memo():

    memo = memo_text.get("1.0", tk.END).strip()

    if not memo:
        messagebox.showwarning("알림", "메모를 입력해주세요")
        return
    
    with open("memo.txt", "a", encoding="utf-8") as file:
        file.write(memo + "\n---\n")

    memo_text.delete("1.0", tk.END)
    messagebox.showinfo("저장 완료", "메모가 저장되었습니다.")

def load_memo():
    try:
        with open("memo.txt", "r", encoding="utf-8") as file:
            memo = file.read()

        memo_text.delete("1.0", tk.END)
        memo_text.insert("1.0", memo)

    except FileNotFoundError:
        messagebox.showwarning("알림", "저장된 메모가 없습니다.")

def delete_memo():
    result = messagebox.askyesno("삭제 확인", "저장된 메모를 모두 삭제하시겠습니까?")

    if result:
        with open("memo.txt", "w", encoding="utf-8") as file:
            file.write("")

        memo_text.delete("1.0", tk.END)
        messagebox.showinfo("삭제 완료", "메모가 모두 삭제되었습니다.")

title_label = tk.Label(window, text="Secure Memo",)
title_label.pack(pady=10)

memo_text = tk.Text(window, width=50, height=15)
memo_text.pack()

save_button = tk.Button(window, text="저장", command=save_memo)
save_button.pack(pady=10)
load_button = tk.Button(window, text="불러오기", command=load_memo)
load_button.pack(pady=5)
delete_button = tk.Button(window, text="전체 삭제", command=delete_memo)
delete_button.pack(pady=5)

window.mainloop()