import tkinter as tk
from tkinter import ttk

# Tạo cửa sổ chính của ứng dụng
win = tk.Tk()
win.title("Calculator")
# Hàm xử lý phép toán khi nhấn các nút
def calculate(operation):
    try:
        # Lấy giá trị từ các ô nhập liệu a và b
        a = float(entry_a.get())
        b = float(entry_b.get())
        # Thực hiện các phép toán dựa trên nút được nhấn
        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            # Kiểm tra chia cho 0
            result = a / b if b != 0 else "Lỗi (chia cho 0)"
        # Hiển thị kết quả trong ô key_field
        key_field.delete(0, tk.END)  # Xóa kết quả cũ
        key_field.insert(0, str(result))  # Chèn kết quả mới
    except ValueError:
        # Nếu nhập dữ liệu không hợp lệ, hiển thị thông báo lỗi
        key_field.delete(0, tk.END)
        key_field.insert(0, "Dữ liệu không hợp lệ")
# Tạo khung cho các ô nhập liệu
input_frame = ttk.Frame(win, padding="10")
input_frame.grid(row=0, column=0, padx=10, pady=10)
# Tạo nhãn và ô nhập liệu cho giá trị a
label_a = ttk.Label(input_frame, text="a")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = ttk.Entry(input_frame)
entry_a.grid(row=0, column=1, padx=5, pady=5)
# Tạo nhãn và ô nhập liệu cho giá trị b
label_b = ttk.Label(input_frame, text="b")
label_b.grid(row=1, column=0, padx=5, pady=5)
entry_b = ttk.Entry(input_frame)
entry_b.grid(row=1, column=1, padx=5, pady=5)
# Tạo khng cho các nút phép toán (cộng, trừ, nhân, chia)
button_frame = ttk.Frame(win, padding="10")
button_frame.grid(row=0, column=1, padx=10, pady=10)
# Thêm nút cộng với sự kiện nhấn nút
plus_button = ttk.Button(button_frame, text="+", command=lambda: calculate("+"))
plus_button.grid(row=0, column=0, padx=5, pady=5)
# Thêm nút trừ với sự kiện nhấn nút
minus_button = ttk.Button(button_frame, text="-", command=lambda: calculate("-"))
minus_button.grid(row=0, column=1, padx=5, pady=5)
# Thêm nút nhân với sự kiện nhấn nút
multiply_button = ttk.Button(button_frame, text="*", command=lambda: calculate("*"))
multiply_button.grid(row=1, column=0, padx=5, pady=5)
# Thêm nút chia với sự kiện nhấn nút
divide_button = ttk.Button(button_frame, text="/", command=lambda: calculate("/"))
divide_button.grid(row=1, column=1, padx=5, pady=5)
# Tạo nhãn cho ô nhập liệu kết quả (key_field)
key_field_label = ttk.Label(win, text="Kết Quả")
key_field_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
# Ô nhập liệu để hiển thị kết quả
key_field = ttk.Entry(win, width=50)
key_field.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Chạy ứng dụng
win.mainloop()
