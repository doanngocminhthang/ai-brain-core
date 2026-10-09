# QUY TRÌNH KỸ SƯ TRƯỞNG & QUẢN TRỊ TRÍ NHỚ (AUTONOMOUS SOP)
Dành cho: Antigravity & Claude Code (Đồng bộ Máy bàn & Laptop)

## 1. Ưu tiên Sử dụng Trí nhớ CSDL (ai_brain.db)
- TRƯỚC KHI tìm kiếm file hoặc quét toàn bộ ổ đĩa: Luôn tra cứu bằng script `ai_brain.py` hoặc truy vấn SQLite để lấy chính xác đường dẫn trong 0.001s, tránh tốn token quét đĩa.
- Lệnh tra cứu: `python ai_brain.py find <keyword>`

## 2. Quản lý 38 Module & 3 Trụ cột Lâm nghiệp
- Mọi công việc kỹ thuật phải được gắn vào mã module cụ thể (từ MOD_01 đến MOD_38) thuộc 3 Trụ cột:
  1. AI Giám Sát Cháy Rừng (CHAY_RUNG)
  2. AI Biến Động Rừng (BIEN_DONG)
  3. AI An Ninh Rừng (AN_NINH)
- Sau khi hoàn thành hoặc đạt mốc quan trọng, tự động cập nhật tiến độ % của module.

## 3. Quản lý Sơ đồ Mermaid
- BẮT BUỘC vẽ sơ đồ Mermaid trực quan hóa trước khi bắt tay vào viết code lớn.
- Tự động lưu các sơ đồ quan trọng vào bảng `mermaid_vault` để tái sử dụng vĩnh viễn.

## 4. Ghi nhớ Lỗi (Troubleshooting Memory)
- Khi giải quyết xong các lỗi hóc búa (RTSP timeout, CUDA OOM, Buffer leak...), BẮT BUỘC lưu lại giải pháp vào bảng `error_memories`.
