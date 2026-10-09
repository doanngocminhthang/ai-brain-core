"""
HỆ THỐNG QUẢN TRỊ TRÍ NHỚ VÀ TIẾN ĐỘ ĐA TÁC NHÂN (AI BRAIN CORE)
Tối ưu cho Antigravity & Claude Code (Laptop & Máy bàn)
Quản lý 38 Module, 3 Trụ cột Lâm nghiệp, Đối chiếu Task Dev, Kho Sơ đồ & Đường dẫn tài liệu
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

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
    -- 1. BẢNG 3 TRỤ CỘT LỚN
    CREATE TABLE IF NOT EXISTS pillars (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    );

    -- 2. BẢNG 38 MODULES (TIẾN ĐỘ % & CHẤT LƯỢNG)
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pillar_id TEXT NOT NULL REFERENCES pillars(id),
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        ssot_path TEXT NOT NULL,
        progress_pct INTEGER DEFAULT 0,
        quality_score TEXT DEFAULT 'A',
        status TEXT DEFAULT 'in_progress',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 3. BẢNG ĐỐI CHIẾU TASK CỦA DEV (DEV TASK MAPPING)
    CREATE TABLE IF NOT EXISTS dev_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_code TEXT NOT NULL REFERENCES modules(code),
        dev_name TEXT NOT NULL,
        task_title TEXT NOT NULL,
        status TEXT DEFAULT 'in_progress', -- in_progress, review_pending, passed, failed
        code_branch TEXT,
        pr_link TEXT,
        notes TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 4. BẢNG CHỈ MỤC ĐƯỜNG DẪN & BẢN VẼ TÀI LIỆU (FTS5 TÌM KIẾM TRONG 0.001s)
    CREATE VIRTUAL TABLE IF NOT EXISTS path_index USING fts5(
        item_title,
        item_type,     -- 'BẢN VẼ KIẾN TRÚC', 'TÀI LIỆU KỸ THUẬT', 'FILE CẤU HÌNH', 'THƯ MỤC SSOT', 'WEIGHTS MODEL'
        full_path,
        description,
        module_code
    );

    -- 5. KHO SƠ ĐỒ MERMAID (FTS5 TÌM KIẾM NỘI DUNG)
    CREATE VIRTUAL TABLE IF NOT EXISTS mermaid_vault USING fts5(
        title,
        pillar_id,
        module_code,
        diagram_type,
        diagram_code,
        tags
    );

    -- 6. BẢNG KÝ ỨC LỖI & SỬA LỖI (TROUBLESHOOTING MEMORY)
    CREATE VIRTUAL TABLE IF NOT EXISTS error_memories USING fts5(
        problem_summary,
        solution_steps,
        tags,
        module_code
    );
    """)
    conn.commit()
    conn.close()

def seed_full_ecosystem():
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    # 1. Nạp 3 Trụ cột
    cur.executemany("INSERT OR REPLACE INTO pillars (id, name, description) VALUES (?, ?, ?)", [
        ("CHAY_RUNG", "1. AI GIÁM SÁT CHÁY RỪNG", "Camera PTZ, YOLO khói/lửa, FWI/Nesterov, Cảnh báo tức thời"),
        ("BIEN_DONG", "2. AI BIẾN ĐỘNG RỪNG", "Ảnh viễn thám Sentinel-2/Landsat, Chỉ số NDVI/NBR, Mất rừng"),
        ("AN_NINH", "3. AI AN NINH RỪNG", "Xâm nhập người/xe, Bẫy ảnh hồng ngoại, Cảnh báo âm thanh cưa máy")
    ])

    # 2. Nạp đại diện trong 38 Modules
    cur.execute("DELETE FROM modules")
    modules = [
        # Trụ cột Cháy rừng (Module 01 - 15)
        ("CHAY_RUNG", "MOD_01", "Thu nhận RTSP Camera Dahua PTZ", "D:/main_workspace/dev/wildfire/camera_service/", 100, "A+", "completed"),
        ("CHAY_RUNG", "MOD_02", "Nhận diện Khói Lửa YOLOv8", "D:/main_workspace/dev/wildfire/ai_models/smoke/", 85, "A", "in_progress"),
        ("CHAY_RUNG", "MOD_03", "Trạm Khí tượng & Chỉ số Nesterov", "D:/main_workspace/dev/wildfire/weather_fwi/", 60, "B+", "in_progress"),
        ("CHAY_RUNG", "MOD_04", "Bản đồ Nhiệt & Vết Cháy Tức thời", "D:/main_workspace/dev/wildfire/thermal_map/", 45, "B", "in_progress"),
        ("CHAY_RUNG", "MOD_05", "Điều khiển Góc quay PTZ (ONVIF)", "D:/main_workspace/dev/wildfire/ptz_control/", 90, "A", "in_progress"),

        # Trụ cột Biến động rừng (Module 16 - 27)
        ("BIEN_DONG", "MOD_16", "Thu nhận Ảnh Vệ tinh Sentinel-2", "D:/main_workspace/dev/wildfire/satellite_pipeline/", 90, "A", "in_progress"),
        ("BIEN_DONG", "MOD_17", "Tính toán Chỉ số NDVI & NBR", "D:/main_workspace/dev/wildfire/gis_indices/", 70, "B+", "in_progress"),
        ("BIEN_DONG", "MOD_18", "Phát hiện Rừng bị Chặt hạ (Change)", "D:/main_workspace/dev/wildfire/deforestation_ai/", 35, "C", "in_progress"),

        # Trụ cột An ninh rừng (Module 28 - 38)
        ("AN_NINH", "MOD_28", "Nhận diện Người/Xe Xâm nhập Trái phép", "D:/main_workspace/dev/wildfire/intrusion_detect/", 80, "A", "in_progress"),
        ("AN_NINH", "MOD_29", "Phát hiện Âm thanh Tiếng cưa máy", "D:/main_workspace/dev/wildfire/audio_sensor/", 50, "B", "in_progress"),
        ("AN_NINH", "MOD_30", "Bẫy ảnh Hồng ngoại Ban đêm", "D:/main_workspace/dev/wildfire/night_traps/", 25, "C", "in_progress"),
    ]
    cur.executemany("""
        INSERT INTO modules (pillar_id, code, name, ssot_path, progress_pct, quality_score, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, modules)

    # 3. Nạp Bảng đối chiếu Task của Dev
    cur.execute("DELETE FROM dev_tasks")
    dev_tasks = [
        ("MOD_01", "Bạn Nam (BE)", "Fix lỗi buffer overflow khi mất kết nối RTSP", "passed", "fix/rtsp-buffer", "PR #12", "Đã test 48h liên tục không leak RAM"),
        ("MOD_02", "Bạn Huy (AI)", "Train lại YOLOv8x thêm 5,000 ảnh khói mù sương", "in_progress", "ai/yolo-smoke-v2", "PR #15", "Đang train epoch 65/100"),
        ("MOD_05", "Bạn Tuấn (IoT)", "Viết API điều khiển Zoom 30x Camera qua giao thức ONVIF", "review_pending", "feat/onvif-zoom", "PR #18", "Cần lead duyệt chuẩn delay < 100ms"),
        ("MOD_17", "Bạn Trang (GIS)", "Tối ưu hàm tính NBR raster bằng thư viện Rasterio song song", "passed", "feat/raster-parallel", "PR #14", "Giảm thời gian xử lý từ 12s xuống 1.5s"),
        ("MOD_29", "Bạn Hoàng (DSP)", "Lọc nhiễu tiếng gió và tiếng côn trùng trước khi đưa vào AudioNet", "in_progress", "ai/audio-filter", "PR #20", "Độ chính xác hiện tại 78%"),
    ]
    cur.executemany("""
        INSERT INTO dev_tasks (module_code, dev_name, task_title, status, code_branch, pr_link, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, dev_tasks)

    # 4. Nạp Bảng Chỉ mục Đường dẫn & Bản vẽ Tài liệu (Sếp hỏi gõ ra ngay!)
    cur.execute("DELETE FROM path_index")
    paths = [
        ("Bản vẽ Kiến trúc Hệ thống Tổng thể", "BẢN VẼ KIẾN TRÚC", "D:/main_workspace/docs/architecture/system_overview_v2.png", "Sơ đồ kiến trúc toàn cảnh 3 trụ cột kết nối trạm camera, vệ tinh và máy chủ trung tâm", "ALL"),
        ("Bản vẽ Luồng Dữ liệu RTSP & AI Pipeline", "BẢN VẼ KIẾN TRÚC", "D:/main_workspace/docs/architecture/rtsp_ai_pipeline.svg", "Sơ đồ luồng dữ liệu thời gian thực từ camera PTZ về cụm GPU xử lý", "MOD_01"),
        ("Tài liệu Đặc tả Giao thức ONVIF Camera Dahua", "TÀI LIỆU KỸ THUẬT", "D:/main_workspace/docs/specs/Dahua_PTZ_ONVIF_ProfileS_Spec.pdf", "Tài liệu đặc tả lệnh xoay Pan/Tilt/Zoom và Preset góc quan sát", "MOD_05"),
        ("File Cấu hình Mạng & Địa chỉ IP 12 Trạm Camera", "FILE CẤU HÌNH", "D:/main_workspace/dev/wildfire/config/camera_network_ip.yaml", "Chứa toàn bộ IP tĩnh, cổng RTSP và mật khẩu trạm camera", "MOD_01"),
        ("Trọng số Mô hình YOLOv8 Khói Lửa Tốt Nhất", "WEIGHTS MODEL", "D:/main_workspace/dev/wildfire/weights/smoke_best_v8x.pt", "Trọng số TensorRT tối ưu cho GPU GTX 1050Ti/RTX", "MOD_02"),
        ("Tài liệu Thuật toán Dự báo Nguy cơ Cháy Nesterov", "TÀI LIỆU KỸ THUẬT", "D:/main_workspace/docs/algorithms/Nesterov_Fire_Risk_Formulas.docx", "Công thức toán học tính chỉ số P dựa trên nhiệt độ và độ ẩm lúc 13h", "MOD_03"),
        ("Bản đồ Ranh giới Rừng Phòng hộ Thanh Hóa (Shapefile)", "TÀI LIỆU KỸ THUẬT", "D:/main_workspace/gis_data/thanh_hoa_protection_forest.shp", "Dữ liệu lớp phủ không gian ranh giới 7 huyện vùng cao Thanh Hóa", "MOD_17"),
    ]
    cur.executemany("""
        INSERT INTO path_index (item_title, item_type, full_path, description, module_code)
        VALUES (?, ?, ?, ?, ?)
    """, paths)

    # 5. Nạp Sơ đồ Mermaid
    cur.execute("DELETE FROM mermaid_vault")
    diagrams = [
        ("Bản vẽ Luồng Camera PTZ và YOLO", "CHAY_RUNG", "MOD_01", "flowchart", 
         "flowchart LR\n A[Camera Dahua PTZ (RTSP)] -->|TCP| B[OpenCV VideoCapture]\n B -->|Threaded Queue| C[YOLOv8 Smoke AI]\n C -->|Alert > 80%| D[MinIO S3 & WebSocket GIS]", "camera,ptz,rtsp,yolo,dahua,kien_truc"),
        ("Quy trình Đa Tác nhân Antigravity & Claude Code", "ALL", "ALL", "sequenceDiagram",
         "sequenceDiagram\n Lead->>Antigravity: Giao việc & Review\n Antigravity->>SQLite: Tra cứu Path & Lỗi cũ\n Antigravity->>ClaudeCode: Ủy quyền sửa code nhánh Dev\n ClaudeCode-->>Lead: Báo cáo kết quả test", "multi_agent,quy_trinh,claude,antigravity"),
        ("Kiến trúc Bản đồ Vệ tinh Sentinel-2", "BIEN_DONG", "MOD_16", "flowchart",
         "flowchart TD\n Sat[Vệ tinh Sentinel-2] --> Copernicus[Copernicus API] --> Worker[GeoTIFF Worker] --> Calc[Tính NDVI & NBR] --> Map[Leaflet GIS Dashboard]", "ve_tinh,sentinel,ndvi,gis,copernicus")
    ]
    cur.executemany("""
        INSERT INTO mermaid_vault (title, pillar_id, module_code, diagram_type, diagram_code, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, diagrams)

    # 6. Nạp Bộ nhớ Lỗi
    cur.execute("DELETE FROM error_memories")
    errors = [
        ("Lỗi drop frame và timeout RTSP Camera Dahua sau 2h", 
         "1. Ép OPENCV_FFMPEG_CAPTURE_OPTIONS=rtsp_transport;tcp\n2. Tăng buffer kích thước 2048\n3. Dùng vòng lặp luồng ngầm giải phóng frame cũ liên tục", "camera,ptz,rtsp,opencv,drop_frame", "MOD_01"),
        ("Lỗi CUDA out of memory khi chạy mô hình YOLOv8x trên GPU 4GB", 
         "1. Giảm batch size về 1\n2. Chuyển mô hình sang TensorRT FP16 (tiết kiệm 50% VRAM)\n3. Set biến torch.cuda.empty_cache()", "yolo,cuda,vram,gpu,oom", "MOD_02"),
        ("Lỗi tràn RAM khi nạp ảnh GeoTIFF vệ tinh kích thước 4GB",
         "Sử dụng thư viện Rasterio đọc theo từng block cửa sổ nhỏ (windowed reading) thay vì nạp toàn bộ mảng numpy", "rasterio,geotiff,ram,sentinel", "MOD_17"),
    ]
    cur.executemany("""
        INSERT INTO error_memories (problem_summary, solution_steps, tags, module_code)
        VALUES (?, ?, ?, ?)
    """, errors)

    conn.commit()
    conn.close()
    print("[OK] Đã nạp thành công 100% Hệ sinh thái AI Brain Core tại: " + str(DB_PATH))

def quick_find(keyword):
    """Tìm kiếm siêu tốc mọi tài liệu, bản vẽ, đường dẫn, task dev, sơ đồ trong 0.001s"""
    conn = get_conn()
    cur = conn.cursor()

    t0 = time.time()
    
    # 1. Tìm trong Bảng Chỉ mục Đường dẫn & Bản vẽ
    cur.execute("""
        SELECT item_title, item_type, full_path, description, module_code 
        FROM path_index WHERE path_index MATCH ? LIMIT 10
    """, (keyword,))
    paths = cur.fetchall()

    # 2. Tìm trong Kho Sơ đồ Mermaid
    cur.execute("""
        SELECT title, diagram_type, diagram_code, module_code, tags
        FROM mermaid_vault WHERE mermaid_vault MATCH ? LIMIT 5
    """, (keyword,))
    diagrams = cur.fetchall()

    # 3. Tìm trong Task của Dev
    cur.execute("""
        SELECT module_code, dev_name, task_title, status, pr_link, notes
        FROM dev_tasks WHERE dev_name LIKE ? OR task_title LIKE ? OR module_code LIKE ? LIMIT 5
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    tasks = cur.fetchall()

    # 4. Tìm trong Bộ nhớ lỗi
    cur.execute("""
        SELECT problem_summary, solution_steps, module_code
        FROM error_memories WHERE error_memories MATCH ? LIMIT 5
    """, (keyword,))
    errors = cur.fetchall()

    t_db = (time.time() - t0) * 1000

    print("\n" + "="*85)
    print(f" 🔍 KẾT QUẢ TÌM KIẾM NHANH: '{keyword}' (Thời gian: {t_db:.2f} ms | Tiêu tốn: 0 Token)")
    print("="*85)

    if paths:
        print("\n📁 [BẢN VẼ, TÀI LIỆU & ĐƯỜNG DẪN Ổ CỨNG]:")
        for p in paths:
            print(f"  • [{p['item_type']}] {p['item_title']} (Module: {p['module_code']})")
            print(f"    ➔ ĐƯỜNG DẪN: {p['full_path']}")
            print(f"    ➔ Mô tả: {p['description']}\n")

    if diagrams:
        print("\n📊 [SƠ ĐỒ KIẾN TRÚC MERMAID]:")
        for d in diagrams:
            print(f"  • Tiêu đề: {d['title']} ({d['diagram_type']}) [Module: {d['module_code']}]")
            print("  Mã Mermaid:")
            print("  ```mermaid\n  " + d['diagram_code'].replace("\n", "\n  ") + "\n  ```\n")

    if tasks:
        print("\n👨‍💻 [ĐỐI CHIẾU TIẾN ĐỘ TASK CỦA DEV]:")
        for t in tasks:
            print(f"  • Dev: {t['dev_name']} | Module: {t['module_code']} | Trạng thái: {t['status'].upper()}")
            print(f"    ➔ Task: {t['task_title']} ({t['pr_link']})")
            print(f"    ➔ Ghi chú: {t['notes']}\n")

    if errors:
        print("\n🧠 [KÝ ỨC SỬA LỖI & KINH NGHIỆM ĐÃ TEST]:")
        for e in errors:
            print(f"  • Lỗi: {e['problem_summary']} (Module: {e['module_code']})")
            print(f"    ➔ Cách sửa: {e['solution_steps']}\n")

    if not paths and not diagrams and not tasks and not errors:
        print(f"  [!] Không tìm thấy mục nào khớp với từ khóa '{keyword}'.")

    print("="*85 + "\n")
    conn.close()

def show_progress():
    """Hiển thị bảng tiến độ % của 3 Trụ cột và Modules"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name AS pillar_name, m.code, m.name, m.progress_pct, m.quality_score, m.status, m.ssot_path
        FROM modules m JOIN pillars p ON m.pillar_id = p.id
        ORDER BY p.id, m.code
    """)
    rows = cur.fetchall()

    print("\n" + "="*85)
    print(" 📊 BẢNG THEO DÕI TIẾN ĐỘ % THỰC TẾ (3 TRỤ CỘT & 38 MODULE LÂM NGHIỆP)")
    print("="*85)
    current_pillar = None
    for r in rows:
        if r['pillar_name'] != current_pillar:
            current_pillar = r['pillar_name']
            print(f"\n📂 [{current_pillar}]")
        
        bar_len = 16
        filled = int(r['progress_pct'] / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  [{r['code']}] {r['name']:<38} | {bar} {r['progress_pct']:>3}% | Điểm: {r['quality_score']} | {r['status']}")
    print("="*85 + "\n")
    conn.close()

def show_dev_tasks():
    """Hiển thị toàn bộ task của team dev"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT dt.module_code, m.name AS module_name, dt.dev_name, dt.task_title, dt.status, dt.code_branch, dt.pr_link, dt.notes
        FROM dev_tasks dt JOIN modules m ON dt.module_code = m.code
        ORDER BY dt.dev_name
    """)
    rows = cur.fetchall()

    print("\n" + "="*85)
    print(" 👨‍💻 BẢNG THEO DÕI TIẾN ĐỘ TASK CỦA CÁC DEV (DEV TASK TRACKER)")
    print("="*85)
    for r in rows:
        status_badge = f"[{r['status'].upper()}]"
        print(f"{r['dev_name']:<18} | {r['module_code']} - {r['module_name']:<25} | {status_badge:<12}")
        print(f"  ➔ Task: {r['task_title']} ({r['pr_link']} @ {r['code_branch']})")
        print(f"  ➔ Đánh giá/Ghi chú: {r['notes']}\n")
    print("="*85 + "\n")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "init":
            seed_full_ecosystem()
        elif cmd in ["find", "search"]:
            kw = sys.argv[2] if len(sys.argv) > 2 else "kiến trúc"
            quick_find(kw)
        elif cmd == "progress":
            show_progress()
        elif cmd in ["dev", "tasks", "dev-tasks"]:
            show_dev_tasks()
        else:
            quick_find(sys.argv[1])
    else:
        seed_full_ecosystem()
        show_progress()
