# AI Brain Core - Trạm Quản Trị Trí Nhớ & Đa Tác Nhân Lâm Nghiệp

Hệ thống quản lý tri thức, đường dẫn tài liệu, sơ đồ kiến trúc và đối chiếu task dev dành riêng cho Kỹ sư trưởng / Lead Developer.
Đồng bộ mượt mà giữa **Máy bàn** và **Laptop cá nhân** (cho cả Antigravity và 2 tài khoản Claude Code).

---

## 🚀 Cách Dùng Nhanh (Gõ 1 cái ra ngay trong 0.001 giây)

Mở Terminal (CMD / PowerShell) tại thư mục này:

1. **Tìm kiếm Đường dẫn, Bản vẽ, Sơ đồ, Tài liệu hoặc Task của Dev:**
   ```cmd
   find <từ_khóa>
   ```
   * *Ví dụ:* `find kiến trúc` ➔ Hiện ngay đường dẫn file ảnh kiến trúc và sơ đồ Mermaid.
   * *Ví dụ:* `find Dahua` ➔ Hiện đặc tả camera Dahua, IP mạng và cách sửa lỗi drop frame.
   * *Ví dụ:* `find Nam` ➔ Hiện ngay bạn Nam đang làm task gì, nhánh Git nào, đã pass test chưa.

2. **Xem Bảng Tiến độ 38 Module (3 Trụ cột Lâm nghiệp):**
   ```cmd
   progress
   ```

3. **Xem Bảng Đối chiếu Task của Team Dev:**
   ```cmd
   dev
   ```

---

## 🖥️ Xem và Sửa Trực quan bằng Chuột (như Excel)

Phần mềm **DB Browser for SQLite** đã được cài đặt tự động trên máy tính của bạn:
1. Mở menu Start của Windows, gõ tìm **DB Browser for SQLite**.
2. Bấm **Open Database** (Mở CSDL) và chọn file: `D:\ai_brain_core\ai_brain.db`.
3. Chuyển sang tab **Browse Data** (Xem Dữ liệu): Bạn sẽ thấy toàn bộ các bảng `modules`, `dev_tasks`, `path_index`, `mermaid_vault` được xếp thành hàng và cột như một bảng tính Excel. Bạn có thể thêm, sửa, xóa trực tiếp bằng chuột bất cứ lúc nào!

---

## 🔄 Hướng Dẫn Đồng Bộ Sang Laptop Cá Nhân (1-Click Git)

1. **Tại Máy bàn:**
   * Thư mục này (`D:\ai_brain_core`) đã được khởi tạo sẵn Git.
   * Tạo một Private Repository trên GitHub hoặc GitLab cá nhân (vd: `my-ai-brain`).
   * Gõ lệnh liên kết và đẩy lên:
     ```cmd
     git remote add origin <link_github_cua_ban>
     git branch -M main
     git push -u origin main
     ```

2. **Tại Laptop Cá nhân:**
   * Mở terminal trên Laptop và kéo về:
     ```cmd
     git clone <link_github_cua_ban> C:\ai_brain_core
     ```
   * Sao chép nội dung file `GEMINI.md` vào: `C:\Users\<Tên_User>\.gemini\GEMINI.md`.
   * **Xong!** Ngay lập tức cả Antigravity và 2 tài khoản Claude Code trên Laptop của bạn sẽ tự động kết nối và dùng chung 100% bộ nhớ trí tuệ này!
