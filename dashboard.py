
from ui_file.eyebeacon_gui import *

from PyQt5.QtWidgets import QGridLayout, QLayout, QMainWindow, QWidget
from flask import Flask, jsonify, abort, request
from flask_restful import Api, abort
import redis, struct, cv2, os
import numpy as np

# os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

app = Flask(__name__)
api = Api(app)

from datetime import datetime, date
import sys

i = 1
j = 1
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

        self.WebClientWorker = self.WebClientWorker()
        self.WebClientWorker.start()

        self.PeopleCounterRequest = self.PeopleCounterRequest()
        self.PeopleCounterRequest.setter.connect(self.people_count_report)

        self.PeopleStatusRequest = self.PeopleStatusRequest()
        self.PeopleStatusRequest.setter.connect(self.people_status_report)


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
        self.r = redis.Redis(host='localhost', port=6379, db=0)

        timer = QTimer(self)
        timer.setInterval(int(1000/30))
        timer.timeout.connect(self.fromRedis)
        timer.start()

    def fromRedis(self):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = self.r.get('image')
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
        now = datetime.now()
        today = date.today()

        current_time = now.strftime("%H:%M:%S")
        current_date = today.strftime("%B %d, %Y")

        widget_report = QWidget()
        widget_report.setStyleSheet("background-color: rgb(255, 255, 255);\nborder-radius: 5px;")
        layout_report = QGridLayout(widget_report)

        label_date = QLabel(current_date)
        label_time = QLabel(current_time)
        label_time.setAlignment(QtCore.Qt.AlignRight)
        label_detected = QLabel("Enter Count: {}\nExit Count: {}\nTotal Person Inside: {}".format(
            people_counter['enter'], people_counter['exit'], people_counter['total']))

        layout_report.addWidget(label_date, 0, 0, 1, 1)
        layout_report.addWidget(label_time, 0, 1, 1, 1)
        layout_report.addWidget(label_detected, 1, 0, 1, 2)

        self.layout = self.ui.report_container_layout_2
        self.layout.insertWidget(self.layout.count()-i, widget_report)

        self.ui.label_status_1.setText("Enter Count: {}".format(
            people_counter['enter']))
        self.ui.label_status_2.setText("Exit Count: {}".format(
            people_counter['exit']))
        self.ui.label_status_3.setText("Total Person Inside: {}".format(
            people_counter['total']))        
        i+=1

    def people_status_report(self):
        global j
        global arr
        user_name = people_status['name']
        isInside = people_status['isInside']


        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        widget_report = QWidget()
        widget_report.setStyleSheet(
            "background-color: rgb(255, 255, 255);\nborder-radius: 5px;")
        layout_report = QGridLayout(widget_report)
        self.layout = self.ui.report_container_layout
        
        if isInside:
            if user_name not in arr:
                arr.append(user_name)
                label_name = QLabel("{}".format(user_name))
                label_time = QLabel(current_time)
                label_time.setAlignment(QtCore.Qt.AlignRight)
                layout_report.addWidget(label_name, 0, 0, 1, 1)
                layout_report.addWidget(label_time, 0, 1, 1, 1)
                widget_report.setObjectName("{}".format(user_name))
                self.layout.insertWidget(self.layout.count()-j, widget_report)
                j+=1
        else:
            child = self.findChild(QWidget, "{}".format(user_name))
            if child:
                arr.remove(user_name)
                child.deleteLater()
                j -= 1
        
    class PeopleCounterRequest(QObject):
        setter = pyqtSignal()

    class PeopleStatusRequest(QObject):
        setter = pyqtSignal()

    class WebClient:
        @app.route("/", methods=['GET'])
        def home():
            return "Hello World"
            
        @app.route("/eyebeacon/dashboard/people_counter", methods=['POST'])
        def post():
            mainWindow.PeopleCounterRequest.setter.emit()
            if len(people_counter) == 0:
                abort(404)
            if not request.json:
                abort(400)
            if 'enter' in request.json and type(request.json['enter']) is not int:
                abort(400)
            if 'exit' in request.json and type(request.json['exit']) is not int:
                abort(400)
            if 'total' in request.json and type(request.json['total']) is not int:
                abort(400)
            people_counter['enter'] = request.json.get(
                'enter', people_counter['enter'])
            people_counter['exit'] = request.json.get(
                'exit', people_counter['exit'])
            people_counter['total'] = request.json.get(
                'total', people_counter['total'])
            return jsonify({'people_counter': people_counter})
        
        @app.route("/eyebeacon/dashboard/people_status", methods=['GET'])
        def get():
            mainWindow.PeopleStatusRequest.setter.emit()
            if len(people_status) == 0:
                abort(404)
            if not request.json:
                abort(400)
            if 'name' in request.json and type(request.json['name']) is not str:
                abort(400)
            if 'isInside' in request.json and type(request.json['isInside']) is not bool:
                abort(400)
            people_status['name'] = request.json.get(
                'name', people_status['name'])
            people_status['isInside'] = request.json.get(
                'isInside', people_status['isInside'])
            return jsonify({'people_status': people_status})

    class WebClientWorker(QThread):
        def run(self):
            app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(application.exec_())
