import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QMessageBox, QLineEdit


# 后端 API
class BackendAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    # 登录, 返回是否登录成功和消息, 如果成功, 则消息为"登录成功", 否则为错误消息
    def login(self, username, password):
        try:
            response = requests.post(f"{self.base_url}/login", json={"username": username, "password": password})

            if response.status_code == 200:
                data = response.json()
                return data.get("success", False), data.get("message", "登录失败")
            else:
                return False, "无法连接到服务器，请稍后再试"

        except requests.exceptions.RequestException as e:
            return False, "网络连接出错，请检查您的网络连接"

    def get_students(self):
        response = requests.get(f"{self.base_url}/students")
        return response.json()

    def get_scores(self):
        response = requests.get(f"{self.base_url}/scores")
        return response.json()


# 用户登录界面
class LoginWindow(QWidget):
    # 初始化
    def __init__(self, backend):
        super().__init__()
        self.main_window = None
        self.backend = backend
        self.setWindowTitle("用户登录")

        layout = QVBoxLayout()
        # 增加用户名和密码输入框
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # 增加登录按钮
        login_button = QPushButton("登录")
        login_button.clicked.connect(self.login)

        # 增加用户名和密码输入框
        layout.addWidget(QLabel("用户名:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("密码:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    # 登录
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        success, message = self.backend.login(username, password)

        if success:
            self.close()  # 关闭登录窗口
            self.main_window = MainWindow()  # 创建主菜单窗口实例
            self.main_window.show()  # 显示主菜单窗口
        else:
            QMessageBox.warning(self, "错误", message)


# 主菜单界面
class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("主菜单")
        # 在主菜单界面布局中添加按钮、标签等内容
        layout = QVBoxLayout()
        layout.addWidget(QLabel("欢迎进入主菜单！"))
        self.setLayout(layout)


        tab_widget = QTabWidget()
        # 增加学生信息管理菜单按钮
        student_info_tab = QWidget()
        student_info_layout = QVBoxLayout()
        student_info_button = QPushButton("获取学生信息")
        student_info_button.clicked.connect(self.get_students)
        student_info_layout.addWidget(student_info_button)
        self.student_info_label = QLabel()
        student_info_layout.addWidget(self.student_info_label)
        student_info_tab.setLayout(student_info_layout)
        tab_widget.addTab(student_info_tab, "学生信息管理")

        # 增加学生成绩管理菜单按钮
        score_management_tab = QWidget()
        score_management_layout = QVBoxLayout()
        score_management_button = QPushButton("获取学生成绩")
        score_management_button.clicked.connect(self.get_scores)
        score_management_layout.addWidget(score_management_button)
        self.score_management_label = QLabel()
        score_management_layout.addWidget(self.score_management_label)
        score_management_tab.setLayout(score_management_layout)
        tab_widget.addTab(score_management_tab, "学生成绩管理")

        # 增加学生表现记录菜单按钮
        student_performance_tab = QWidget()
        student_performance_layout = QVBoxLayout()
        student_performance_button = QPushButton("获取学生表现记录")
        student_performance_button.clicked.connect(self.get_student_performance)
        student_performance_layout.addWidget(student_performance_button)
        self.student_performance_label = QLabel()
        student_performance_layout.addWidget(self.student_performance_label)
        student_performance_tab.setLayout(student_performance_layout)
        tab_widget.addTab(student_performance_tab, "学生表现记录")

        # 增加工作安排菜单按钮
        work_arrangement_tab = QWidget()
        work_arrangement_layout = QVBoxLayout()
        work_arrangement_button = QPushButton("获取工作安排")
        work_arrangement_button.clicked.connect(self.get_work_arrangement)
        work_arrangement_layout.addWidget(work_arrangement_button)
        self.work_arrangement_label = QLabel()
        work_arrangement_layout.addWidget(self.work_arrangement_label)
        work_arrangement_tab.setLayout(work_arrangement_layout)
        tab_widget.addTab(work_arrangement_tab, "工作安排")

        # 增加学生考勤记录菜单按钮
        student_attendance_tab = QWidget()
        student_attendance_layout = QVBoxLayout()
        student_attendance_button = QPushButton("获取学生考勤记录")
        student_attendance_button.clicked.connect(self.get_student_attendance)
        student_attendance_layout.addWidget(student_attendance_button)
        self.student_attendance_label = QLabel()
        student_attendance_layout.addWidget(self.student_attendance_label)
        student_attendance_tab.setLayout(student_attendance_layout)
        tab_widget.addTab(student_attendance_tab, "学生考勤记录")

        # 增加个人备忘录菜单按钮
        personal_memo_tab = QWidget()
        personal_memo_layout = QVBoxLayout()
        personal_memo_button = QPushButton("获取个人备忘录")
        personal_memo_button.clicked.connect(self.get_personal_memo)
        personal_memo_layout.addWidget(personal_memo_button)
        self.personal_memo_label = QLabel()
        personal_memo_layout.addWidget(self.personal_memo_label)
        personal_memo_tab.setLayout(personal_memo_layout)
        tab_widget.addTab(personal_memo_tab, "个人备忘录")

        self.setCentralWidget(tab_widget)

    # 获取学生信息
    def get_students(self):
        students = self.backend.get_students()
        self.student_info_label.setText(str(students))

    # 获取学生成绩
    def get_scores(self):
        scores = self.backend.get_scores()
        self.score_management_label.setText(str(scores))

    # 获取学生表现记录
    def get_student_performance(self):
        student_performance = self.backend.get_student_performance()
        self.student_performance_label.setText(str(student_performance))

    # 获取工作安排
    def get_work_arrangement(self):
        work_arrangement = self.backend.get_work_arrangement()
        self.work_arrangement_label.setText(str(work_arrangement))

    # 获取学生考勤记录
    def get_student_attendance(self):
        student_attendance = self.backend.get_student_attendance()
        self.student_attendance_label.setText(str(student_attendance))

    # 获取个人备忘录
    def get_personal_memo(self):
        personal_memo = self.backend.get_personal_memo()
        self.personal_memo_label.setText(str(personal_memo))


def main():
    app = QApplication(sys.argv)
    base_url = "http://your-backend-api-url"  # Replace with your actual API base URL
    backend = BackendAPI(base_url)

    main_window = MainWindow(backend)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
