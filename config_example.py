# -*- coding: utf-8 -*-
"""
Auto9am Configuration Example File
ไฟล์ตัวอย่างการตั้งค่าสำหรับโปรแกรม Auto9am

คำแนะนำ:
1. คัดลอกไฟล์นี้และเปลี่ยนชื่อเป็น config.py
2. แก้ไขข้อมูลต่างๆ ให้ตรงกับข้อมูลของคุณ
3. เก็บไฟล์ config.py ไว้ในโฟลเดอร์เดียวกับ Auto9am.py
"""

# ========================================
# ข้อมูลการเข้าสู่ระบบ (Login Credentials)
# ========================================
LOGIN_CONFIG = {
    # ข้อมูลเข้าสู่ระบบเว็บไซต์ - แก้ไขให้ตรงกับข้อมูลของคุณ
    "username": "your_username_here",  # ← แก้ไขชื่อผู้ใช้ของคุณ
    "password": "your_password_here",  # ← แก้ไขรหัสผ่านของคุณ
    
    # URL ของเว็บไซต์ - ปกติไม่ต้องแก้ไข
    "website_url": "http://csoc.intra.tot.co.th/nt.csoc/",
    "public_url": "http://csoc.intra.tot.co.th/nt.csoc/public/",
    "traffic_report_url": "http://csoc.intra.tot.co.th/nt.csoc/public/trafficReport/"
}

# ========================================
# ข้อมูลการส่งอีเมล (Email Configuration)
# ========================================
EMAIL_CONFIG = {
    # การตั้งค่า SMTP Server - สำหรับ Gmail
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    
    # ข้อมูลผู้ส่ง - แก้ไขให้ตรงกับข้อมูลของคุณ
    "sender_email": "your_email@gmail.com",        # ← แก้ไขอีเมลผู้ส่งของคุณ
    "sender_password": "your_app_password_here",   # ← แก้ไข App Password ของ Gmail
    
    # ข้อมูลผู้รับ - แก้ไขให้ตรงกับผู้รับที่ต้องการ
    "recipient_email": "recipient@example.com",    # ← แก้ไขอีเมลผู้รับ
    
    # หัวข้ออีเมล (จะมีการเพิ่มวันที่ต่อท้าย)
    "subject_prefix": "Traffic Report",
    
}

# ========================================
# ข้อมูลวงจร (Circuit Information)
# ========================================
CIRCUIT_CONFIG = {
    # รายการวงจรที่ต้องการสร้างรายงาน - แก้ไขให้ตรงกับวงจรของคุณ
    "circuits": "2551M0322, 2551M0323, 2133M2632, 2133M2633",  # ← แก้ไขรายการวงจร
    
    # คำอธิบายวงจร (สำหรับใช้ในอีเมล) - แก้ไขให้ตรงกับข้อมูลของคุณ
    "circuit_description": "วงจร 2551M0322, 2551M0323, 2133M2632, 2133M2633 รายงาน Traffic กรมการกงสุล"  # ← แก้ไขคำอธิบาย
}

# ========================================
# การตั้งค่าไฟล์ (File Configuration)
# ========================================
FILE_CONFIG = {
    # รูปแบบชื่อไฟล์ที่ดาวน์โหลดจากเว็บ - ปกติไม่ต้องแก้ไข
    "download_file_prefix": "GXE00-64-0016_",
    
    # รูปแบบชื่อไฟล์ใหม่ - สามารถแก้ไขได้ตามต้องการ
    "new_file_prefix": "CWM_",                    # ← แก้ไขคำนำหน้าชื่อไฟล์ใหม่
    
    # รูปแบบชื่โฟลเดอร์ - สามารถแก้ไขได้ตามต้องการ
    "folder_prefix": "Traffic_Report_",           # ← แก้ไขคำนำหน้าชื่อโฟลเดอร์
    
    # เวลาที่รอหาไฟล์ที่ดาวน์โหลด (วินาที)
    "file_search_timeout": 120  # 2 นาที
}

# ========================================
# การตั้งค่า WebDriver (WebDriver Configuration)
# ========================================
WEBDRIVER_CONFIG = {
    # เส้นทางไปยัง Edge WebDriver - แก้ไขให้ตรงกับเส้นทางของคุณ
    "driver_paths": [
        r'C:\Users\YourUsername\OneDrive\Desktop\Auto9am\edgedriver_win32\msedgedriver.exe',  # ← แก้ไขเส้นทาง
        r'C:\edgedriver\msedgedriver.exe',  # เส้นทางสำรอง
        r'.\edgedriver_win32\msedgedriver.exe',  # เส้นทางสำรอง
    ],
    
    # การตั้งค่า Browser Options
    "headless_mode": True,      # True = ไม่แสดงหน้าจอ, False = แสดงหน้าจอ
    "window_size": "1920,1080", # ขนาดหน้าต่าง
    "disable_images": True,     # ปิดการโหลดรูปภาพเพื่อเพิ่มความเร็ว
    
    # Timeout สำหรับการรอ (วินาที)
    "page_load_timeout": 60,    # เวลารอโหลดหน้า
    "element_wait_timeout": 15, # เวลารอหา element
    "results_wait_timeout": 60  # เวลารอผลลัพธ์
}

# ========================================
# ข้อความในอีเมล (Email Body)
# ========================================
# แก้ไขข้อความนี้ให้ตรงกับที่ต้องการ - สามารถก็อปวางได้เลย
EMAIL_BODY = """เรียน กรมการกงสุล,



       ขออนุญาตส่งรายงาน Traffic กรมการกงสุล

วงจร 2551M0322, 2551M0323, 2133M2632, 2133M2633 รายงาน Traffic กรมการกงสุล วันที่ {report_date}



Best Regards,



Hussayakorn L,

NT CSOC Manage Service

Solutions Product After Sales Service Sector

National Telecom Public Company Limited

Tel: +66 (2) 159 9555

Fax: +66 (2) 568 2131

************
"""

# ========================================
# ฟังก์ชันสำหรับดึงข้อมูล
# ========================================
def get_login_config():
    """ดึงข้อมูลการเข้าสู่ระบบ"""
    return LOGIN_CONFIG

def get_email_config():
    """ดึงข้อมูลการส่งอีเมล"""
    return EMAIL_CONFIG

def get_circuit_config():
    """ดึงข้อมูลวงจร"""
    return CIRCUIT_CONFIG

def get_file_config():
    """ดึงข้อมูลการจัดการไฟล์"""
    return FILE_CONFIG

def get_webdriver_config():
    """ดึงข้อมูลการตั้งค่า WebDriver"""
    return WEBDRIVER_CONFIG

def get_email_body():
    """ดึงเนื้อหาอีเมล"""
    return EMAIL_BODY

# ========================================
# ฟังก์ชันสำหรับสร้างเนื้อหาอีเมล
# ========================================
def create_email_body(report_date):
    """สร้างเนื้อหาอีเมล"""
    return EMAIL_BODY.format(report_date=report_date)

def create_email_subject(folder_name):
    """สร้างหัวข้ออีเมล"""
    email_config = get_email_config()
    return f"{email_config['subject_prefix']} - {folder_name}"
