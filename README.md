# Data Analyzer Tool

**ผู้พัฒนา:** Vinner

เครื่องมือสำหรับการวิเคราะห์ข้อมูลด้วย Python ที่รองรับไฟล์ CSV และ Excel พร้อมฟังก์ชันการวิเคราะห์ข้อมูลเชิงสถิติและการแสดงผลกราฟ

## ฟีเจอร์

- โหลดและอ่านไฟล์ CSV และ Excel (xlsx, xls)
- แสดงข้อมูลพื้นฐาน (จำนวนแถว, คอลัมน์, ชนิดข้อมูล)
- แสดงสถิติ (ค่าเฉลี่ย, ค่ามัธยฐาน, ค่าเบี่ยงเบนมาตรฐาน ฯลฯ)
- ตรวจสอบข้อมูลที่หายไป (Missing Values)
- สร้าง Correlation Matrix แสดงความสัมพันธ์ระหว่างตัวแปร
- สร้างกราฟแสดงการกระจายของข้อมูล (Histogram, Box Plot, Bar Chart)
- ส่งออกสรุปข้อมูลเป็นไฟล์ text

## ความต้องการของระบบ

- Python 3.8 หรือสูงกว่า
- pip (Python package installer)

## การติดตั้ง

### 1. ติดตั้ง Python

ตรวจสอบว่ามี Python ติดตั้งอยู่แล้วหรือไม่:

```bash
python --version
```

หรือ

```bash
python3 --version
```

หากยังไม่มี Python สามารถดาวน์โหลดได้ที่: https://www.python.org/downloads/

### 2. ติดตั้ง Dependencies

ใช้คำสั่งต่อไปนี้เพื่อติดตั้ง libraries ที่จำเป็น:

```bash
pip install -r requirements.txt
```

หรือติดตั้งแบบแยกแต่ละตัว:

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 3. ยืนยันการติดตั้ง

ตรวจสอบว่า libraries ติดตั้งเรียบร้อยแล้ว:

```bash
pip list
```

## การใช้งาน

### วิธีที่ 1: ใช้งานผ่าน Interactive Mode

เรียกใช้โปรแกรมโดยตรง:

```bash
python dataanalyzed.py
```

หรือ

```bash
python3 dataanalyzed.py
```

โปรแกรมจะถามหา path ของไฟล์ข้อมูล จากนั้นแสดงเมนูให้เลือกฟังก์ชันที่ต้องการใช้งาน

**ตัวอย่างการใช้งาน:**

```
กรุณาใส่ path ของไฟล์ข้อมูล (CSV หรือ Excel): data.csv

==================================================
เมนูการวิเคราะห์
==================================================
1. แสดงข้อมูลพื้นฐาน
2. แสดงสถิติเชิงพรรณนา
3. แสดง 5 แถวแรก
4. แสดง 5 แถวท้าย
5. สร้าง Correlation Matrix
6. สร้างกราฟแสดงการกระจาย
7. ส่งออกสรุปข้อมูล
0. ออกจากโปรแกรม

เลือกเมนู (0-7):
```

### วิธีที่ 2: ใช้งานผ่าน Python Script

สร้างไฟล์ Python ใหม่และ import DataAnalyzer class:

```python
from dataanalyzed import DataAnalyzer

# โหลดข้อมูล
analyzer = DataAnalyzer('your_data.csv')

# แสดงข้อมูลพื้นฐาน
analyzer.basic_info()

# แสดงสถิติเชิงพรรณนา
analyzer.statistical_summary()

# แสดง 5 แถวแรก
analyzer.show_head()

# สร้าง Correlation Matrix และบันทึกเป็นรูปภาพ
analyzer.correlation_matrix(save_path='correlation.png')

# สร้างกราฟแสดงการกระจายของคอลัมน์
analyzer.plot_distribution('column_name', save_path='distribution.png')

# ส่งออกสรุปข้อมูล
analyzer.export_summary('summary.txt')
```

## ตัวอย่างข้อมูล

หากต้องการทดสอบ สามารถสร้างไฟล์ CSV ตัวอย่าง:

```python
import pandas as pd
import numpy as np

# สร้างข้อมูลตัวอย่าง
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda', 'James'],
    'Age': [28, 24, 35, 32, 40],
    'Salary': [50000, 60000, 75000, 65000, 80000],
    'Department': ['IT', 'HR', 'Finance', 'IT', 'Finance']
}

df = pd.DataFrame(data)
df.to_csv('sample_data.csv', index=False)
```

จากนั้นเรียกใช้:

```bash
python dataanalyzed.py
```

และใส่ path: `sample_data.csv`

## ไฟล์ที่สร้างจากโปรแกรม

- **correlation.png**: กราฟ Correlation Matrix (ถ้าเลือกบันทึก)
- **distribution.png**: กราฟแสดงการกระจายของข้อมูล (ถ้าเลือกบันทึก)
- **data_summary.txt**: ไฟล์สรุปข้อมูลเชิงสถิติ

## การแก้ปัญหา

### ปัญหา: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'pandas'
```

**วิธีแก้:** ติดตั้ง dependencies ด้วยคำสั่ง:

```bash
pip install -r requirements.txt
```

### ปัญหา: ไม่สามารถเปิดไฟล์ Excel ได้

```
ValueError: รองรับเฉพาะไฟล์ .csv, .xlsx, .xls เท่านั้น
```

**วิธีแก้:** ตรวจสอบว่าไฟล์มีนามสกุลที่ถูกต้อง และติดตั้ง openpyxl:

```bash
pip install openpyxl
```

### ปัญหา: กราฟไม่แสดงผล

```bash
# สำหรับ macOS
brew install python-tk

# สำหรับ Ubuntu/Debian
sudo apt-get install python3-tk

# สำหรับ Windows
# ติดตั้ง Python ใหม่และเลือก tcl/tk ในตอนติดตั้ง
```

## ข้อมูลเพิ่มเติม

- Documentation: รายละเอียดฟังก์ชันอยู่ใน docstrings ของแต่ละ method
- Issues: หากพบปัญหาหรือต้องการเสนอแนะ สามารถติดต่อผู้พัฒนาได้

## License

Free to use for educational and personal projects.

---

**Developed by Vinner**
Version 1.0
Last Updated: 2025
