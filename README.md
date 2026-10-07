# Bài tập tổng hợp Chương 3 - Sổ điểm lớp học

## 1. Routes

Chạy lệnh:

flask --app sodiem routes

Ứng dụng gồm các route chính:

- `/`
- `/students`
- `/students/<mssv>`
- `/sv/<mssv>`
- `/students/<mssv>/export`
- `/search`
- `/api/students`
- `/api/students/<mssv>`
- `/api/students/<mssv>/scores/<course>`
- `/static/<path:filename>`

## 2. Kiểm thử

### Chuyển hướng link rút gọn

GET /sv/23T1020001

Kết quả: 301 MOVED PERMANENTLY

Location: /students/23T1020001


### Xuất CSV

GET /students/23T1020001/export

Kết quả: tải file CSV bảng điểm của sinh viên.


### Lọc API

GET /api/students?lop=k47a&min_avg=7

Kết quả: trả về các sinh viên lớp K47A có điểm trung bình >= 7.


### min_avg không hợp lệ

GET /api/students?min_avg=abc

Kết quả: 400 BAD REQUEST.


### MSSV không tồn tại

GET /api/students/999

Kết quả: 404 NOT FOUND.


### Thêm điểm

PUT /api/students/23T1020005/scores/web?score=9

Kết quả: 201 CREATED.


### Sửa điểm

PUT /api/students/23T1020005/scores/WEB?score=7.5

Kết quả: 200 OK.


### Điểm không hợp lệ

PUT /api/students/23T1020005/scores/WEB?score=11

Kết quả: 400 BAD REQUEST.


### Xóa điểm

DELETE /api/students/23T1020005/scores/WEB

Kết quả: 204 NO CONTENT.


### POST API không hỗ trợ

POST /api/students/23T1020005/scores/WEB

Kết quả: 405 METHOD NOT ALLOWED, trả về JSON.


### POST trang web không hỗ trợ

POST /students

Kết quả: 405 METHOD NOT ALLOWED, trả về HTML.


## 3. Câu hỏi

### Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm Location?

Câu 4 dùng mã 301 vì `/sv/<mssv>` là đường dẫn rút gọn và chuyển hướng vĩnh viễn đến `/students/<mssv>`.

Câu 8 trả mã 201 khi thêm mới điểm cho một học phần vì tài nguyên mới đã được tạo. Header Location cho biết URL của tài nguyên vừa được tạo.

### Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?

Không. Dữ liệu STUDENTS hiện chỉ được lưu trong bộ nhớ của chương trình. Khi server khởi động lại, biến STUDENTS được tạo lại từ dữ liệu ban đầu trong mã nguồn nên điểm được thêm qua API sẽ mất.