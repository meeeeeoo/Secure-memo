import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Secure Memo")
window.geometry("500x400")

def save_memo():
    print("저장 버튼 클릭됨")

    memo = memo_text.get("1.0", tk.END).strip()

    if not memo:
        messagebox.showwarning("알림", "메모를 입력해주세요")
        return
    
    with open("memo.txt", "a", encoding="utf-8") as file:
        file.write(memo + "\n---\n")

    memo_text.delete("1.0", tk.END)
    messagebox.showinfo("저장 완료", "메모가 저장되었습니다.")

title_label = tk.Label(window, text="Secure Memo",)
title_label.pack(pady=10)

memo_text = tk.Text(window, width=50, height=15)
memo_text.pack()

save_button = tk.Button(window, text="저장", command=save_memo)
save_button.pack(pady=10)

window.mainloop()