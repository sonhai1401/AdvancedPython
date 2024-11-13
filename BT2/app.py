import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Lớp chính của ứng dụng quản lý sinh viên
class DatabaseApp:
    def __init__(self, root):
        # Thiết lập cửa sổ chính
        self.root = root
        self.root.title("Quản lý Sinh viên")
        self.root.geometry("800x600")

        # Các trường kết nối cơ sở dữ liệu với giá trị mặc định
        self.db_name = tk.StringVar(value='quanlysinhvien')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        
        # Lựa chọn bảng với bảng mặc định và các bảng khả dụng
        self.selected_table = tk.StringVar(value='sinh_vien')
        self.tables = ['sinh_vien', 'khoa', 'mon_hoc', 'ket_qua']
        
        # Khởi tạo các phần tử giao diện và các biến kết nối cơ sở dữ liệu
        self.create_widgets()
        self.conn = None
        self.cur = None

    # Tạo tất cả các phần tử giao diện và bố trí
    def create_widgets(self):
        # Phần kết nối cơ sở dữ liệu
        connection_frame = ttk.LabelFrame(self.root, text="Kết nối Database")
        connection_frame.pack(pady=10, padx=10, fill="x")

        # Nhãn và ô nhập cho tên cơ sở dữ liệu
        ttk.Label(connection_frame, text="Database:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        
        # Nhãn và ô nhập cho tên người dùng
        ttk.Label(connection_frame, text="User:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.user).grid(row=0, column=3, padx=5, pady=5)

        # Nhãn và ô nhập cho mật khẩu
        ttk.Label(connection_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=1, column=1, padx=5, pady=5)

        # Nhãn và ô nhập cho địa chỉ host
        ttk.Label(connection_frame, text="Host:").grid(row=1, column=2, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.host).grid(row=1, column=3, padx=5, pady=5)

        # Nút kết nối cơ sở dữ liệu
        ttk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=2, columnspan=4, pady=10)

        # Phần chọn bảng
        table_frame = ttk.LabelFrame(self.root, text="Chọn bảng")
        table_frame.pack(pady=10, padx=10, fill="x")

        # Nhãn và hộp chọn bảng
        ttk.Label(table_frame, text="Bảng:").pack(side="left", padx=5)
        table_combo = ttk.Combobox(table_frame, textvariable=self.selected_table, values=self.tables)
        table_combo.pack(side="left", padx=5)
        table_combo.bind('<<ComboboxSelected>>', self.on_table_select)

        # Phần nhập dữ liệu
        self.data_entry_frame = ttk.LabelFrame(self.root, text="Nhập dữ liệu")
        self.data_entry_frame.pack(pady=10, padx=10, fill="x")

        # Phần nút hành động (Thêm, Cập nhật, Xóa, Tải lại)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Thêm", command=self.insert_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cập nhật", command=self.update_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Tải lại", command=self.load_data).pack(side="left", padx=5)

        # Phần hiển thị dữ liệu
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Thanh cuộn cho Treeview
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    # Hàm kết nối cơ sở dữ liệu
    def connect_db(self):
        try:
            # Thực hiện kết nối
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành công", "Kết nối database thành công!")
            self.load_data()  # Tải dữ liệu sau khi kết nối thành công
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối database: {e}")

    # Tạo các trường nhập dữ liệu theo bảng được chọn
    def create_data_entry_fields(self):
        # Xóa các trường cũ
        for widget in self.data_entry_frame.winfo_children():
            widget.destroy()

        # Tạo các trường nhập dữ liệu theo bảng đã chọn
        self.entries = {}
        row = 0
        col = 0
        
        # Xác định các trường cho từng bảng
        if self.selected_table.get() == 'sinh_vien':
            fields = ['ma_sinh_vien', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'mail', 
                     'di_dong', 'cmnd', 'hoc_bong', 'ma_khoa']
        elif self.selected_table.get() == 'khoa':
            fields = ['ma_khoa', 'ten']
        elif self.selected_table.get() == 'mon_hoc':
            fields = ['ma_mon', 'ten']
        elif self.selected_table.get() == 'ket_qua':
            fields = ['ma_sinh_vien', 'ma_mon', 'diem']

        # Tạo nhãn và ô nhập cho mỗi trường
        for field in fields:
            ttk.Label(self.data_entry_frame, text=field).grid(row=row, column=col*2, padx=5, pady=5)
            entry = ttk.Entry(self.data_entry_frame)
            entry.grid(row=row, column=col*2+1, padx=5, pady=5)
            self.entries[field] = entry
            
            col += 1
            if col == 2:
                col = 0
                row += 1

    # Xử lý sự kiện khi chọn bảng
    def on_table_select(self, event=None):
        self.create_data_entry_fields()  # Tạo các trường nhập mới
        self.load_data()  # Tải lại dữ liệu từ bảng được chọn

    # Hàm thực thi truy vấn SQL
    def execute_transaction(self, query, values=None):
        try:
            if values:
                self.cur.execute(query, values)
            else:
                self.cur.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()  # Quay lại nếu có lỗi
            raise e

    # Tải dữ liệu từ bảng hiện tại
    def load_data(self):
        if not self.conn or not self.cur:
            messagebox.showerror("Lỗi", "Chưa kết nối database!")
            return

        try:
            # Xóa các mục hiện tại trong Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Lấy tên các cột từ bảng đã chọn
            self.cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{self.selected_table.get()}'
            """)
            columns = [col[0] for col in self.cur.fetchall()]

            # Sắp xếp lại cột để khớp với thứ tự mong đợi của từng bảng
            expected_order = None
            if self.selected_table.get() == 'sinh_vien':
                expected_order = ['ma_sinh_vien', 'ho', 'ten', 'gioi_tinh', 'ngay_sinh', 'mail', 'di_dong', 'cmnd', 'hoc_bong', 'ma_khoa']
            elif self.selected_table.get() == 'khoa':
                expected_order = ['ma_khoa', 'ten']
            elif self.selected_table.get() == 'mon_hoc':
                expected_order = ['ma_mon', 'ten']
            elif self.selected_table.get() == 'ket_qua':
                expected_order = ['ma_sinh_vien', 'ma_mon', 'diem']
            
            if expected_order:
                columns = [col for col in expected_order if col in columns]

            # Thiết lập cột và tiêu đề trong Treeview
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            # Lấy dữ liệu và hiển thị trên Treeview
            self.cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.selected_table.get())))
            rows = self.cur.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")
            self.conn.rollback()
          
if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
