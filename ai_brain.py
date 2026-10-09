"""
HỆ THỐNG QUẢN TRỊ TRÍ NHỚ VÀ TOÀN DIỆN KỸ THUẬT PHẦN MỀM (AI BRAIN ENTERPRISE)
Quản lý:
1. 38 Module & 3 Trụ cột Lâm nghiệp (Tiến độ %, Deadline, Tech Lead)
2. Phân rã Kỹ thuật sâu: Chức năng con -> Công nghệ -> Thuật toán -> Bộ lọc
3. Tra cứu Tài liệu & Bản vẽ (Tác giả, Ngày tạo, Phụ trách, Đường dẫn tuyệt đối)
4. Kho Sơ đồ Mermaid (Chủ đề, Người vẽ, Người duyệt, Tags)
5. Giám sát Git & Pull Requests (PR, Branch, Commit, Người làm, Reviewer)
6. Nhật ký Kiểm thử QA/Test (File test, Người test, Ngày test, FPS, Latency, Pass/Fail)
7. Ký ức Lỗi & Sửa lỗi (Troubleshooting Memory)
"""
import sys
import os
import time
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "ai_brain.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_enterprise_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS modules;
    DROP TABLE IF EXISTS pillars;
    DROP TABLE IF EXISTS git_pull_requests;
    DROP TABLE IF EXISTS qa_test_runs;
    DROP TABLE IF EXISTS tech_breakdown;
    DROP TABLE IF EXISTS document_catalog;
    DROP TABLE IF EXISTS mermaid_vault;
    DROP TABLE IF EXISTS error_memories;

    -- 1. BẢNG 3 TRỤ CỘT
    CREATE TABLE IF NOT EXISTS pillars (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    );

    -- 2. BẢNG 38 MODULES (TIẾN ĐỘ, THỜI HẠN, TECH LEAD)
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar_id TEXT NOT NULL REFERENCES pillars(id),
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        tech_lead TEXT DEFAULT 'Lead Dev',
        ssot_path TEXT NOT NULL,
        progress_pct INTEGER DEFAULT 0,
        quality_score TEXT DEFAULT 'A',
        start_date TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'in_progress',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 3. BẢNG PHÂN RÃ KỸ THUẬT SÂU (CHỨC NĂNG -> THUẬT TOÁN -> BỘ LỌC)
    CREATE VIRTUAL TABLE IF NOT EXISTS tech_breakdown USING fts5(
        module_code,
        feature_name,
        tech_stack,
        algorithms,
        filters,
        developer,
        notes
    );

    -- 4. BẢNG CHỈ MỤC TÀI LIỆU & BẢN VẼ (TÁC GIẢ, NGƯỜI DUYỆT, TỪ KHÓA, PATH)
    CREATE VIRTUAL TABLE IF NOT EXISTS document_catalog USING fts5(
        title,
        doc_type,
        full_path,
        author,
        assignee,
        category,
        tags,
        created_date,
        module_code
    );

    -- 5. KHO SƠ ĐỒ MERMAID (CHỦ ĐỀ, NGƯỜI VẼ, NGƯỜI DUYỆT, TAGS)
    CREATE VIRTUAL TABLE IF NOT EXISTS mermaid_vault USING fts5(
        title,
        pillar_id,
        module_code,
        diagram_type,
        diagram_code,
        author,
        reviewer,
        tags
    );

    -- 6. BẢNG THEO DÕI GIT & PULL REQUESTS
    CREATE TABLE IF NOT EXISTS git_pull_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_number INTEGER UNIQUE,
        title TEXT NOT NULL,
        module_code TEXT,
        author TEXT NOT NULL,
        reviewer TEXT,
        branch_name TEXT,
        created_date TEXT,
        status TEXT DEFAULT 'open', -- open, merged, closed
        summary TEXT
    );

    -- 7. BẢNG NHẬT KÝ KIỂM THỬ & CHẤT LƯỢNG (QA / TESTING)
    CREATE TABLE IF NOT EXISTS qa_test_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_code TEXT NOT NULL,
        test_name TEXT NOT NULL,
        test_file TEXT NOT NULL,
        tester TEXT NOT NULL,
        test_date TEXT NOT NULL,
        environment TEXT DEFAULT 'Windows + Docker',
        result TEXT DEFAULT 'PASSED', -- PASSED, FAILED
        fps REAL,
        latency_ms REAL,
        error_log TEXT
    );

    -- 8. BỘ NHỚ LỖI VĨNH VIỄN (TROUBLESHOOTING MEMORY)
    CREATE VIRTUAL TABLE IF NOT EXISTS error_memories USING fts5(
        problem_summary,
        solution_steps,
        tags,
        module_code
    );
    """)
    conn.commit()
    conn.close()

def seed_enterprise_data():
    init_enterprise_db()
    conn = get_conn()
    cur = conn.cursor()

    # 1. Trụ cột
    cur.executemany("INSERT OR REPLACE INTO pillars (id, name, description) VALUES (?, ?, ?)", [
        ("CHAY_RUNG", "1. AI GIÁM SÁT CHÁY RỪNG", "Camera PTZ, YOLO khói/lửa, FWI/Nesterov, Cảnh báo tức thời"),
        ("BIEN_DONG", "2. AI BIẾN ĐỘNG RỪNG", "Ảnh viễn thám Sentinel-2/Landsat, Chỉ số NDVI/NBR, Mất rừng"),
        ("AN_NINH", "3. AI AN NINH RỪNG", "Xâm nhập người/xe, Bẫy ảnh hồng ngoại, Cảnh báo âm thanh cưa máy")
    ])

    # 2. Modules với Deadline & Tech Lead
    cur.execute("DELETE FROM modules")
    modules = [
        ("CHAY_RUNG", "MOD_01", "Thu nhận RTSP Camera Dahua PTZ", "Bạn Nam", "D:/main_workspace/dev/wildfire/camera_service/", 100, "A+", "2026-08-01", "2026-09-15", "completed"),
        ("CHAY_RUNG", "MOD_02", "Nhận diện Khói Lửa YOLOv8", "Bạn Huy", "D:/main_workspace/dev/wildfire/ai_models/smoke/", 85, "A", "2026-08-15", "2026-10-20", "in_progress"),
        ("CHAY_RUNG", "MOD_03", "Trạm Khí tượng & Chỉ số Nesterov", "Bạn Tuấn", "D:/main_workspace/dev/wildfire/weather_fwi/", 60, "B+", "2026-09-01", "2026-11-01", "in_progress"),
        ("CHAY_RUNG", "MOD_05", "Điều khiển Góc quay PTZ (ONVIF)", "Bạn Tuấn", "D:/main_workspace/dev/wildfire/ptz_control/", 90, "A", "2026-09-10", "2026-10-25", "in_progress"),
        ("BIEN_DONG", "MOD_16", "Thu nhận Ảnh Vệ tinh Sentinel-2", "Bạn Trang", "D:/main_workspace/dev/wildfire/satellite_pipeline/", 90, "A", "2026-08-10", "2026-10-15", "in_progress"),
        ("BIEN_DONG", "MOD_17", "Tính toán Chỉ số NDVI & NBR", "Bạn Trang", "D:/main_workspace/dev/wildfire/gis_indices/", 70, "B+", "2026-09-01", "2026-11-10", "in_progress"),
        ("AN_NINH", "MOD_28", "Nhận diện Người/Xe Xâm nhập", "Bạn Huy", "D:/main_workspace/dev/wildfire/intrusion_detect/", 80, "A", "2026-09-05", "2026-11-15", "in_progress"),
        ("AN_NINH", "MOD_29", "Phát hiện Âm thanh Tiếng cưa máy", "Bạn Hoàng", "D:/main_workspace/dev/wildfire/audio_sensor/", 50, "B", "2026-09-15", "2026-12-01", "in_progress"),
    ]
    cur.executemany("""
        INSERT INTO modules (pillar_id, code, name, tech_lead, ssot_path, progress_pct, quality_score, start_date, deadline, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, modules)

    # 3. Phân rã Kỹ thuật sâu (Chức năng -> Thuật toán -> Bộ lọc)
    cur.execute("DELETE FROM tech_breakdown")
    techs = [
        ("MOD_01", "Stream Đa Luồng Chống Nghẽn", "Python 3.11, OpenCV FFMPEG, AsyncIO", 
         "Non-blocking Frame Ingest, Circular Ring Buffer", "Drop Late Frame Filter, TCP KeepAlive", "Bạn Nam (BE)", "Đảm bảo độ trễ < 200ms"),
        ("MOD_02", "Nhận diện Cột Khói Xa (>3km)", "PyTorch, TensorRT FP16, CUDA 12", 
         "YOLOv8x + Multi-scale Feature Pyramid (FPN)", "CLAHE Cân bằng Sáng, Bộ lọc Nhiễu Sương mù Morlet", "Bạn Huy (AI)", "Đã train 85 epoch, mAP@0.5 đạt 89.2%"),
        ("MOD_03", "Dự báo Nguy cơ Cháy Cấp 1-5", "NumPy, Pandas, SciPy", 
         "Công thức Nesterov P = T * (T - Td) tích lũy, Rothermel Fire Spread", "Bộ lọc Làm mịn Dữ liệu Khí tượng Kalman", "Bạn Tuấn (IoT)", "Tự động kích hoạt khi P > 4,000"),
        ("MOD_17", "Phân tích Tổn thất Tán Rừng", "Rasterio, GDAL, GeoPandas", 
         "Chỉ số NBR = (NIR - SWIR2)/(NIR + SWIR2), NDVI = (NIR - RED)/(NIR + RED)", "Cloud Masking SCL (Lọc mây bóng mây)", "Bạn Trang (GIS)", "Xử lý song song 8 CPU core"),
        ("MOD_29", "Nhận diện Tiếng Cưa Xích Dã Ngoại", "Librosa, PyTorch, Torchaudio", 
         "Mel-Spectrogram 128 dải tần + Mạng CNN AudioNet", "Bandpass Filter 500Hz - 4000Hz (Cắt tiếng gió)", "Bạn Hoàng (DSP)", "Tỷ lệ nhận diện đúng 91.5% trong môi trường rừng")
    ]
    cur.executemany("""
        INSERT INTO tech_breakdown (module_code, feature_name, tech_stack, algorithms, filters, developer, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, techs)

    # 4. Tài liệu chi tiết (Tác giả, Ngày tạo, Phụ trách, Đường dẫn)
    cur.execute("DELETE FROM document_catalog")
    docs = [
        ("Bản vẽ Kiến trúc Hệ thống Tổng thể 3 Trụ Cột", "BẢN VẼ KIẾN TRÚC", "D:/main_workspace/docs/architecture/system_overview_v2.png", 
         "Kỹ sư Trưởng (Lead)", "Kỹ sư Trưởng (Lead)", "Kiến trúc Tổng quan", "kien_truc,tong_the,3_tru_cot,system", "2026-08-10", "ALL"),
        ("Bản vẽ Luồng Dữ liệu RTSP & AI Pipeline", "BẢN VẼ KIẾN TRÚC", "D:/main_workspace/docs/architecture/rtsp_ai_pipeline.svg", 
         "Bạn Nam", "Kỹ sư Trưởng (Lead)", "Xử lý Video", "luong_du_lieu,rtsp,camera,opencv", "2026-08-25", "MOD_01"),
        ("Đặc tả Giao thức ONVIF Điều khiển Camera Dahua", "TÀI LIỆU KỸ THUẬT", "D:/main_workspace/docs/specs/Dahua_PTZ_ONVIF_ProfileS_Spec.pdf", 
         "Hãng Dahua", "Bạn Tuấn", "Giao thức Thiết bị", "dahua,onvif,ptz,spec", "2026-09-02", "MOD_05"),
        ("Công thức Toán học Chỉ số Nguy cơ Cháy Nesterov", "TÀI LIỆU KỸ THUẬT", "D:/main_workspace/docs/algorithms/Nesterov_Fire_Risk_Formulas.docx", 
         "Viện Điều tra Quy hoạch Rừng", "Bạn Tuấn", "Thuật toán Lâm nghiệp", "nesterov,chay_rung,khi_tuong,cong_thuc", "2026-09-05", "MOD_03"),
        ("File Cấu hình Mạng & Địa chỉ IP 12 Trạm Camera", "FILE CẤU HÌNH", "D:/main_workspace/dev/wildfire/config/camera_network_ip.yaml", 
         "Bạn Nam", "Bạn Nam", "Hạ tầng Mạng", "camera,ip,config,yaml,mat_khau", "2026-09-12", "MOD_01"),
        ("Trọng số Mô hình YOLOv8 Khói Lửa Tốt Nhất", "WEIGHTS MODEL", "D:/main_workspace/dev/wildfire/weights/smoke_best_v8x.pt", 
         "Bạn Huy", "Kỹ sư Trưởng (Lead)", "Trọng số AI", "yolo,weights,pt,smoke,fire", "2026-09-28", "MOD_02")
    ]
    cur.executemany("""
        INSERT INTO document_catalog (title, doc_type, full_path, author, assignee, category, tags, created_date, module_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, docs)

    # 5. Sơ đồ Mermaid (Tác giả, Người duyệt, Tags)
    cur.execute("DELETE FROM mermaid_vault")
    diagrams = [
        ("Bản vẽ Luồng Camera PTZ và YOLO", "CHAY_RUNG", "MOD_01", "flowchart", 
         "flowchart LR\n A[Camera Dahua PTZ] -->|TCP Transport| B[OpenCV VideoCapture]\n B -->|Ring Buffer| C[YOLOv8 Smoke AI]\n C -->|Alert > 80%| D[MinIO S3 & WebSocket GIS]", 
         "Bạn Nam", "Kỹ sư Trưởng (Lead)", "camera,ptz,rtsp,yolo,dahua,kien_truc"),
        ("Quy trình Phân tích Ảnh Viễn thám Sentinel-2", "BIEN_DONG", "MOD_16", "sequenceDiagram",
         "sequenceDiagram\n Copernicus API->>Worker: Tải ảnh GeoTIFF Đa phổ\n Worker->>Index Calc: Tính NBR & NDVI đa luồng\n Index Calc->>GIS Dashboard: Xuất Layer Vùng Cháy", 
         "Bạn Trang", "Kỹ sư Trưởng (Lead)", "ve_tinh,sentinel,ndvi,nbr,gis"),
        ("Quy trình Đa Tác nhân Antigravity & Claude Code", "ALL", "ALL", "sequenceDiagram",
         "sequenceDiagram\n Lead->>Antigravity: Giao việc & Review\n Antigravity->>SQLite: Tra cứu Path & Lỗi cũ trong 1ms\n Antigravity->>ClaudeCode: Giao refactor code\n ClaudeCode-->>Lead: Báo cáo kết quả test", 
         "Kỹ sư Trưởng (Lead)", "Kỹ sư Trưởng (Lead)", "multi_agent,quy_trinh,claude,antigravity")
    ]
    cur.executemany("""
        INSERT INTO mermaid_vault (title, pillar_id, module_code, diagram_type, diagram_code, author, reviewer, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, diagrams)

    # 6. Bảng Git & Pull Requests
    cur.execute("DELETE FROM git_pull_requests")
    prs = [
        (12, "Fix lỗi buffer overflow khi mất kết nối RTSP Camera", "MOD_01", "Bạn Nam (BE)", "Kỹ sư Trưởng (Lead)", "fix/rtsp-buffer", "2026-09-14", "merged", "Đã test 48h không leak RAM"),
        (14, "Tối ưu hóa tính toán NBR raster song song bằng Rasterio", "MOD_17", "Bạn Trang (GIS)", "Kỹ sư Trưởng (Lead)", "feat/raster-parallel", "2026-09-20", "merged", "Thời gian xử lý giảm 8x"),
        (15, "Huấn luyện lại YOLOv8x với 5,000 ảnh khói sương mù", "MOD_02", "Bạn Huy (AI)", "Kỹ sư Trưởng (Lead)", "ai/yolo-smoke-v2", "2026-10-02", "open", "Đang train epoch 85/100"),
        (18, "Tích hợp API Zoom 30x Camera qua chuẩn ONVIF", "MOD_05", "Bạn Tuấn (IoT)", "Kỹ sư Trưởng (Lead)", "feat/onvif-zoom", "2026-10-05", "open", "Chờ kiểm thử độ trễ kết nối")
    ]
    cur.executemany("""
        INSERT INTO git_pull_requests (pr_number, title, module_code, author, reviewer, branch_name, created_date, status, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, prs)

    # 7. Bảng Nhật ký Kiểm thử QA/Test
    cur.execute("DELETE FROM qa_test_runs")
    tests = [
        ("MOD_01", "Stress-test 48h Luồng RTSP", "tests/test_rtsp_stress.py", "Bạn Nam", "2026-09-14", "Ubuntu 22.04 Docker", "PASSED", 25.0, 160.0, "FPS ổn định 25fps, latency 160ms"),
        ("MOD_02", "Inference Benchmark YOLOv8x TensorRT", "tests/test_yolo_benchmark.py", "Bạn Huy", "2026-10-01", "Windows 11 (GPU GTX 1050Ti)", "PASSED", 32.5, 30.8, "FP16 tối ưu, VRAM chiếm 2.1GB"),
        ("MOD_17", "Kiểm thử Tính Chỉ số NBR 4 Tỉnh Bắc Trung Bộ", "tests/test_nbr_calc.py", "Bạn Trang", "2026-09-22", "Linux Server 32GB RAM", "PASSED", 0.0, 1500.0, "Xử lý thành công file 8.4GB trong 1.5s"),
        ("MOD_05", "Đo Độ Trễ Điều Khiển Góc Xoay ONVIF", "tests/test_onvif_latency.py", "Bạn Tuấn", "2026-10-06", "Windows Local Lab", "FAILED", 0.0, 450.0, "Độ trễ 450ms vượt ngưỡng cho phép 200ms")
    ]
    cur.executemany("""
        INSERT INTO qa_test_runs (module_code, test_name, test_file, tester, test_date, environment, result, fps, latency_ms, error_log)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tests)

    # 8. Ký ức Lỗi
    cur.execute("DELETE FROM error_memories")
    errors = [
        ("Lỗi drop frame và timeout RTSP Camera Dahua sau 2h", 
         "1. Ép OPENCV_FFMPEG_CAPTURE_OPTIONS=rtsp_transport;tcp\n2. Tăng buffer kích thước 2048\n3. Luồng ngầm giải phóng frame cũ liên tục", "camera,ptz,rtsp,opencv,drop_frame", "MOD_01"),
        ("Lỗi CUDA out of memory khi chạy mô hình YOLOv8x trên GPU 4GB", 
         "1. Giảm batch size về 1\n2. Chuyển sang TensorRT FP16 (tiết kiệm 50% VRAM)\n3. Gọi torch.cuda.empty_cache() sau mỗi batch", "yolo,cuda,vram,gpu,oom", "MOD_02"),
        ("Lỗi tràn RAM khi nạp ảnh GeoTIFF vệ tinh kích thước 4GB",
         "Sử dụng Rasterio windowed reading để đọc theo khối block 512x512 thay vì nạp toàn bộ ảnh vào RAM", "rasterio,geotiff,ram,sentinel", "MOD_17")
    ]
    cur.executemany("""
        INSERT INTO error_memories (problem_summary, solution_steps, tags, module_code)
        VALUES (?, ?, ?, ?)
    """, errors)

    conn.commit()
    conn.close()
    print("[OK] Đã nạp thành công 100% CSDL Kỹ thuật Phần mềm Toàn diện tại: " + str(DB_PATH))

def find_all(keyword):
    """Tìm kiếm siêu tốc mọi ngóc ngách: Tài liệu, Bản vẽ, Sơ đồ, Thuật toán, PR, Test, Lỗi"""
    conn = get_conn()
    cur = conn.cursor()
    t0 = time.time()

    # 1. Tài liệu & Bản vẽ
    cur.execute("""
        SELECT title, doc_type, full_path, author, assignee, category, created_date, module_code
        FROM document_catalog WHERE document_catalog MATCH ? LIMIT 5
    """, (keyword,))
    docs = cur.fetchall()

    # 2. Phân rã Kỹ thuật & Thuật toán
    cur.execute("""
        SELECT module_code, feature_name, tech_stack, algorithms, filters, developer, notes
        FROM tech_breakdown WHERE tech_breakdown MATCH ? LIMIT 5
    """, (keyword,))
    techs = cur.fetchall()

    # 3. Sơ đồ Mermaid
    cur.execute("""
        SELECT title, diagram_type, diagram_code, author, reviewer, module_code
        FROM mermaid_vault WHERE mermaid_vault MATCH ? LIMIT 5
    """, (keyword,))
    diagrams = cur.fetchall()

    # 4. Git & Pull Requests
    cur.execute("""
        SELECT pr_number, title, module_code, author, reviewer, branch_name, status, created_date
        FROM git_pull_requests 
        WHERE title LIKE ? OR author LIKE ? OR module_code LIKE ? OR branch_name LIKE ? LIMIT 5
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    prs = cur.fetchall()

    # 5. Nhật ký Kiểm thử QA
    cur.execute("""
        SELECT module_code, test_name, test_file, tester, test_date, result, fps, latency_ms, error_log
        FROM qa_test_runs
        WHERE test_name LIKE ? OR module_code LIKE ? OR tester LIKE ? LIMIT 5
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    tests = cur.fetchall()

    # 6. Ký ức Lỗi
    cur.execute("""
        SELECT problem_summary, solution_steps, module_code
        FROM error_memories WHERE error_memories MATCH ? LIMIT 5
    """, (keyword,))
    errors = cur.fetchall()

    t_db = (time.time() - t0) * 1000

    print("\n" + "="*90)
    print(f" 🔍 TRA CỨU TOÀN DIỆN KỸ THUẬT: '{keyword}' (Thời gian: {t_db:.2f} ms | Tiêu tốn: 0 Token)")
    print("="*90)

    if docs:
        print("\n📁 [TÀI LIỆU, BẢN VẼ & ĐƯỜNG DẪN Ổ CỨNG]:")
        for d in docs:
            print(f"  • [{d['doc_type']}] {d['title']} (Module: {d['module_code']})")
            print(f"    ➔ ĐƯỜNG DẪN: {d['full_path']}")
            print(f"    ➔ Tác giả: {d['author']} | Phụ trách: {d['assignee']} | Ngày tạo: {d['created_date']}\n")

    if techs:
        print("\n⚙️ [PHÂN RÃ KỸ THUẬT, THUẬT TOÁN & BỘ LỌC]:")
        for tc in techs:
            print(f"  • Module [{tc['module_code']}]: {tc['feature_name']} (Dev: {tc['developer']})")
            print(f"    ➔ Công nghệ: {tc['tech_stack']}")
            print(f"    ➔ Thuật toán: {tc['algorithms']}")
            print(f"    ➔ Bộ lọc: {tc['filters']}\n")

    if diagrams:
        print("\n📊 [SƠ ĐỒ KIẾN TRÚC MERMAID]:")
        for dg in diagrams:
            print(f"  • {dg['title']} ({dg['diagram_type']}) [Tác giả: {dg['author']} | Duyệt: {dg['reviewer']}]")
            print("  Mã Mermaid:")
            print("  ```mermaid\n  " + dg['diagram_code'].replace("\n", "\n  ") + "\n  ```\n")

    if prs:
        print("\n🐙 [GIT & PULL REQUESTS]:")
        for p in prs:
            status_str = f"[{p['status'].upper()}]"
            print(f"  • PR #{p['pr_number']}: {p['title']} {status_str}")
            print(f"    ➔ Người tạo: {p['author']} | Reviewer: {p['reviewer']} | Nhánh: {p['branch_name']} ({p['created_date']})\n")

    if tests:
        print("\n🧪 [NHẬT KÝ KIỂM THỬ QA & CHẤT LƯỢNG]:")
        for ts in tests:
            res_str = f"[{ts['result']}]"
            print(f"  • {ts['test_name']} {res_str} (Module: {ts['module_code']})")
            print(f"    ➔ File test: {ts['test_file']} | Tester: {ts['tester']} ({ts['test_date']})")
            print(f"    ➔ Hiệu năng: {ts['fps']} FPS | Độ trễ: {ts['latency_ms']} ms | Ghi chú: {ts['error_log']}\n")

    if errors:
        print("\n🧠 [KÝ ỨC LỖI & GIẢI PHÁP ĐÃ TEST THÀNH CÔNG]:")
        for e in errors:
            print(f"  • Lỗi: {e['problem_summary']} (Module: {e['module_code']})")
            print(f"    ➔ Cách sửa: {e['solution_steps']}\n")

    if not docs and not techs and not diagrams and not prs and not tests and not errors:
        print(f"  [!] Không tìm thấy dữ liệu nào khớp với từ khóa '{keyword}'.")

    print("="*90 + "\n")
    conn.close()

def show_progress():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name AS pillar_name, m.code, m.name, m.tech_lead, m.progress_pct, m.start_date, m.deadline, m.status
        FROM modules m JOIN pillars p ON m.pillar_id = p.id
        ORDER BY p.id, m.code
    """)
    rows = cur.fetchall()

    print("\n" + "="*95)
    print(" 📊 BẢNG TIẾN ĐỘ 38 MODULE LÂM NGHIỆP (TIẾN ĐỘ %, THỜI HẠN & TECH LEAD)")
    print("="*95)
    current_pillar = None
    for r in rows:
        if r['pillar_name'] != current_pillar:
            current_pillar = r['pillar_name']
            print(f"\n📂 [{current_pillar}]")
        
        bar_len = 15
        filled = int(r['progress_pct'] / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        deadline_str = f"Hạn: {r['deadline']}" if r['deadline'] else ""
        print(f"  [{r['code']}] {r['name']:<35} | {bar} {r['progress_pct']:>3}% | Lead: {r['tech_lead']:<9} | {deadline_str:<15} | {r['status']}")
    print("="*95 + "\n")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "init":
            seed_enterprise_data()
        elif cmd in ["find", "search"]:
            kw = sys.argv[2] if len(sys.argv) > 2 else "camera"
            find_all(kw)
        elif cmd == "progress":
            show_progress()
        else:
            find_all(sys.argv[1])
    else:
        seed_enterprise_data()
        show_progress()
