import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class DataAnalyzer:
    """คลาสสำหรับการวิเคราะห์ข้อมูล"""

    def __init__(self, file_path):
        """
        เริ่มต้น DataAnalyzer

        Args:
            file_path (str): path ของไฟล์ข้อมูล (CSV หรือ Excel)
        """
        self.file_path = file_path
        self.df = None
        self.load_data()

    def load_data(self):
        """โหลดข้อมูลจากไฟล์"""
        file_extension = Path(self.file_path).suffix.lower()

        try:
            if file_extension == '.csv':
                self.df = pd.read_csv(self.file_path)
            elif file_extension in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.file_path)
            else:
                raise ValueError(f"รองรับเฉพาะไฟล์ .csv, .xlsx, .xls เท่านั้น")

            if self.df.empty:
                print("คำเตือน: ไฟล์ไม่มีข้อมูล (0 แถว)")
            else:
                print(f"โหลดข้อมูลสำเร็จ: {len(self.df)} แถว, {len(self.df.columns)} คอลัมน์")
        except FileNotFoundError:
            print(f"เกิดข้อผิดพลาด: ไม่พบไฟล์ '{self.file_path}'")
            self.df = None
        except pd.errors.EmptyDataError:
            print("เกิดข้อผิดพลาด: ไฟล์ว่างเปล่า")
            self.df = None
        except pd.errors.ParserError as e:
            print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
            self.df = None
        except ValueError as e:
            print(f"เกิดข้อผิดพลาด: {e}")
            self.df = None
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
            self.df = None

    def _validate_data(self):
        """ตรวจสอบว่าข้อมูลถูกโหลดและพร้อมใช้งาน"""
        if self.df is None:
            print("ข้อผิดพลาด: ไม่มีข้อมูล กรุณาโหลดไฟล์ที่ถูกต้อง")
            return False
        if self.df.empty:
            print("ข้อผิดพลาด: DataFrame ว่างเปล่า")
            return False
        return True

    def basic_info(self):
        """แสดงข้อมูลพื้นฐานของ dataset"""
        if not self._validate_data():
            return

        print("\n=== ข้อมูลพื้นฐาน ===")
        print(f"จำนวนแถว: {len(self.df)}")
        print(f"จำนวนคอลัมน์: {len(self.df.columns)}")
        print(f"\nชื่อคอลัมน์: {list(self.df.columns)}")

        print("\n=== ชนิดข้อมูล ===")
        print(self.df.dtypes)

        print("\n=== ข้อมูลที่หายไป ===")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("ไม่มีข้อมูลที่หายไป")

    def statistical_summary(self):
        """แสดงสถิติเชิงพรรณนา"""
        if not self._validate_data():
            return

        print("\n=== สถิติเชิงพรรณนา ===")
        print(self.df.describe())

    def show_head(self, n=5):
        """แสดงข้อมูล n แถวแรก"""
        if not self._validate_data():
            return

        print(f"\n=== {n} แถวแรก ===")
        print(self.df.head(n))

    def show_tail(self, n=5):
        """แสดงข้อมูล n แถวท้าย"""
        if not self._validate_data():
            return

        print(f"\n=== {n} แถวท้าย ===")
        print(self.df.tail(n))

    def correlation_matrix(self, save_path=None):
        """
        สร้าง correlation matrix สำหรับข้อมูลตัวเลข

        Args:
            save_path (str, optional): path สำหรับบันทึกรูปภาพ
        """
        if not self._validate_data():
            return

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            print("ต้องมีคอลัมน์ตัวเลขอย่างน้อย 2 คอลัมน์เพื่อสร้าง correlation matrix")
            return

        try:
            plt.figure(figsize=(10, 8))
            sns.heatmap(self.df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Matrix')
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path)
                print(f"บันทึก correlation matrix ที่: {save_path}")
            else:
                plt.show()
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้าง correlation matrix: {e}")
        finally:
            plt.close()

    def plot_distribution(self, column, save_path=None):
        """
        สร้างกราฟแสดงการกระจายของข้อมูล

        Args:
            column (str): ชื่อคอลัมน์
            save_path (str, optional): path สำหรับบันทึกรูปภาพ
        """
        if not self._validate_data():
            return

        if column not in self.df.columns:
            print(f"ไม่พบคอลัมน์ '{column}'")
            return

        try:
            plt.figure(figsize=(10, 6))

            if pd.api.types.is_numeric_dtype(self.df[column]):
                data = self.df[column].dropna()

                if len(data) == 0:
                    print(f"คอลัมน์ '{column}' ไม่มีข้อมูล (ทั้งหมดเป็น NaN)")
                    return

                plt.subplot(1, 2, 1)
                plt.hist(data, bins=30, edgecolor='black')
                plt.title(f'Histogram: {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')

                plt.subplot(1, 2, 2)
                plt.boxplot(data)
                plt.title(f'Box Plot: {column}')
                plt.ylabel(column)
            else:
                value_counts = self.df[column].value_counts()
                if len(value_counts) == 0:
                    print(f"คอลัมน์ '{column}' ไม่มีข้อมูล")
                    return

                plt.bar(range(len(value_counts)), value_counts.values)
                plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
                plt.title(f'Value Counts: {column}')
                plt.xlabel(column)
                plt.ylabel('Count')

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                print(f"บันทึกกราฟที่: {save_path}")
            else:
                plt.show()
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสร้างกราฟ: {e}")
        finally:
            plt.close()

    def export_summary(self, output_path='data_summary.txt'):
        """
        ส่งออกสรุปข้อมูลเป็นไฟล์ text

        Args:
            output_path (str): path สำหรับบันทึกไฟล์
        """
        if not self._validate_data():
            return

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("Data Analysis Summary\n")
                f.write("Author: Vinner\n")
                f.write("=" * 50 + "\n\n")

                f.write(f"File: {self.file_path}\n")
                f.write(f"Rows: {len(self.df)}\n")
                f.write(f"Columns: {len(self.df.columns)}\n\n")

                f.write("Column Names:\n")
                for col in self.df.columns:
                    f.write(f"  - {col} ({self.df[col].dtype})\n")

                f.write("\n" + "=" * 50 + "\n")
                f.write("Statistical Summary:\n")
                f.write("=" * 50 + "\n")
                f.write(str(self.df.describe()))

                f.write("\n\n" + "=" * 50 + "\n")
                f.write("Missing Values:\n")
                f.write("=" * 50 + "\n")
                missing = self.df.isnull().sum()
                if missing.sum() > 0:
                    f.write(str(missing[missing > 0]))
                else:
                    f.write("No missing values\n")

            print(f"บันทึกสรุปข้อมูลที่: {output_path}")
        except IOError as e:
            print(f"เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")


def main():
    """ฟังก์ชันหลักสำหรับการทดสอบ"""
    print("Data Analyzer Tool")
    print("Author: Vinner")
    print("-" * 50)

    # ตัวอย่างการใช้งาน
    file_path = input("กรุณาใส่ path ของไฟล์ข้อมูล (CSV หรือ Excel): ")

    try:
        analyzer = DataAnalyzer(file_path)

        # ตรวจสอบว่าโหลดข้อมูลสำเร็จหรือไม่
        if analyzer.df is None:
            print("\nไม่สามารถโหลดข้อมูลได้ โปรแกรมจะหยุดทำงาน")
            return

        while True:
            print("\n" + "=" * 50)
            print("เมนูการวิเคราะห์")
            print("=" * 50)
            print("1. แสดงข้อมูลพื้นฐาน")
            print("2. แสดงสถิติเชิงพรรณนา")
            print("3. แสดง 5 แถวแรก")
            print("4. แสดง 5 แถวท้าย")
            print("5. สร้าง Correlation Matrix")
            print("6. สร้างกราฟแสดงการกระจาย")
            print("7. ส่งออกสรุปข้อมูล")
            print("0. ออกจากโปรแกรม")

            choice = input("\nเลือกเมนู (0-7): ")

            if choice == '1':
                analyzer.basic_info()
            elif choice == '2':
                analyzer.statistical_summary()
            elif choice == '3':
                analyzer.show_head()
            elif choice == '4':
                analyzer.show_tail()
            elif choice == '5':
                save = input("ต้องการบันทึกรูปภาพหรือไม่? (y/n): ")
                if save.lower() == 'y':
                    path = input("ใส่ path สำหรับบันทึก (เช่น correlation.png): ")
                    analyzer.correlation_matrix(save_path=path)
                else:
                    analyzer.correlation_matrix()
            elif choice == '6':
                print("\nคอลัมน์ที่มี:", list(analyzer.df.columns))
                col = input("ใส่ชื่อคอลัมน์ที่ต้องการวิเคราะห์: ")
                save = input("ต้องการบันทึกรูปภาพหรือไม่? (y/n): ")
                if save.lower() == 'y':
                    path = input("ใส่ path สำหรับบันทึก (เช่น distribution.png): ")
                    analyzer.plot_distribution(col, save_path=path)
                else:
                    analyzer.plot_distribution(col)
            elif choice == '7':
                path = input("ใส่ path สำหรับบันทึกสรุป (กด Enter เพื่อใช้ชื่อ data_summary.txt): ")
                if not path:
                    path = 'data_summary.txt'
                analyzer.export_summary(path)
            elif choice == '0':
                print("ขอบคุณที่ใช้งาน!")
                break
            else:
                print("เลือกเมนูไม่ถูกต้อง กรุณาลองใหม่")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
    main()
