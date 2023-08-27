import os
import re
import sqlite3

import openpyxl
import pandas as pd
import json
import logging


def create_excel_template(file_name):
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['姓名', '班级', '学号', '性别', '联系方式', '其他信息'])

        # 添加示例数据
        for row in range(2, 11):
            # 添加示例数据，row-1是为了从1开始计数
            ws.append(
                [f'学生{row - 1}姓名', f'班级{row - 1}', f'学号{row - 1}', '男', f'13800138000{row - 1}', '其他信息'])

        wb.save(file_name)
    except Exception as e:
        logging.error(f"An error occurred while creating Excel template: {e}")


# 学生信息类
class Student:
    # 初始化学生信息
    def __init__(self, name, class_name, student_id, gender, contact, other_info):
        self.name = name
        self.class_name = class_name
        self.student_id = student_id
        self.gender = gender
        self.contact = contact
        self.other_info = other_info

    # 打印学生信息
    def __str__(self):
        return f"姓名： {self.name}, 班级： {self.class_name}, 学号： {self.student_id}, 性别： {self.gender}, 联系方式： {self.contact}, 其他信息： {self.other_info}"


# 学生管理类
class StudentManager:
    def __init__(self):
        self.students = []

    # 添加学生，如果姓名或联系方式为空，则抛出异常
    def add_student(self, student):
        if not student.name or not student.contact:
            raise ValueError("姓名和联系方式不能为空")
        self.students.append(student)

    # 编辑学生，如果找不到该学生，则返回False
    def edit_student(self, name, new_info):
        student_to_edit = next((student for student in self.students if student.name == name), None)
        if student_to_edit:
            for key, value in new_info.items():
                if hasattr(student_to_edit, key):
                    setattr(student_to_edit, key, value)
            return True
        else:
            return False

    # 删除学生，如果找不到该学生，则抛出异常
    def get_students(self):
        return self.students


# 检查文件名是否合法，支持中文
def is_valid_filename(filename):
    pattern = r'^[a-zA-Z0-9_.-\u4e00-\u9fa5]+$'
    return re.match(pattern, filename)


# 检查文件名合法性
def validate_filename(file_name):
    if not file_name:
        raise ValueError("文件名不能为空")
    if not file_name.endswith('.xlsx'):
        raise ValueError("文件名必须以.xlsx结尾")
    if os.path.exists(file_name):
        raise ValueError("文件名已存在")
    if not is_valid_filename(file_name):
        raise ValueError("文件名不合法")


class StudentsInfo:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS students (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   class_name TEXT,
                   student_id TEXT,
                   gender TEXT,
                   contact TEXT,
                   other_info TEXT
               )
           ''')
        self.connection.commit()

    # 从Excel导入数据, 如果文件不存在，则抛出异常, 如果文件格式不正确，则抛出异常, 如果文件中有重复的姓名，则抛出异常; 如果文件中有空值，则抛出异常
    def import_from_excel(self, file_name):
        try:
            df = pd.read_excel(file_name)
            students_info = df.to_dict('records')
            self.students_info.extend(students_info)
            with open('StudentsInfo.json', 'w') as f:
                json.dump(self.students_info, f)
        except Exception as e:
            logging.error(f"An error occurred while importing from Excel: {e}")

    # 导出数据到Excel
    def export_to_excel(self, file_name):
        try:
            # 检查文件名合法性
            validate_filename(file_name)

            # 检查导出的数据不为空
            if not self.students_info:
                raise ValueError("导出的数据不能为空")

            df = pd.DataFrame(self.students_info)
            df.to_excel(file_name, index=False)
        except Exception as e:
            logging.error(f"An error occurred while exporting to Excel: {e}")

    # 手动添加学生信息, 如果姓名或联系方式为空，则抛出异常, 如果姓名已存在，则抛出异常
    def add_manual_student(self, student):
        try:
            if not student.name or not student.contact:
                raise ValueError("姓名和联系方式不能为空")
            if student.name in [s['姓名'] for s in self.students_info]:
                logging.warning("无法添加学生信息：姓名已存在")
                return False
            self.students_info.append(student.__dict__)
            with open('StudentsInfo.json', 'w') as f:
                json.dump(self.students_info, f)
            logging.info(f"添加了新手动学生信息：{student.__dict__}")
            return True
        except Exception as e:
            logging.error(f"添加学生信息时出现错误: {e}")
            return False

    # 编辑学生信息, 如果找不到该学生，则返回False
    def edit_student_info(self, name, new_info):
        try:
            student_to_edit = next((student for student in self.students_info if student['姓名'] == name), None)
            if student_to_edit:
                student_to_edit.update(new_info)
                logging.info(f"编辑学生信息成功：{student_to_edit}")
                return True
            else:
                logging.warning("找不到要编辑的学生信息")
                return False
        except Exception as e:
            logging.error(f"编辑学生信息时出现错误: {e}")
            return False

    def delete_student_info(self, name):
        try:
            initial_count = len(self.students_info)
            self.students_info = [student for student in self.students_info if student['姓名'] != name]
            if len(self.students_info) < initial_count:
                logging.info(f"删除学生信息成功：{name}")
                return True
            else:
                logging.warning("找不到要删除的学生信息")
                return False
        except Exception as e:
            logging.error(f"删除学生信息时出现错误: {e}")
            return False


# 设置日志配置
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建学生信息管理对象
add_students_info = StudentsInfo()

# 创建模板并导入数据
create_excel_template('template.xlsx')
add_students_info.import_from_excel('template.xlsx')

# 编辑和删除数据
add_students_info.edit_student_info('学生2姓名', {'姓名': '张三', '班级': '班1', '联系方式': '13900139000'})
add_students_info.delete_student_info('学生3姓名')

# 手动添加学生信息
manual_student = Student('手动添加学生', '手动班级', '手动学号', '男', '13999999999', '手动信息')
add_students_info.add_manual_student(manual_student)

# 导出数据
add_students_info.export_to_excel('output.xlsx')
