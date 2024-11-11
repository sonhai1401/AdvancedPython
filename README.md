# Hệ thống quản lý khách sạn

Ứng dụng này là một hệ thống quản lý khách sạn với giao diện đồ họa (GUI) sử dụng Tkinter của Python để tạo giao diện người dùng và psycopg2 để kết nối với cơ sở dữ liệu PostgreSQL.

Tính Năng
Đăng Ký và Đăng Nhập Người Dùng: Người dùng có thể đăng ký tài khoản bằng cách cung cấp tên, số điện thoại, email, CMND/hộ chiếu và mật khẩu. Mật khẩu được mã hóa để đảm bảo an toàn.
Giao Diện Quản Lý:
Xem trạng thái phòng: Hiển thị mã phòng, tình trạng, tiện nghi và khách hàng đang ở (nếu có).
Xem khách hàng đang lưu trú: Hiển thị danh sách khách hàng hiện đang lưu trú trong khách sạn.
Xem tổng doanh thu: Hiển thị tổng doanh thu từ các hóa đơn thanh toán.

Giao Diện Khách Hàng:
Tìm kiếm và đặt phòng: Cho phép khách hàng tìm phòng trống dựa trên số giường và mức giá tối đa.
Trả phòng: Cho phép khách hàng trả phòng và hiển thị tổng chi phí phải trả cho thời gian lưu trú.

Yêu Cầu Hệ Thống
Python: Phiên bản 3.x
Thư viện Python:
tkinter: Thư viện để tạo giao diện người dùng.
psycopg2: Thư viện để kết nối với cơ sở dữ liệu PostgreSQL.
hashlib: Để mã hóa mật khẩu người dùng.

Cơ sở dữ liệu: PostgreSQL với các bảng sau:
khachhang: Lưu thông tin khách hàng như tên, số điện thoại, email, CMND/hộ chiếu, mật khẩu, và vai trò người dùng.
phong: Chứa thông tin phòng gồm mã phòng, tình trạng, giá, tiện nghi, và số lượng giường.
lichsuluutru: Lưu lịch sử lưu trú của khách hàng.
hoadon: Lưu thông tin hóa đơn thanh toán của khách hàng.

Các chức năng của ứng dụng
Đăng Ký Người Dùng: Truy cập vào tab "Đăng ký" để tạo tài khoản mới bằng cách nhập thông tin cá nhân.
Đăng Nhập: Sử dụng tab "Đăng nhập" để đăng nhập. Nếu người dùng có vai trò là quản lý, giao diện quản lý sẽ hiển thị. Nếu không, giao diện dành cho khách hàng sẽ hiển thị.
Chức Năng Quản Lý:
Xem trạng thái phòng: Hiển thị thông tin phòng gồm tình trạng, tiện nghi, và tên khách hàng (nếu có).
Xem khách hàng đang lưu trú: Hiển thị danh sách khách hàng hiện đang ở tại khách sạn.
Xem tổng doanh thu: Hiển thị tổng doanh thu từ các hóa đơn đã được thanh toán.
Chức Năng Khách Hàng:
Tìm kiếm và đặt phòng: Khách hàng có thể tìm phòng trống và đặt phòng phù hợp với nhu cầu.
Trả phòng: Cho phép khách hàng thực hiện trả phòng và thanh toán chi phí cho thời gian đã lưu trú.

Lưu Ý
Đảm bảo rằng PostgreSQL đang chạy và thông tin kết nối cơ sở dữ liệu (dbname, user, password, host) trong mã Python là chính xác.
Mật khẩu người dùng được mã hóa trước khi lưu vào cơ sở dữ liệu để bảo mật.
Nếu có lỗi kết nối hoặc lỗi từ cơ sở dữ liệu, thông báo lỗi sẽ hiển thị cho người dùng để dễ dàng khắc phục.
