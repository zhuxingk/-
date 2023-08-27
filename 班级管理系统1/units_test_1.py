import unittest
from openpyxl import load_workbook
from StudentsInfo import AddStudentsInfo  # 请将your_module替换为你的模块名

class TestAddStudentsInfo(unittest.TestCase):
    def setUp(self):
        self.add_students_info = AddStudentsInfo()
        create_excel_template('template.xlsx')
        self.add_students_info.import_excel('template.xlsx')

    # 测试用例
    def test_import_excel(self):
        self.add_students_info.export_excel('output.xlsx')
        workbook = load_workbook('output.xlsx')
        sheet = workbook.active
        data = [cell.value for cell in sheet['A']]
        self.assertEqual(data, ['学生2姓名', '学号2', '男', '班级2', '13800138000', '其他信息'])  # 更新预期结果

    def test_edit_student_info(self):
        self.add_students_info.edit_student_info(0, 姓名='张三', 班级='班1', 联系方式='13900139000')
        student_info = self.add_students_info.students_info[0]
        self.assertEqual(student_info['姓名'], '张三')
        self.assertEqual(student_info['班级'], '班1')
        self.assertEqual(student_info['联系方式'], '13900139000')

    # 测试用例
    def test_delete_student_info(self):
        self.add_students_info.delete_student_info(0)
        self.assertEqual(len(self.add_students_info.students_info), 8)  # 更新预期结果

if __name__ == '__main__':
    unittest.main()
