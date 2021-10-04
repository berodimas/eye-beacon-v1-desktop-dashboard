
from ui_file.eyebeacon_gui import *

from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
import redis, struct, cv2, os, json, sys
from datetime import datetime, date
import numpy as np

# os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

r = redis.Redis(host='localhost', port=6379, db=0)

i, j = 1, 1
arr = []

people_counter = {
    'enter': 0,
    'exit': 0,
    'total': 0
}

people_status = {
    'name': '',
    'isInside': False
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.RedisClientWorker = self.RedisClientWorker()
        self.RedisClientWorker.start()
        self.RedisClientWorker.setter_counter.connect(self.people_count_report)
        self.RedisClientWorker.setter_status.connect(self.people_status_report)

        self.ui.button_page_feed.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.page_1))
        self.ui.button_page_feed.clicked.connect(
            self.state_function)
        self.ui.button_page_log.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.page_2))
        self.ui.button_page_log.clicked.connect(
            self.state_function)

        self.screen_width = QApplication.desktop().screenGeometry().width()
        self.screen_height = QApplication.desktop().screenGeometry().height()

        self.container_camera = self.ui.label_camera_stream

        timer = QTimer(self)
        timer.setInterval(int(1000/30))
        timer.timeout.connect(self.fromRedis)
        timer.start()

    def fromRedis(self):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = r.get('image')
        h, w = struct.unpack('>II',encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
        a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
        self.img = QImage(a, a.shape[1], a.shape[0],
                      QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(self.img)
        self.pix = self.pix.scaledToHeight(self.container_camera.height())
        self.container_camera.setPixmap(self.pix)

    def state_function(self):
        if self.ui.stacked_widget.currentIndex() == 0:
            self.ui.button_page_feed.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                                "border-top-left-radius: 5px;\n"
                                                "border-bottom-left-radius: 5px;\n"
                                                "font: 10pt;\n"
                                                "font-weight: bold;\n"
                                                "")
            self.ui.button_page_log.setStyleSheet("background-color: rgb(188, 188, 188);\n"
                                               "border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;\n"
                                               "font: 10pt;\n"
                                               "font-weight: regular;")
        else:
            self.ui.button_page_feed.setStyleSheet("background-color: rgb(188, 188, 188);\n"
                                                "border-top-left-radius: 5px;\n"
                                                "border-bottom-left-radius: 5px;\n"
                                                "font: 10pt;\n"
                                                "font-weight: regular;\n"
                                                "")
            self.ui.button_page_log.setStyleSheet("background-color: rgb(238, 238, 238);\n"
                                               "border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;\n"
                                               "font: 10pt;\n"
                                               "font-weight: bold;")
                   
    def people_count_report(self):
        global i

        widget_report = QWidget()
        widget_report.setStyleSheet("background-color: rgb(255, 255, 255);\nborder-radius: 5px;")
        layout_report = QGridLayout(widget_report)

        label_date = QLabel(date.today().strftime("%B %d, %Y"))
        label_time = QLabel(datetime.now().strftime("%H:%M:%S"))
        label_time.setAlignment(QtCore.Qt.AlignRight)
        label_detected = QLabel("Enter Count: {}\nExit Count: {}\nTotal Person Inside: {}".format(
            people_counter['enter'], people_counter['exit'], people_counter['total']))

        layout_report.addWidget(label_date, 0, 0, 1, 1)
        layout_report.addWidget(label_time, 0, 1, 1, 1)
        layout_report.addWidget(label_detected, 1, 0, 1, 2)

        self.ui.label_status_1.setText("Enter Count: {}".format(
            people_counter['enter']))
        self.ui.label_status_2.setText("Exit Count: {}".format(
            people_counter['exit']))
        self.ui.label_status_3.setText("Total Person Inside: {}".format(
            people_counter['total']))     

        self.layout = self.ui.report_container_layout_2
        self.layout.insertWidget(self.layout.count()-i, widget_report)

        i+=1

    def people_status_report(self):
        global j, arr

        widget_report = QWidget()
        widget_report.setStyleSheet(
            "background-color: rgb(255, 255, 255);\nborder-radius: 5px;")
        layout_report = QGridLayout(widget_report)
        self.layout = self.ui.report_container_layout
        
        if people_status['isInside']:
            if people_status['name'] not in arr:
                arr.append(people_status['name'])
                label_name = QLabel("{}".format(people_status['name']))
                label_time = QLabel(datetime.now().strftime("%H:%M:%S"))
                label_time.setAlignment(QtCore.Qt.AlignRight)
                layout_report.addWidget(label_name, 0, 0, 1, 1)
                layout_report.addWidget(label_time, 0, 1, 1, 1)
                widget_report.setObjectName("{}".format(people_status['name']))
                self.layout.insertWidget(self.layout.count()-j, widget_report)
                j+=1
        else:
            child = self.findChild(QWidget, "{}".format(people_status['name']))
            if child:
                arr.remove(people_status['name'])
                child.deleteLater()
                j -= 1

    class RedisClientWorker(QThread):
        setter_counter = pyqtSignal()
        setter_status = pyqtSignal()
        
        def __init__(self):
            super().__init__()
            self.p = r.pubsub()
            self.p.psubscribe('http_*')

        def run(self):
            for message in self.p.listen():
                if 'pmessage' != message['type']:
                    continue
                data = json.loads(message['data'].decode('utf-8'))
                if 'http_counter' == message['channel'].decode('utf-8'):
                    people_counter["enter"], people_counter["exit"], people_counter["total"] = data["enter"], data["exit"], data["total"]
                    self.setter_counter.emit()
                if 'http_status' == message['channel'].decode('utf-8'):
                    people_status["name"], people_status["isInside"] = data["name"], data["isInside"]
                    self.setter_status.emit()
                
if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec_())
