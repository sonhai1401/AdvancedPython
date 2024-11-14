
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Key để sử dụng flash thông báo

# Cấu hình kết nối đến cơ sở dữ liệu
db_config = {
    "dbname": "quanlykhachsan",
    "user": "postgres",
    "password": "123456",
    "host": "localhost",
    "port": "5432"
}

# Hàm kết nối cơ sở dữ liệu
def get_db_connection():
    conn = psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Hiển thị danh sách khách hàng
@app.route('/khachhang')
def khachhang():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM KhachHang;")
    khachhangs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('khachhang.html', khachhangs=khachhangs)

# Thêm mới khách hàng
@app.route('/khachhang/add', methods=['POST'])
def add_khachhang():
    conn = get_db_connection()
    cur = conn.cursor()
    ten = request.form['ten']
    so_dien_thoai = request.form['so_dien_thoai']
    email = request.form['email']
    cmnd = request.form['cmnd']

    cur.execute("INSERT INTO KhachHang (Ten, SoDienThoai, Email, CMND_HoChieu) VALUES (%s, %s, %s, %s);",
                (ten, so_dien_thoai, email, cmnd))
    conn.commit()
    cur.close()
    conn.close()
    flash("Khách hàng đã được thêm thành công!", "success")
    return redirect(url_for('khachhang'))

# Xóa khách hàng
@app.route('/khachhang/delete/<int:id>', methods=['POST'])
def delete_khachhang(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM KhachHang WHERE ID = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Khách hàng đã được xóa thành công!", "success")
    return redirect(url_for('khachhang'))

# Quản lý phòng
@app.route('/phong')
def phong():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Phong;")
    phongs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('phong.html', phongs=phongs)

# Thêm phòng mới
@app.route('/phong/add', methods=['POST'])
def add_phong():
    conn = get_db_connection()
    cur = conn.cursor()
    so_luong_giuong = request.form['so_luong_giuong']
    tien_nghi = request.form['tien_nghi']
    gia = request.form['gia']
    tinh_trang = request.form['tinh_trang']

    cur.execute("INSERT INTO Phong (SoLuongGiuong, TienNghi, Gia, TinhTrang) VALUES (%s, %s, %s, %s);",
                (so_luong_giuong, tien_nghi, gia, tinh_trang))
    conn.commit()
    cur.close()
    conn.close()
    flash("Phòng đã được thêm thành công!", "success")
    return redirect(url_for('phong'))

# Hiển thị đặt phòng
@app.route('/datphong')
def datphong():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DatPhong.IDDatPhong, KhachHang.Ten, Phong.IDPhong, DatPhong.NgayNhanPhong, DatPhong.NgayTraPhong
        FROM DatPhong
        JOIN KhachHang ON DatPhong.IDKhachHang = KhachHang.ID
        JOIN Phong ON DatPhong.IDPhong = Phong.IDPhong;
    """)
    datphongs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('datphong.html', datphongs=datphongs)

# Thêm mới đặt phòng
@app.route('/datphong/add', methods=['POST'])
def add_datphong():
    conn = get_db_connection()
    cur = conn.cursor()
    id_khachhang = request.form['id_khachhang']
    id_phong = request.form['id_phong']
    ngay_nhan = request.form['ngay_nhan']
    ngay_tra = request.form['ngay_tra']

    cur.execute("INSERT INTO DatPhong (IDKhachHang, IDPhong, NgayNhanPhong, NgayTraPhong) VALUES (%s, %s, %s, %s);",
                (id_khachhang, id_phong, ngay_nhan, ngay_tra))
    conn.commit()
    cur.close()
    conn.close()
    flash("Đặt phòng đã được thêm thành công!", "success")
    return redirect(url_for('datphong'))

if __name__ == "__main__":
    app.run(debug=True)
