import os
import sys
import json     # for reading cluster configuration files
import csv
import datetime
import logging

import serial
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from WebCrawler import crawler
from Handler.Zigbee.constants import *
from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from Handler.Zigbee.structures import get_all_clusters, update_cluster_table,\
                Cluster, Cmd, Attr, TaskCmd, CLUSTER_TABLE, CLUSTER_FILE_TABLE

from CommandGenerator.command_generator import CmdGenerator

ui_file = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'ui', 'new_main.ui'))

main_class = uic.loadUiType(ui_file)[0]

# for debugging
GUIlogger = logging.getLogger("GUI")
logging.basicConfig(level=logging.DEBUG)

def get_enable_ports():
    if sys.platform.startswith('win'):   
        ports = ['COM%s' % (i + 1) for i in range(256)]   
    else:   
        raise EnvironmentError('Unsupported platform')   

    result = []   
    for port in ports:   
        try:   
            s = serial.Serial(port)
            s.close()   
            result.append(port)   
        except:   
            pass   
    return result

# groupBox_cmd_gen 에다가 cluster를 만들어서 추가하면 될 듯
def get_cluster_boxes():
    """
    Returns cluster GUI
    """
    cluster_box_list = []
    y = 0
    iter_y = 310
    for cluster_key in CLUSTER_TABLE:
        cluster_box = QGroupBox(cluster_key)
        cluster_layout = QVBoxLayout()
        cluster_box.x = 20
        cluster_box.y = y
        y += iter_y
        cluster_box.width = 371
        cluster_box.height = 221
        # 대충 위치 높이 이런거 설정하고
        # x = 20
        # y를 얼마만큼 증가시켜야 하는가?
        # width=371
        # height=221
        # cluster_box.setLayout()
        cluster_box_list.append(cluster_box)
    return cluster_box_list


class WindowClass(QMainWindow, main_class):
    def __init__(self, isOnline=False):
        super().__init__()
        self.setupUi(self)
        self.crawler = crawler.Crawler(isOnline)
    
        self.set_enable_ports()
        self.pushButton_zigbee_webcrwal.clicked.connect(self.func_btn_zigbee_crwaler)
        # TODO: add automatic routine for adding cluster comboBox
        # cluster_box_list = get_cluster_boxes()
        # for cluster_box in cluster_box_list:
        #     self.groupBox_cmd_gen.addWidget(cluster_box)
        self.comboBox_level_commands.currentIndexChanged.connect(self.func_level_interface)
        self.comboBox_color_commands.currentIndexChanged.connect(self.func_color_interface)

        self.pushButton_edit_cluster.clicked.connect(self.func_btn_edit_cluster)
        self.pushButton_edit_cmd.clicked.connect(self.func_btn_edit_cmd)
        self.pushButton_launch_chrome.clicked.connect(self.func_btn_launch_chrome)  
        self.pushButton_cmd_gen.clicked.connect(self.func_btn_command_generator)
        self.pushButton_save_cmd.clicked.connect(self.func_btn_save_command)
        self.pushButton_load_cmd.clicked.connect(self.func_btn_load_command)
        self.pushButton_start.clicked.connect(self.func_btn_start)
        self.pushButton_result_save.clicked.connect(self.func_btn_result_save)
        self.pushButton_summary.clicked.connect(self.func_btn_summary)
        self.pushButton_reset.clicked.connect(self.func_btn_reset)
        self.pushButton_zigbee_dongle_connect.clicked.connect(self.func_btn_zigbee_dongle_connect)
        self.pushButton_zigbee_dongle_disconnect.clicked.connect(self.func_btn_zigbee_dongle_disconnect)
        
        self.pushButton_zigbee_dongle_connect.setEnabled(False)
        self.pushButton_zigbee_dongle_disconnect.setEnabled(False)
        self.pushButton_zigbee_webcrwal.setEnabled(False)
        self.list_gen_cmd.itemDoubleClicked.connect(self.func_cmd_list_double_clicked)
        self.init_commands()
        self.cmd_generator = CmdGenerator()


    def init_commands(self):
        # TODO: automatically initialize cluster commands
        try:
            # init level commands
            level_commands = list(commands['LVL_CTRL_CLUSTER'].keys())
            for command in level_commands:
                self.comboBox_level_commands.addItem(command)

            color_commands = list(commands['COLOR_CTRL_CLUSTER'].keys())
            for command in color_commands:
                self.comboBox_color_commands.addItem(command)

            self.groupBox_cmd_gen.setEnabled(False) # disable all commands

        except:
            pass
    
    def set_cmd_gen_enable(self, isEnable=False):
        self.groupBox_cmd_gen.setEnabled(isEnable)

    def set_enable_ports(self):
        enabled_ports = get_enable_ports()

        for port in enabled_ports:
            self.comboBox_port.addItem(port)

    def func_btn_launch_chrome(self):
        self.crawler.login()
        self.pushButton_zigbee_webcrwal.setEnabled(True)

    def func_btn_zigbee_dongle_disconnect(self):
        port = self.comboBox_port.currentText()
        channel = int(self.lineEdit_zigbee_channel.text())
        zigbee_id = int(self.comboBox_zigbee_ids.currentText().split(':')[1], 16)
        driver = ZigBeeDriver(port, channel, zigbee_id)
        
        isConnected = True
        while isConnected:
            short_addr = driver.disconnect()
            if short_addr < 0:
                isConnected = False
                print(short_addr)
                break
            time.sleep(1)
        
        self.set_cmd_gen_enable(False)
        del driver
        
    def func_btn_zigbee_dongle_connect(self):
        port = self.comboBox_port.currentText()
        channel = int(self.lineEdit_zigbee_channel.text())
        zigbee_id = int(self.comboBox_zigbee_ids.currentText().split(':')[1], 16)
        driver = ZigBeeDriver(port, channel, zigbee_id)
        
        isConnected = False
        while not isConnected:
            short_addr = driver.connect()
            if short_addr > 0:
                isConnected = True
                print(short_addr)
                break
            time.sleep(1)
        
        self.set_cmd_gen_enable(True)
        self.pushButton_zigbee_dongle_disconnect.setEnabled(True)

        del driver

    def func_btn_edit_cluster(self):
        protocol_type = self.protocols.currentIndex()
        if protocol_type == 0:
            EditClusterWindow(self)

    def func_btn_edit_cmd(self):
        protocol_type = self.protocols.currentIndex()
        EditCmdWindow(self, type=protocol_type)

    def func_btn_command_generator(self):
        # FIXING
        # commands will be a list of TaskCmd objects
        # TODO: append commands from cluster_table
        commands = []
        
        # try:
        # on/off
        for i in range(self.spinBox_count_onoff.value()):
            cmds = self.cmd_generator.cmd_onoff(on=self.radioButton_on.isChecked(), off=self.radioButton_off.isChecked(), toggle=self.radioButton_toggle.isChecked())
            commands.append(cmds)

        # level
        for i in range(self.spinBox_count_level.value()):
            cmds = self.cmd_generator.cmd_level_interface(self.comboBox_level_commands.currentText(), self.vlayout_level_widget.children())
            commands.append(cmds)

        # color
        for i in range(self.spinBox_count_color.value()):
            cmds = self.cmd_generator.cmd_color_interface(self.comboBox_color_commands.currentText(), self.vlayout_color_widget.children())
            commands.append(cmds)

        
        # show commands 
        for i in range(self.spinBox_iter_entire.value()):
            for command in commands:
                self.list_gen_cmd.addItem(json.dumps(command))


    def func_btn_save_command(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save file', '', 'JSON (*.json)')

        commands = []
        for i in range(self.list_gen_cmd.count()):
            commands.append(self.list_gen_cmd.item(i).text())
        json_format = {'commands': commands}

        if file_name[0]:
            with open(file_name[0], 'w') as f:
                try:
                    f.write(json.dumps(json_format, indent=4))
                    QMessageBox.about(
                        self, "message", file_name[0] + " 파일이 생성되었습니다. ")

                except Exception:
                    QMessageBox.about(self, "message", Exception)
            
    def func_btn_load_command(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON (*.json)')
        try:
            if file_name[0]:
                json_data = None
                with open(file_name[0]) as json_file:
                    json_data = json.load(json_file)

                commands = json_data['commands']
                for command in commands:
                    self.list_gen_cmd.addItem(command)
        
        except Exception:
                    QMessageBox.about(self, "message", "명령어 모음 파일을 확인해")

    def func_cmd_list_double_clicked(self):
        self.list_gen_cmd.takeItem(self.list_gen_cmd.currentRow())

    def func_btn_zigbee_crwaler(self):
        # try:
        channel, zigbee_ids = self.crawler.crawl()
        self.lineEdit_zigbee_channel.setText(channel)
        for zigbee_id in zigbee_ids:
            self.comboBox_zigbee_ids.addItem(zigbee_id) # this should be changed as combobox later
        # self.set_cmd_gen_enable()
        self.pushButton_zigbee_dongle_connect.setEnabled(True)
        # except:
        #    pass # put error messages here

    # flexible layout function
    def func_overall_interface(self):
        # @hipiphock
        # TODO: think of commands such as STOP.
        # first, get cluster key.
        cluster_key = "tempkey"
        # then, get command key.
        command_key = "tempkey"
        # Cluster will be the 
        cluster = CLUSTER_TABLE[cluster_key]
        hlayout = []
        for attr_key in cluster.cmd_table[command_key].affected_attrs:
            attr_desc = cluster.attr_table[attr_key].desc
            attr_type = cluster.attr_table[attr_key].type
            temp_layout = QHBoxLayout()
            temp_label = QLabel(attr_desc)
            # get appropriate input box according to attr_type
            input_layout = None
            if attr_type == 0x20:
                input_layout = QSpinBox()
            elif attr_type == 0x30:
                pass
            # for random value
            hlayout_random = self.func_layout_random()
            hlayout.append(hlayout_random)
        for element in hlayout:
            self.vlayout_level_widget.addLayout(element) 


    def func_level_interface(self):
        try:
            current_cmd = self.comboBox_level_commands.currentText()
            self.clear_layout(self.vlayout_level_widget)                                

            if commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_MV_TO_LVL_CMD or commands['LEVEL'][current_cmd] == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
                hlayout_brightness = QHBoxLayout()
                label_brightness = QLabel("밝기")
                spinbox_brightness = QSpinBox(objectName='spinbox_brightness')
                spinbox_brightness.setMaximum(254) # 254 should be changed as constants.maxvalue
                hlayout_brightness.addWidget(label_brightness)
                hlayout_brightness.addWidget(spinbox_brightness)
                
                hlayout_random = self.func_layout_random()
                hlayout_transition, hlayout_wait = self.func_layout_transition_time()

                self.put_layout(self.vlayout_level_widget, hlayout_brightness, hlayout_random, hlayout_transition, hlayout_wait)
                
            elif commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_MOVE_CMD or commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_MOVE_ONOFF_CMD:
                hlayout_minmax = QHBoxLayout()
                label_minmax = QLabel("최대/최소")
                combobox_minmax = QComboBox()
                combobox_minmax.addItem("최대")
                combobox_minmax.addItem("최소")
                hlayout_minmax.addWidget(label_minmax)
                hlayout_minmax.addWidget(combobox_minmax)

                self.put_layout(self.vlayout_level_widget, hlayout_minmax)

            elif commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_STEP_CMD or commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_STEP_ONOFF_CMD:
                pass

            elif commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_STOP_CMD or commands['LVL_CTRL_CLUSTER'][current_cmd] == LVL_CTRL_STOP_ONOFF_CMD:
                self.clear_layout(self.vlayout_level_widget)


        except Exception:
           print(Exception) # put error messages here
    
    def func_layout_random(self):
        hlayout_random = QHBoxLayout()
        label_random = QLabel("임의값")
        checkbox_normal = QCheckBox("정상 범위", objectName="checkbox_normal")
        checkbox_abnormal = QCheckBox("비정상 범위", objectName="checkbox_abnormal")
        hlayout_random.addWidget(label_random)
        hlayout_random.addWidget(checkbox_normal)        
        hlayout_random.addWidget(checkbox_abnormal)

        return hlayout_random
  
    def func_color_interface(self):
        try:
            current_cmd = self.comboBox_color_commands.currentText()
            self.clear_layout(self.vlayout_color_widget)

            if commands['COLOR_CTRL_CLUSTER'][current_cmd] == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                hlayout_mired = QHBoxLayout()
                label_mired = QLabel("온도(Mired)")
                spinbox_mired = QSpinBox(objectName="spinbox_mired")
                spinbox_mired.setMinimum(200)
                spinbox_mired.setMaximum(370)

                hlayout_mired.addWidget(label_mired)
                hlayout_mired.addWidget(spinbox_mired)

                hlayout_random = self.func_layout_random()
                hlayout_transtition, hlayout_wait = self.func_layout_transition_time()

                self.put_layout(self.vlayout_color_widget, hlayout_mired, hlayout_random, hlayout_transtition, hlayout_wait)
            
            elif commands['COLOR_CTRL_CLUSTER'][current_cmd] == COLOR_CTRL_MV_TO_COLOR_CMD:
                hlayout_color_x = QHBoxLayout()
                label_color_x = QLabel("Color X (hex)")
                lineEdit_color_x = QLineEdit(objectName="lineEdit_color_x")
                hlayout_color_x.addWidget(label_color_x)
                hlayout_color_x.addWidget(lineEdit_color_x)

                hlayout_color_y = QHBoxLayout()
                label_color_y = QLabel("Color Y (hex)")
                lineEdit_color_y = QLineEdit(objectName="lineEdit_color_y")
                hlayout_color_y.addWidget(label_color_y)
                hlayout_color_y.addWidget(lineEdit_color_y)

                hlayout_random = self.func_layout_random()
                hlayout_transtition, hlayout_wait = self.func_layout_transition_time()
                
                self.put_layout(self.vlayout_color_widget, hlayout_color_x, hlayout_color_y, hlayout_random, hlayout_transtition, hlayout_wait)

        except:
            pass

    def func_layout_transition_time(self):
        hlayout_transition = QHBoxLayout()
        label_transition = QLabel("전환시간(100ms)")
        spinbox_transition = QSpinBox(objectName="spinbox_transition")
        spinbox_transition.setMinimum(5)
        spinbox_transition.setMaximum(65534)
        hlayout_transition.addWidget(label_transition) 
        hlayout_transition.addWidget(spinbox_transition)

        hlayout_wait = QHBoxLayout()
        label_wait = QLabel("대기시간(100ms)")
        spinbox_wait = QSpinBox(objectName="spinbox_wait")
        spinbox_wait.setMinimum(6)
        spinbox_wait.setMaximum(65534)
        hlayout_wait.addWidget(label_wait) 
        hlayout_wait.addWidget(spinbox_wait)

        return hlayout_transition, hlayout_wait

    def func_calculate_wait_time(self, spinbox_wait):
        spinbox_wait.setMinimum(self.spinbox_transition.value() + 1)
        spinbox_wait.setValue(max(self.spinbox_transition.value() + 1, spinbox_wait.value()))

    def func_btn_start(self):
        connection_meta = {}
        connection_meta['port'] = self.comboBox_port.currentText()
        connection_meta['channel'] = int(self.lineEdit_zigbee_channel.text())
        connection_meta['zigbee_id'] = int(self.comboBox_zigbee_ids.currentText().split(':')[1], 16)

        if self.list_gen_cmd.count() < 1:
            QMessageBox.about(self, "오류" ,"수행할 명령이 존재하지 않습니다. \n 명령을 입력해주세요")    

        else:
            cmds = []
            for i in range(self.list_gen_cmd.count()):
                cmds.append(json.loads(self.list_gen_cmd.item(i).text()))
            self.worker = Worker(connection_meta, cmds, parent=self)
            self.worker.signal_command_complete.connect(self.worker_func_add_current_result)        
            # self.pushButton_start.setEnabled(False)
            self.worker.start()
            # del self.worker
            # self.pushButton_start.setEnabled(True)
            
    def func_btn_summary(self):

        self.list_summary.clear()

        now =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        experience_date = "실험일\t {}".format(now)
        self.list_summary.addItem(experience_date)
        
        rows = self.table_current_result.rowCount()
        total_cmd_count = "수행 명령어 수\t {}".format(rows)
        self.list_summary.addItem(total_cmd_count)
        
        summary = {}
        for row in range(rows):
            command = None
            cluster = None
            for column in range(self.table_current_result.columnCount()):
                item = self.table_current_result.item(row, column)
                
                if item is not None:
                    if column == 1:
                        cluster = item.text()
                        if not cluster in summary:
                            summary[item.text()] = {}
                    
                    elif column == 2:
                        command = item.text()
                        if not command in summary[cluster]:
                            summary[cluster][item.text()] = {"count": 1, "OK":0, "NG":0}
                        else:
                            summary[cluster][item.text()]["count"] = summary[cluster][item.text()]["count"] + 1
                        
                    elif column == 8:
                        if item.text() == "True":
                            summary[cluster][command]["OK"] = summary[cluster][command]["OK"] + 1
                        else:
                            summary[cluster][command]["NG"] = summary[cluster][command]["NG"] + 1

        for k, v in summary.items():
            print(k, v)
            for command, values in v.items():
                print(command, values)
                command_summary = "클러스터: {}\t CMD: {}\t 횟수: {}\t 성공: {}\t 실패: {}".format(k, command, values['count'], values['OK'], values['NG'])
                self.list_summary.addItem(command_summary)

    def func_btn_reset(self):
        # 진행상황 reset
        self.table_current_result.setRowCount(0)

        # 최종결과 reset
        self.list_summary.clear()

    def func_btn_result_save(self):
        file_names = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        
        if file_names[0]:
            try:
                f_path = file_names[0].split('.')[0]
                f_prefix = file_names[0].split('.')[1]

                raw_file = '{}_{}.{}'.format(f_path, 'raw', f_prefix)
                summary_file = '{}_{}.{}'.format(f_path, 'summary', f_prefix)
                # file_name = "{}_{}".format(file_names[0], 'entire')
                with open(raw_file, 'w', newline='', encoding='utf-8-sig') as stream:
                    writer = csv.writer(stream)
                    # get column header
                    headerdata = []
                    for col in range(self.table_current_result.columnCount()):
                        header = self.table_current_result.horizontalHeaderItem(col)
                        if header is not None:
                            headerdata.append(
                                header.text()
                            )
                    writer.writerow(headerdata)

                    for row in range(self.table_current_result.rowCount()):
                        rowdata = []
                        for column in range(self.table_current_result.columnCount()):
                            item = self.table_current_result.item(row, column)
                            if item is not None:
                                rowdata.append(
                                    item.text()
                                )
                                
                        writer.writerow(rowdata)
            
                with open(summary_file, 'w',  newline='', encoding='utf-8-sig') as stream:
                    writer = csv.writer(stream)
                    for index in range(self.list_summary.count()):
                        item = self.list_summary.item(index)
                        if item is not None:
                            writer.writerow([item.text()])

            except PermissionError:
                QMessageBox.about(self, "오류",  "파일이 열려있습니다.")

    @pyqtSlot(str)
    def worker_func_add_current_result(self, result):
        row = self.table_current_result.rowCount()
        self.table_current_result.setRowCount(row+1)

        result = result.split('\t')
        for col in range(self.table_current_result.columnCount()):
            self.table_current_result.setItem(row, col, QTableWidgetItem(result[col]))
            
            self.table_current_result.item(row,col).setForeground(QBrush(QColor(255, 255, 255)))
            if result[-1] == 'True':
                self.table_current_result.item(row,col).setBackground(QColor(0,128,0))
            else:
                self.table_current_result.item(row,col).setBackground(QColor(255,0,0))
                
        
    def clear_layout(self, layout):
        #if type(layout) == QVBoxLayout:
        while layout.count():
            child = layout.takeAt(0)
            if type(child) == QWidgetItem:
                child.widget().deleteLater()
            elif type(child) == QHBoxLayout or type(child) == QVBoxLayout:
                self.clear_layout(child)

    def put_layout(self, parent, *childs):
        for child in childs:
            parent.addLayout(child) 

from Handler.Zigbee.zigbee_driver import ZigBeeDriver
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute
import time
import datetime

class Worker(QThread):
    signal_command_complete = pyqtSignal(str) # signal for letting the main thread know that the command is done

    def __init__(self, meta, commands, parent=None):
        super().__init__()
        self.main = parent
        self.commands = commands
        self.port = meta['port']
        self.zigbee_id = meta['zigbee_id']
        self.channel = meta['channel']
        self.driver = ZigBeeDriver(self.port, self.channel, self.zigbee_id)

    def run(self): # communicate to zigbee driver class
        # TODO: make new routine for new structure
        # for task_cmd in self.commands:
        #     pass
        # Original code
        for command in self.commands:
            currents = []
            prevs = []
            command['timestamp'] = datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')    # add time stamp

            if not "CONNECT" in command['command']:
                try:
                    # get current value of attributes
                    attrs = self.create_attribute(command)    
                    for attr in attrs:
                        prevs.append(self.driver.read_attr_command(attr))
                    
                    # write command
                    self.driver.write_attr_command(command)

                    if command['cluster'] != 'ON_OFF_CLUSTER':    
                        # then, wait until remaining_time == 0
                        while True:
                            attribute = self.create_attribute(command, isRemain=True)
                            remain_time = self.driver.read_attr_command(attribute)
                            time.sleep(0.1)
                            if remain_time.value == 0:
                                break

                    attrs = self.create_attribute(command)
                    for attr in attrs:
                        currents.append(self.driver.read_attr_command(attr))
                    
                    # result validation and then, update result into the table
                    for prev, current in list(zip(prevs, currents)):
                        validator = Validator(command, prev, current)
                        result = validator.vaildate_attribute()
                        self.signal_command_complete.emit(result)
                except:
                    print("read attr is none")    

        print("현재 명령셋 종료")
        del self.driver


    def create_attribute(self, command, isRemain=False):
        # just get attribute from pre-defined command - attribute
        cluster = clusters[command['cluster']]
        cmd = commands[command['cluster']][command['command']]

        if isRemain: # read remaining time
            if cluster == LVL_CTRL_CLUSTER: 
                attribute_id, attribute_type = attributes['LVL_CTRL_REMAIN_TIME_ATTR']
            elif cluster == COLOR_CTRL_CLUSTER:
                attribute_id, attribute_type = attributes['COLOR_CTRL_REMAIN_TIME_ATTR']
            
            attr_name = "remain_time"
            attribute = Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name)
            return attribute

        else: # read value
            attrs = []
            if cluster == ON_OFF_CLUSTER: # onoff cluster only need on_off_attr
                attribute_id, attribute_type = attributes['ON_OFF_ONOFF_ATTR']
                attr_name = "ON/OFF"
                attrs.append(Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name))
            elif cluster == LVL_CTRL_CLUSTER: # update here
                attribute_id, attribute_type = attributes['LVL_CTRL_CURR_LVL_ATTR']
                attr_name = "밝기"
                attrs.append(Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name))
            elif cluster == COLOR_CTRL_CLUSTER:
                if cmd == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                    attribute_id, attribute_type = attributes['COLOR_CTRL_COLOR_TEMP_MIRED_ATTR']
                    attr_name = "온도" 
                    attrs.append(Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name))
                elif cmd == COLOR_CTRL_MV_TO_COLOR_CMD:
                    attribute_id, attribute_type = attributes['COLOR_CTRL_CURR_X_ATTR']
                    attr_name = "Color X"
                    attrs.append(Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name))
                    
                    attr_name = "Color Y"
                    attribute_id, attribute_type = attributes['COLOR_CTRL_CURR_Y_ATTR']
                    attrs.append(Attribute(cluster=cluster, id=attribute_id, type=attribute_type, name=attr_name))

            # @hipiphock
            # attrs = command.attr_list

    def stop(self):
        del self


from Handler.Zigbee.constants import commands, attributes, clusters
class Validator():
    def __init__(self, cmd, previous, current):
        self.cmd = cmd
        self.previous = previous
        self.current = current

    def new_validate_attribute(self):
        # TODO: fix Validator
        """
        new_validate_attribute function validates attributes
        based on cmd.affected_attrs lists.
        """
        # self.cmd가 TaskCmd라고 가정하고 구현하자.
        
        pass

    def vaildate_attribute(self):
        cluster = clusters[self.cmd['cluster']]
        cmd = commands[self.cmd['cluster']][self.cmd['command']]

        if cluster == ON_OFF_CLUSTER:
            if cmd == ON_OFF_ON_CMD:
                expected = True

            elif cmd == ON_OFF_OFF_CMD:    
                expected = False
                
            elif cmd == ON_OFF_TOGGLE_CMD:
                expected = not self.previous.value

        elif cluster == LVL_CTRL_CLUSTER:
            if cmd == LVL_CTRL_MV_TO_LVL_CMD or cmd == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
                expected = self.cmd['payloads'][0][0]

        elif cluster == COLOR_CTRL_CLUSTER:
            if cmd == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                expected = self.cmd['payloads'][0][0]
            
            elif cmd == COLOR_CTRL_MV_TO_COLOR_CMD:
                if 'X' in self.current.name:
                    expected = self.cmd['payloads'][0][0]
                elif 'Y' in self.current.name:
                    expected = self.cmd['payloads'][1][0]
        
        if expected == self.current.value:
            return self.formatter(True, expected)
        else:
            return self.formatter(False, expected)

    def formatter(self, isValid, expected):
        # TODO: fix formatter to appropriate one
        print(self.cmd)
        try:
            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                self.cmd['timestamp'], self.cmd['cluster'], self.cmd['command'], self.current.name,
                self.current.value, expected, self.cmd['payloads'][-1][0], self.cmd['wait'], isValid
                )
        except KeyError:
            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                self.cmd['timestamp'], self.cmd['cluster'], self.cmd['command'], self.current.name,
                self.current.value, expected, None, None, isValid
                )
        except TypeError:
            result = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                self.cmd['timestamp'], self.cmd['cluster'], self.cmd['command'], self.current.name,
                self.current.value, expected, None, None, isValid
                )
        finally:
            return result

# Cluster, commands
# CLUSTER_TABLE과 CLUSTER_FILE_TABLE들을 이용해서 cluster들을 관리한다.
# 새로운 cluster가 생성되면 이를 CLUSTER_TABLE에다가 넣는다.
# attr이나 cmd를 읽거나 써올 때에는 tas

# 명령 바꾸는 애들
class EditCmdWindow(QMainWindow):
    def __init__(self, parent, type):
        super(EditCmdWindow, self).__init__(parent)
        edit_ui = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'ui', 'edit_cmd_window.ui'))
        uic.loadUi(edit_ui, self)
        # TODO: CLUSTER_TABLE의 주기적인 업데이트, 그 이후에 get_all_cluster call을 CLUSTER_TABLE로 변경
        update_cluster_table()
        for cluster_key in CLUSTER_TABLE.keys():
            self.comboBox_cluster.addItem(cluster_key)
        self.comboBox_cluster.currentIndexChanged.connect(self.func_cluster_changed)

        if type == 0: #zigbee
            self.groupBox_1.setTitle("command 수정")
            self.groupBox_2.setTitle("attribute 수정")
            self.pushButton_save.clicked.connect(self.func_btn_edit_zigbee)

            self.tableWidget_g1.setSelectionMode(QAbstractItemView.SingleSelection)
            self.tableWidget_g1.setColumnCount(4)
            self.tableWidget_g1.setRowCount(0)  # 파일에 있는 특정 cluster의 command 만큼
            self.tableWidget_g1.setHorizontalHeaderLabels(["command id", "command name", "command desc", "affected_attrs"])

            self.tableWidget_g2.setSelectionMode(QAbstractItemView.SingleSelection)
            self.tableWidget_g2.setColumnCount(3)
            self.tableWidget_g2.setRowCount(0) # 파일에 있는 특정 cluster의 attribute 만큼
            self.tableWidget_g2.setHorizontalHeaderLabels(["attribute id", "attribute name", "attribute type"])
            self.func_cluster_changed()
        else: #ble
            # TODO: make automated routine for fetching service files
            self.groupBox_1.setTitle("service 수정")
            self.groupBox_2.setTitle("characteristic 수정")
            self.pushButton_save.clicked.connect(self.func_btn_save_ble)

        self.pushButton_delete_g1.clicked.connect(self.func_delete_row_command)
        self.pushButton_add_g1.clicked.connect(self.func_add_command)
        self.pushButton_delete_g2.clicked.connect(self.func_delete_row_attribute)
        self.pushButton_add_g2.clicked.connect(self.func_add_attribute)
        self.pushButton_cancel.clicked.connect(self.func_btn_cancel)
        self.show()

    def func_cluster_changed(self):
        """
        CLUSTER_TABEL에 저장된 정보를 기반으로 cluster 정보를 읽어들인다.
        """
        self.tableWidget_g1.setRowCount(0)
        self.tableWidget_g2.setRowCount(0)
        cluster_key = self.comboBox_cluster.currentText()
        # update_cluster_table()
        cluster = CLUSTER_TABLE[cluster_key]
        attributes = cluster.attr_table
        commands = cluster.cmd_table
        self.tableWidget_g1.setRowCount(len(commands))
        self.tableWidget_g2.setRowCount(len(attributes))
        cnt = 0
        for cmd_key in commands.keys():
            command = commands[cmd_key]
            self.tableWidget_g1.setItem(cnt, 0, QTableWidgetItem(str(hex(command.id))))
            self.tableWidget_g1.setItem(cnt, 1, QTableWidgetItem(command.name))
            self.tableWidget_g1.setItem(cnt, 2, QTableWidgetItem(command.desc))
            attr_str = str()
            for attr in command.affected_attrs:
                attr_str += attr
                attr_str += ','
            self.tableWidget_g1.setItem(cnt, 3, QTableWidgetItem(attr_str))
            cnt += 1
        cnt = 0
        for attr_key in attributes.keys():
            attribute = attributes[attr_key]
            self.tableWidget_g2.setItem(cnt, 0, QTableWidgetItem(str(hex(attribute.id))))
            self.tableWidget_g2.setItem(cnt, 1, QTableWidgetItem(str(attribute.name)))
            self.tableWidget_g2.setItem(cnt, 2, QTableWidgetItem(str(hex(attribute.type))))
            # type??
            cnt += 1
#         GUIlogger.debug("func_cluster_changed called.")
#         # @hipiphock
#         # clear table
#         while self.tableWidget_g1.rowCount() > 0:
#             self.tableWidget_g1.removeRow(0)
#         while self.tableWidget_g2.rowCount() > 0:
#             self.tableWidget_g2.removeRow(0)

#         cluster_key = self.comboBox_cluster.currentText()
#         cluster = CLUSTER_TABLE[cluster_key]
#         for cmd_key in cluster.cmd_table:
#             new_row_cnt = self.tableWidget_g1.rowCount() + 1
#             self.tableWidget_g1.setRowCount(new_row_cnt)
#             # id, name, desc, attr
#             cmd = cluster.cmd_table[cmd_key]
#             self.tableWidget_g1.setItem(new_row_cnt - 1, 0, QTableWidgetItem(str(hex(cmd.id))))
#             self.tableWidget_g1.setItem(new_row_cnt - 1, 1, QTableWidgetItem(cmd.name))
#             self.tableWidget_g1.setItem(new_row_cnt - 1, 2, QTableWidgetItem(cmd.desc))
#             attr_str = str()
#             for attr in cmd.affected_attrs:
#                 attr_str += attr
#                 attr_str += ','
#             self.tableWidget_g1.setItem(new_row_cnt - 1, 3, QTableWidgetItem(attr_str))
#         for attr_key in cluster.attr_table:
#             new_row_cnt = self.tableWidget_g2.rowCount() + 1
#             self.tableWidget_g2.setRowCount(new_row_cnt)
#             # id, name, type
#             attr = cluster.attr_table[attr_key]
#             self.tableWidget_g2.setItem(new_row_cnt - 1, 0, QTableWidgetItem(str(hex(attr.id))))
#             self.tableWidget_g2.setItem(new_row_cnt - 1, 1, QTableWidgetItem(attr.name))
#             self.tableWidget_g2.setItem(new_row_cnt - 1, 2, QTableWidgetItem(str(hex(attr.type))))
        

    def func_add_command(self, type):
        cluster_key = self.comboBox_cluster.currentText()
        if type==0: #zigbee
            input_dialog = InputZigbeeDialog(self, 1)
            input_dialog.exec_()
            cmd_id = input_dialog.cmd_id
            cmd_name = input_dialog.cmd_name
            cmd_desc = input_dialog.cmd_desc
            affected_attr_str = input_dialog.cmd_affected_attrs
            cmd_affected_attrs = None
            if affected_attr_str != None:
                cmd_affected_attrs = affected_attr_str.split(',')
            new_cmd = Cmd(int(cmd_id, 16), cmd_name, cmd_desc, cmd_affected_attrs)
            CLUSTER_TABLE[cluster_key].cmd_table[cmd_name] = new_cmd
            if cmd_id != "" and cmd_desc != "":
                new_row_cnt = self.tableWidget_g1.rowCount() + 1
                self.tableWidget_g1.setRowCount(new_row_cnt)
                self.tableWidget_g1.setItem(new_row_cnt-1,0,QTableWidgetItem(cmd_id))
                self.tableWidget_g1.setItem(new_row_cnt-1,1,QTableWidgetItem(cmd_name))
                self.tableWidget_g1.setItem(new_row_cnt-1,2,QTableWidgetItem(cmd_desc))
                self.tableWidget_g1.setItem(new_row_cnt-1,3,QTableWidgetItem(affected_attr_str))
                self.tableWidget_g1.resizeRowsToContents()
        else: #ble
            input_dialog = InputBLEDialog(self,1)

    def func_add_attribute(self, type):
        cluster_key = self.comboBox_cluster.currentText()
        if type==0: #zigbee
            input_dialog = InputZigbeeDialog(self, 2)
            input_dialog.exec_()
            attr_id = input_dialog.attr_id
            attr_name = input_dialog.attr_name
            attr_desc = "temp"  # TODO: fix desc
            attr_type = input_dialog.attr_type
            new_attr = Attr(int(attr_id, 16), attr_name, attr_desc, int(attr_type, 16))
            CLUSTER_TABLE[cluster_key].attr_table[attr_name] = new_attr
            if attr_id is not None and attr_name is not None and attr_type is not None and attr_id !="" and attr_name != "" and attr_type !="":
                new_row_cnt = self.tableWidget_g2.rowCount() + 1
                self.tableWidget_g2.setRowCount(new_row_cnt)
                self.tableWidget_g2.setItem(new_row_cnt-1,0,QTableWidgetItem(attr_id))
                self.tableWidget_g2.setItem(new_row_cnt-1,1,QTableWidgetItem(attr_name))
                self.tableWidget_g2.setItem(new_row_cnt-1,2,QTableWidgetItem(attr_type))
        else: #ble
            input_dialog = InputBLEDialog(self,2)
    
    def func_delete_row_command(self):
        cluster_key = self.comboBox_cluster.currentText()
        row = self.tableWidget_g1.currentRow()
        cmd_key = self.tableWidget_g1.item(row, 1).text()
        del CLUSTER_TABLE[cluster_key].cmd_table[cmd_key]
        self.tableWidget_g1.removeRow(row)
    
    def func_delete_row_attribute(self):
        cluster_key = self.comboBox_cluster.currentText()
        row = self.tableWidget_g2.currentRow()
        attr_key = self.tableWidget_g2.item(row, 1).text()
        del CLUSTER_TABLE[cluster_key].attr_table[attr_key]
        self.tableWidget_g2.removeRow(row)

    def func_btn_edit_zigbee(self):
        """
        CLUSTER_TABLE을 저장한다.
        """
        for cluster_key in CLUSTER_TABLE:
            cluster = CLUSTER_TABLE[cluster_key]
            cluster.writeClusterFile(CLUSTER_FILE_TABLE[cluster_key])
        self.close()
    
    def func_btn_save_ble(self):
        # TODO: implement
        self.close()

    def func_btn_cancel(self):
        self.close()

class EditClusterWindow(QMainWindow):
    def __init__(self, parent):
        super(EditClusterWindow, self).__init__(parent)

        input_ui = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'ui', 'edit_cluster_window.ui'))
        uic.loadUi(input_ui, self)
        self.listWidget.itemDoubleClicked.connect(self.func_btn_delete)
        update_cluster_table()
        for cluster_key in CLUSTER_TABLE.keys():
            self.listWidget.addItem(QListWidgetItem(cluster_key))
        self.pushButton_add.clicked.connect(self.func_btn_add)
        self.pushButton_cancel.clicked.connect(self.func_btn_cancel)
        self.pushButton_delete.clicked.connect(self.func_btn_delete)
        self.show()
    
    def func_btn_add(self):
        """
        새로운 cluster를 만든다.
        problem: 새로운 cluster file을 만든 후 파일로 언제 저장할까?
        """
        input_dialog = InputClusterDialog(self)
        input_dialog.exec_()
        cluster_id = input_dialog.cluster_id
        cluster_name = input_dialog.cluster_name
        if cluster_id is not None and cluster_name is not None and cluster_id != "" and cluster_name != "":
            # update new cluster to CLUSTER_TABLE
            new_cluster = Cluster(cluster_id, cluster_name)
            CLUSTER_TABLE[cluster_name] = new_cluster
            # update new cluster's filepath to CLUSTER_FILE_TABLE
            cluster_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'src', 'Handler', 'Zigbee', 'Clusters'))
            upper_name = cluster_name.upper()
            filename = os.path.join(cluster_path, upper_name+".json")
            new_cluster.writeClusterFile(filename)
            CLUSTER_FILE_TABLE[cluster_name] = filename
            self.listWidget.addItem(QListWidgetItem(cluster_name))

    def func_btn_delete(self):
        """
        cluster를 지운다.
        problem: cluster file을 언제 지울 것인가?
        """
        seleted = self.listWidget.currentItem().text() +".json"
        delete_filename =os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'src', 'Handler', 'Zigbee', 'Clusters', seleted))
        if os.path.isfile(delete_filename):
            os.remove(delete_filename)
            self.listWidget.takeItem(self.listWidget.currentRow())

    
    def func_btn_cancel(self):
        self.close()
# =======
#     # @hipiphock
#     def func_btn_edit_zigbee(self):
#         # 그냥 바로 CLUSTER_TABLE을 저장하는 식으로 바꾼다.
#         for cluster_key in CLUSTER_TABLE:
#             cluster = CLUSTER_TABLE[cluster_key]
#             cluster.writeClusterFile(CLUSTER_FILE_TABLE[cluster_key])
#         self.close()
    
#     def func_btn_save_ble(self):
#         # TODO: implement save ble
#        self.close()
# >>>>>>> master


class InputClusterDialog(QDialog):
    def __init__(self, parent):
        super(InputClusterDialog, self).__init__(parent)
        self.cluster_id = None
        self.cluster_name = None

        input_ui = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'ui', 'input_cluster_dialog.ui'))
        uic.loadUi(input_ui, self)
        self.setAutoFillBackground(True)
        self.pushButton_save.clicked.connect(self.func_btn_save)
        self.pushButton_cancel.clicked.connect(self.func_btn_cancel)
        self.show()
    
    def func_btn_save(self):
        self.cluster_name = self.lineEdit_cluster_name.text()
        self.cluster_id = self.lineEdit_cluster_id.text()
        self.cluster_name = self.lineEdit_cluster_name.text()
        self.close()
    
    def func_btn_cancel(self):
        self.close()

class InputZigbeeDialog(QDialog):
    def __init__(self, parent, choice):
        super(InputZigbeeDialog, self).__init__(parent)
        self.choice = choice
        self.cmd_id = None
        self.cmd_name = None
        self.cmd_desc = None
        self.cmd_affected_attrs = None
        self.attr_id = None
        self.attr_name = None
        self.attr_type = None

        input_ui = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'ui', 'input_zigbee_dialog.ui'))
        uic.loadUi(input_ui, self)
        self.setAutoFillBackground(True)
        if choice == 1:
            self.groupBox_attr.setEnabled(False)
            self.groupBox_cmd.setEnabled(True)
        else:
            self.groupBox_attr.setEnabled(True)
            self.groupBox_cmd.setEnabled(False)
        self.pushButton_add.clicked.connect(self.func_btn_add)
        self.pushButton_cancel.clicked.connect(self.func_btn_cancel)
        self.show()
    
    def func_btn_add(self):
        if self.choice == 1:
            self.cmd_id = self.lineEdit_cmd_id.text()
            self.cmd_name = self.lineEdit_cmd_name.text()
            self.cmd_desc = self.lineEdit_cmd_desc.text()
            self.cmd_affected_attrs = self.lineEdit_cmd_affected_attrs.text()
        else:
            self.attr_id = self.lineEdit_attr_id.text()
            self.attr_name = self.lineEdit_attr_name.text()
            self.attr_type = self.lineEdit_attr_type.text()
        self.close()
    
    def func_btn_cancel(self):
        self.close()

class InputBLEDialog(QDialog):
    def __init__(self, parent, choice):
        super(InputBLEDialog, self).__init__(parent)
        self.choice = choice
        self.service_id = None
        self.service_desc = None
        self.attr_id = None
        self.attr_name = None
        self.attr_type = None

        input_ui = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'ui', 'input_ble_dialog.ui'))
        uic.loadUi(input_ui, self)
        self.setAutoFillBackground(True)
        if choice == 1:
            self.groupBox_attr.setEnabled(False)
            self.groupBox_service.setEnabled(True)
        else:
            self.groupBox_attr.setEnabled(True)
            self.groupBox_service.setEnabled(False)
        self.pushButton_add.clicked.connect(self.func_btn_add)
        self.pushButton_cancel.clicked.connect(self.func_btn_cancel)
        self.show()
    
    def func_btn_add(self):
        if self.choice == 1:
            self.service_id = str(self.lineEdit_service_id.text())
            self.service_desc = str(self.lineEdit_service_desc.text())
        else:
            self.attr_id = self.lineEdit_attr_id.text()
            self.attr_name = self.lineEdit_attr_name.text()
            self.attr_type = self.lineEdit_attr_type.text()
        self.close()
    
    def func_btn_cancel(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        myWindow = WindowClass(bool(sys.argv[1]))
    except:
        myWindow = WindowClass()
    
    myWindow.show()
    app.exec_()


