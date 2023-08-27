import logging
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices


class LoginHandler:
    def __init__(self):
        self.username = "admin"
        self.password = "123456"
        self.logger = logging.getLogger("LoginHandler")
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler("login_error.log")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def validate(self, username, password):
        try:
            return self.username == username and self.password == password
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False

    def login(self):
        if self.validate(self.username, self.password):
            print("登录成功")
            # 在新线程中执行打开新窗口的操作
            thread = QThread()
            thread.started.connect(lambda: QDesktopServices.openUrl(QUrl("http://localhost:8080/main_menu")))
            thread.start()
        else:
            print("用户名或密码错误")
