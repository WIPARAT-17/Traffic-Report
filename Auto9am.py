from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import os
import glob
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# นำเข้าข้อมูลการตั้งค่าจากไฟล์ config.py
from config import (
    get_login_config, get_email_config, get_circuit_config,
    get_file_config, get_webdriver_config, get_email_body,
    create_email_body, create_email_subject
)

# โหลดการตั้งค่าจากไฟล์ config
webdriver_config = get_webdriver_config()
file_config = get_file_config()

# ตั้งค่า Edge Options สำหรับการดาวน์โหลดอัตโนมัติ
edge_options = Options()

# ตั้งค่าโฟลเดอร์ดาวน์โหลด - ใช้โฟลเดอร์ Downloads ของ Windows
from pathlib import Path

# หาโฟลเดอร์ Downloads ของ Windows
user_downloads = str(Path.home() / "Downloads")
download_dir = user_downloads

print(f"โฟลเดอร์ดาวน์โหลด: {download_dir}")

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# ตั้งค่าการดาวน์โหลดอัตโนมัติ
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # ไม่ถามก่อนดาวน์โหลด
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,  # ปิด safe browsing
    "profile.default_content_setting_values.automatic_downloads": 1,  # อนุญาตการดาวน์โหลดอัตโนมัติ
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
    "profile.default_content_settings.popups": 0,  # ปิดป๊อปอัพ
    "profile.managed_default_content_settings": {"downloads": 1},  # อนุญาตการดาวน์โหลด
}

print(f"ตั้งค่าการดาวน์โหลดไปที่: {download_dir}")

# เพิ่ม arguments สำหรับ Edge
edge_options.add_argument("--disable-popup-blocking")  # ปิดการบล็อกป๊อปอัพ
'''
# ตั้งค่า Headless Mode ตามการกำหนดค่าในไฟล์ config
if webdriver_config["headless_mode"]:
    print("🚀 เริ่มต้นโปรแกรม Auto9am - โหมดเบื้องหลัง (Headless Mode)")
    # เพิ่ม arguments สำหรับ Headless Mode (ทำงานเบื้องหลังไม่แสดงหน้าจอ)
    edge_options.add_argument("--headless=new")  # ใช้ headless mode รุ่นใหม่
    edge_options.add_argument("--disable-gpu")  # ปิด GPU acceleration
    edge_options.add_argument("--no-sandbox")  # ปิด sandbox mode
    edge_options.add_argument("--disable-dev-shm-usage")  # ลดการใช้ shared memory
    edge_options.add_argument("--disable-extensions")  # ปิด extensions
    edge_options.add_argument("--disable-plugins")  # ปิด plugins

    if webdriver_config["disable_images"]:
        edge_options.add_argument("--disable-images")  # ปิดการโหลดรูปภาพเพื่อเพิ่มความเร็ว

    edge_options.add_argument(f"--window-size={webdriver_config['window_size']}")  # กำหนดขนาดหน้าต่าง
    edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")  # กำหนด user agent
else:
    print("🖥️ เริ่มต้นโปรแกรม Auto9am - โหมดแสดงหน้าจอ")'''

# ตั้งค่า preferences
edge_options.add_experimental_option("prefs", prefs)

# ระบุเส้นทางไปยัง Edge WebDriver - ใช้ข้อมูลจาก config
possible_driver_paths = webdriver_config["driver_paths"]

driver_path = None
for path in possible_driver_paths:
    if os.path.exists(path):
        driver_path = path
        print(f"✓ พบ Edge WebDriver ที่: {path}")
        break

if not driver_path:
    print("❌ ไม่พบ Edge WebDriver ในตำแหน่งใดๆ")
    print("กรุณาดาวน์โหลด Edge WebDriver จาก: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    exit(1)

service = Service(driver_path)

# โหลดการตั้งค่าการเข้าสู่ระบบ
login_config = get_login_config()

if webdriver_config["headless_mode"]:
    print("📱 กำลังเปิด Edge WebDriver แบบไม่แสดงหน้าจอ...")
else:
    print("🖥️ กำลังเปิด Edge WebDriver แบบแสดงหน้าจอ...")

driver = webdriver.Edge(service=service, options=edge_options)

print("🌐 กำลังเชื่อมต่อไปยังเว็บไซต์...")
# เปิดหน้าเว็บไซต์
driver.get(login_config["website_url"])

try:
    print("🔐 กำลังเข้าสู่ระบบ...")
    # ----------------------------------------------------
    #  1. ค้นหาและกรอก Username และ Password
    # ----------------------------------------------------
    username_field = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='User intra']"))
    )
    username_field.send_keys(login_config["username"])

    password_field = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pass intra']"))
    )
    password_field.send_keys(login_config["password"])
    print("✅ กรอกข้อมูลเข้าสู่ระบบเรียบร้อย")

    # ----------------------------------------------------
    #  2. คลิกปุ่ม "Continue"
    # ----------------------------------------------------
    print("🔄 กำลังเข้าสู่ระบบ...")
    continue_button = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.element_to_be_clickable((By.ID, "submit"))
    )
    continue_button.click()

    # ----------------------------------------------------
    #  3. ไปยังหน้า Public และคลิก "Traffic Report"
    # ----------------------------------------------------
    print("⏳ รอการเข้าสู่หน้าหลัก...")
    WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.url_to_be(login_config["public_url"])
    )
    print("✅ เข้าสู่หน้าหลักสำเร็จ")

    # ใช้ JavaScript ในการค้นหาและคลิกปุ่ม Traffic Report
    print("🔍 กำลังค้นหาปุ่ม Traffic Report...")
    traffic_report_selector = "#list-app > div:nth-child(4) > div:nth-child(7) > a"
    traffic_report_element = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, traffic_report_selector))
    )
    driver.execute_script("arguments[0].click();", traffic_report_element)

    print("✅ คลิกปุ่ม 'Traffic Report' สำเร็จแล้ว!")

    # ----------------------------------------------------
    #  4. กรอกข้อมูลวงจร, วันที่เริ่มต้น และคลิกปุ่ม "สร้าง"
    # ----------------------------------------------------
    print("⏳ รอการโหลดหน้า Traffic Report...")
    WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.url_to_be(login_config["traffic_report_url"])
    )
    print("✅ เข้าสู่หน้า Traffic Report สำเร็จ")

    # โหลดข้อมูลวงจรจาก config
    circuit_config = get_circuit_config()

    # แก้ไข ID ของช่องกรอกข้อมูลวงจรให้ถูกต้อง
    print("📝 กำลังกรอกข้อมูลวงจร...")
    circuit_field = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.presence_of_element_located((By.ID, "f_circuit"))
    )
    circuits = circuit_config["circuits"]
    circuit_field.send_keys(circuits)
    print(f"✅ กรอกข้อมูลวงจร: {circuits}")

    # กำหนดวันที่เริ่มต้นและสิ้นสุด
    print("📅 กำลังตั้งค่าวันที่...")
    # ใช้วันที่ปัจจุบัน
    today = datetime.now().date()
    start_date = today - timedelta(days=1)  # เมื่อวาน
    end_date = today  # วันนี้

    # รูปแบบวันที่: MM-DD-YYYY
    start_date_str = start_date.strftime('%m-%d-%Y')
    end_date_str = end_date.strftime('%m-%d-%Y')
    print(f"📅 วันที่เริ่มต้น: {start_date_str}")
    print(f"📅 วันที่สิ้นสุด: {end_date_str}")

    # ตั้งค่าวันที่เริ่มต้นด้วย JavaScript (ลองหลายรูปแบบ)
    print("📅 กำลังตั้งค่าวันที่ในฟอร์ม...")
    start_date_field = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.presence_of_element_located((By.ID, "f_date_start"))
    )

    # ตั้งค่าวันที่เริ่มต้น
    driver.execute_script(f"arguments[0].value = '{start_date_str}';", start_date_field)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", start_date_field)

    # ตั้งค่าวันที่สิ้นสุด
    end_date_field = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.presence_of_element_located((By.ID, "f_date_end"))
    )
    driver.execute_script(f"arguments[0].value = '{end_date_str}';", end_date_field)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", end_date_field)
    print("✅ ตั้งค่าวันที่เรียบร้อย")

    # รอให้ฟอร์มพร้อม
    print("⏳ รอให้ฟอร์มพร้อม...")
    time.sleep(3)

    # หาและคลิกปุ่ม "สร้าง"
    print("🔄 กำลังสร้างรายงาน...")
    create_button = WebDriverWait(driver, webdriver_config["element_wait_timeout"]).until(
        EC.element_to_be_clickable((By.ID, "submit"))
    )

    # คลิกปุ่ม "สร้าง"
    driver.execute_script("arguments[0].click();", create_button)
    print("✅ คลิกปุ่มสร้างรายงานแล้ว")

    # รอให้หน้าผลลัพธ์โหลดขึ้นมา
    def wait_for_results_page():
        try:
            # รอให้ตารางข้อมูลปรากฏ
            WebDriverWait(driver, webdriver_config["results_wait_timeout"]).until(
                EC.presence_of_element_located((By.ID, "resdata"))
            )
            time.sleep(5)
            return True
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการรอหน้าผลลัพธ์: {e}")
            return False

    # รอให้หน้าผลลัพธ์พร้อม
    results_ready = wait_for_results_page()

    if results_ready:
        print("🎉 หน้าผลลัพธ์โหลดเสร็จสมบูรณ์!")
        time.sleep(15)

        # เปลี่ยนชื่อและย้ายไฟล์ PDF ที่ดาวน์โหลดจากเว็บ Traffic Report
        def rename_and_move_files():
                """เปลี่ยนชื่อและย้ายไฟล์ PDF จากเว็บ Traffic Report ไปยังโฟลเดอร์ใหม่"""
                try:
                    # สร้างส่วนวันที่สำหรับชื่อไฟล์และโฟลเดอร์
                    folder_date_str = end_date.strftime('%d%m%Y')  # สำหรับชื่อโฟลเดอร์

                    # สร้างโฟลเดอร์ Traffic_Report_วันเดือนปี
                    traffic_folder_name = f"{file_config['folder_prefix']}{folder_date_str}"
                    traffic_folder_path = os.path.join(download_dir, traffic_folder_name)

                    if not os.path.exists(traffic_folder_path):
                        os.makedirs(traffic_folder_path)
                        print(f"📁 สร้างโฟลเดอร์: {traffic_folder_name}")
                    else:
                        print(f"📁 โฟลเดอร์มีอยู่แล้ว: {traffic_folder_name}")

                    # หาเฉพาะไฟล์ PDF ที่ดาวน์โหลดมาจากเว็บไซต์ Traffic Report
                    import time as time_module
                    current_time = time_module.time()
                    all_files = []

                    # ตรวจสอบไฟล์ PDF ในโฟลเดอร์ Downloads
                    for file_path in glob.glob(os.path.join(download_dir, "*.pdf")):
                        if os.path.isfile(file_path):
                            file_time = os.path.getmtime(file_path)
                            file_name = os.path.basename(file_path)

                            # เฉพาะไฟล์ PDF ที่สร้างในช่วงเวลาที่กำหนด (ไฟล์ที่เพิ่งดาวน์โหลด)
                            if current_time - file_time < file_config["file_search_timeout"]:
                                # และมีชื่อขึ้นต้นตามที่กำหนดใน config (ไฟล์รายงานจากเว็บ Traffic Report)
                                if file_name.startswith(file_config["download_file_prefix"]) and file_name.endswith(".pdf"):
                                    all_files.append(file_path)
                                    print(f"📄 พบไฟล์ PDF ที่เพิ่งดาวน์โหลดจากเว็บ: {file_name}")

                    print(f"📊 พบไฟล์ PDF ที่เพิ่งดาวน์โหลดจากเว็บ Traffic Report: {len(all_files)} ไฟล์")

                    if not all_files:
                        print("⚠ ไม่พบไฟล์ PDF ที่เพิ่งดาวน์โหลดจากเว็บ Traffic Report")
                        return

                    for file_path in all_files:
                        try:
                            # แยกชื่อไฟล์และ extension
                            file_name = os.path.basename(file_path)
                            name_without_ext = os.path.splitext(file_name)[0]
                            extension = os.path.splitext(file_name)[1]

                            # ดึงเลขวงจรจากชื่อไฟล์เดิม
                            circuit_number = ""
                            if "_" in name_without_ext:
                                parts = name_without_ext.split("_")
                                if len(parts) >= 2:
                                    circuit_number = parts[1]  # ส่วนหลัง _

                            # ถ้าไม่พบเลขวงจร ใช้ชื่อไฟล์เดิม
                            if not circuit_number:
                                circuit_number = name_without_ext

                            # สร้างชื่อไฟล์ใหม่ตามรูปแบบที่กำหนดใน config
                            if not extension:
                                extension = ".pdf"

                            new_file_name = f"{file_config['new_file_prefix']}{circuit_number}_{end_date.strftime('%d%m%Y')}{extension}"

                            # เปลี่ยนชื่อและย้ายไฟล์ไปยังโฟลเดอร์ Traffic_Report
                            if os.path.exists(file_path):
                                # เปลี่ยนชื่อและย้ายไปยังโฟลเดอร์ใหม่
                                final_file_path = os.path.join(traffic_folder_path, new_file_name)
                                shutil.move(file_path, final_file_path)
                                print(f"✓ เปลี่ยนชื่อและย้าย: {file_name}")
                                print(f"  → {traffic_folder_name}/{new_file_name}")
                            else:
                                print(f"⚠ ไม่พบไฟล์: {file_name}")

                        except Exception as e:
                            print(f"❌ เปลี่ยนชื่อไฟล์ {file_name} ไม่สำเร็จ: {e}")

                    print(f"🎉 เปลี่ยนชื่อและย้ายไฟล์เสร็จสิ้น!")
                    print(f"📁 ไฟล์ถูกเก็บไว้ในโฟลเดอร์: {traffic_folder_path}")

                    # ส่งไฟล์ผ่าน email
                    send_email_with_files(traffic_folder_path, traffic_folder_name)

                except Exception as e:
                    print(f"❌ เกิดข้อผิดพลาดในการเปลี่ยนชื่อและย้ายไฟล์: {e}")

        # ฟังก์ชันส่ง email
        def send_email_with_files(folder_path, folder_name):
            """ส่งไฟล์ PDF ผ่าน email"""
            try:
                # โหลดการตั้งค่าอีเมลจาก config
                email_config = get_email_config()

                # สร้าง email message
                msg = MIMEMultipart()
                msg['From'] = email_config["sender_email"]
                msg['To'] = email_config["recipient_email"]
                msg['Subject'] = create_email_subject(folder_name)

                # เนื้อหา email - ใช้เทมเพลตจาก config
                body = create_email_body(end_date.strftime('%d/%m/%Y'))
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                # หาไฟล์ PDF ในโฟลเดอร์
                pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

                if not pdf_files:
                    print("⚠ ไม่พบไฟล์ PDF ในโฟลเดอร์เพื่อส่ง email")
                    return

                print(f"📧 กำลังแนบไฟล์: {len(pdf_files)} ไฟล์")

                # แนบไฟล์ PDF
                for pdf_file in pdf_files:
                    file_name = os.path.basename(pdf_file)
                    print(f"  📎 แนบไฟล์: {file_name}")

                    with open(pdf_file, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_name}',
                    )
                    msg.attach(part)

                # ส่ง email
                print("📧 กำลังส่ง email...")
                server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
                server.starttls()  # เปิดใช้งาน TLS
                server.login(email_config["sender_email"], email_config["sender_password"])
                text = msg.as_string()
                server.sendmail(email_config["sender_email"], email_config["recipient_email"], text)
                server.quit()

                print("✅ ส่ง email สำเร็จ!")
                print(f"📧 ส่งไปยัง: {email_config['recipient_email']}")

            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาดในการส่ง email: {e}")
                print("💡 กรุณาตรวจสอบ:")
                print("   - ข้อมูล email และ password")
                print("   - การเชื่อมต่ออินเทอร์เน็ต")
                print("   - การตั้งค่า App Password ของ Gmail")

        # เรียกใช้ฟังก์ชันเปลี่ยนชื่อและย้ายไฟล์
        rename_and_move_files()
    else:
        print("❌ หน้าผลลัพธ์ไม่โหลดสำเร็จ")

    print("ดำเนินการเสร็จสิ้น!")
    
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
    
finally:
   driver.quit()