import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import *
import random
from random import randint
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams,BoardIds
from PyQt5.QtCore import Qt
import winsound as sd
import time
from pprint import pprint
random.seed()

     
class WindowClass(QMainWindow):
    def __init__(self) :
        super().__init__()
        self.setGeometry(0,0,width, height)
        self.setWindowTitle('Set Protocol')
        self.data_list=[]
        self.time_list=[]
        self.count_list=[]
        self.timer = QTimer(self)
        self.time =0
        #label
        self.label = QLabel("실험을 시작하려면 시작하기 버튼을 눌러주세요", self)
        font1 = self.label.font()
        font1.setBold(True)
        font1.setPointSize(40)
        self.label.setFont(font1)
        self.label.setGeometry(1200,350,1300,500)
        #button
        self.btn_1= QPushButton("시작하기",self)
        self.btn_1.setGeometry(1650,800,200,80)
        self.btn_1.clicked.connect(self.btn_1_clicked)
        
    
    def btn_1_clicked(self):
        global trial
        global last
        self.label.clear()
        self.btn_1.hide()
        global ref ,r_num, ran_n, a
        ref =10000
        last=0
        r_num=0
        trial=0
        ran_n=0
        
        a=1
        QTimer.singleShot(0, self.beepsound) #1
        QTimer.singleShot(0, self.time_n)
        QTimer.singleShot(10000, self.beepsound) #2
        QTimer.singleShot(10000, self.time_n)

        for trial in range(1): 
                 
           
            ref += r_num
            QTimer.singleShot(ref, self.point) #3

            QTimer.singleShot(ref, self.time_n)
            QTimer.singleShot(ref+5000, self.close1) #4
            QTimer.singleShot(ref+5000, self.time_n)
            
            QTimer.singleShot(ref+5000, self.random) #5
            QTimer.singleShot(ref+5000, self.time_n)
            QTimer.singleShot(ref+7500, self.close2) #6
            QTimer.singleShot(ref+7500, self.time_n)
            QTimer.singleShot(ref+7500, self.point1) #7
            QTimer.singleShot(ref+7500, self.time_n)
            QTimer.singleShot(ref+10000, self.close3) #8
            QTimer.singleShot(ref+10000, self.time_n)
                
            QTimer.singleShot(ref+10000, self.random) #9
            QTimer.singleShot(ref+10000, self.time_n)
            QTimer.singleShot(ref+12500, self.close2) #10
            QTimer.singleShot(ref+12500, self.time_n)
            QTimer.singleShot(ref+12500, self.point1) #11
            QTimer.singleShot(ref+12500, self.time_n)
            QTimer.singleShot(ref+15000, self.close3) #12
            QTimer.singleShot(ref+15000, self.time_n)
                
            QTimer.singleShot(ref+15000, self.random) #13
            QTimer.singleShot(ref+15000, self.time_n)
            QTimer.singleShot(ref+17500, self.close2) #14
            QTimer.singleShot(ref+17500, self.time_n)
            QTimer.singleShot(ref+17500, self.point1) #15
            QTimer.singleShot(ref+17500, self.time_n)
            QTimer.singleShot(ref+20000, self.close3) #16
            QTimer.singleShot(ref+20000, self.time_n)
                
            QTimer.singleShot(ref+20000, self.random) #17
            QTimer.singleShot(ref+20000, self.time_n)
            QTimer.singleShot(ref+22500, self.close2) #18
            QTimer.singleShot(ref+22500, self.time_n)
            QTimer.singleShot(ref+22500, self.point1) #19
            QTimer.singleShot(ref+22500, self.time_n)
            QTimer.singleShot(ref+25000, self.close3) #20  
            QTimer.singleShot(ref+25000, self.ran)    
            QTimer.singleShot(ref+25000, self.time_n)                         
            last=25000
            r_num=last
        QTimer.singleShot(ref+r_num+500,self.pr_data)   
        QTimer.singleShot(ref+r_num,self.thank)
        QTimer.singleShot(ref+r_num+4000,self.clo)
            
    def pr_data(self):
        board.stop_stream()
        board.release_session()
        data = board.get_board_data()
        data=pd.DataFrame(data)
        data.to_csv("result_02.csv")
        time_list=pd.DataFrame(self.time_list)
        count_list=pd.DataFrame(self.count_list)
        time_list=pd.concat([time_list,count_list],axis=1).T
        time_list.to_csv("time_02.csv")
        
        #globals()['data{}'.format(trial)]=pd.DataFrame(data)
        #self.data_list.append(globals()['data{}'.format(trial)])

    def ran(self):
        global ran_n      
        ran_n += 1    
    def save(self):
        #data_save=pd.concat(self.data_list)
        data_save = pd.DataFrame(self.data_list)
        data_save.to_csv("result_01.csv")
    def thank(self):
        protocol.thank(self)
    def rest(self):
        protocol.rest(self)
    def time_n(self):
        global a
        
        board.insert_marker(a)
        self.time_list.append(time.time())
        self.count_list.append(a)
        a += 1
        
    def clo(self):
        self.close()
    def beepsound(self):
        fr = 2000    # range : 37 ~ 32767
        du = 200     # 1000 ms ==1second
        sd.Beep(fr, du) # winsound.Beep(frequency, duration)
         
    def point (self):
        global a
        protocol.point(self)
        a=3
       

    def random(self): 
        protocol.random(self)
       
        
    def point1(self):   
        protocol.point1(self)
      
      
    def point_blue(self):
        protocol.point_blue(self)
        
             
    def close1(self):
        label2.close()  
       
    def close2(self):
        label3.close() 
      
    def close3(self):
        label4.close()  
    def close4(self):
        label5.close() 
        
        
class protocol(WindowClass):
    def __init__(self) :
        super().__init__()
    
    def point(self):
        global label2
        label2 = QLabel("·",self)
        font2 = label2.font()
        font2.setBold(True)
        font2.setPointSize(300)
        label2.setFont(font2)
        label2.setGeometry(1700,650,200,100)
        label2.show()
    
                
    def close1():
        label2.close()
                
    def random(self):
        target=["열어","전화","연락처","메세지","카카오톡","검색","볼륨","화면","음소거","키보드"]

        global label3   
        
        
        label3= QLabel(target[ran_n],self)
        font2 = label3.font()
        font2.setBold(True)
        font2.setPointSize(50)
        label3.setFont(font2)
        font2.setFamily('초코쿠키체')
        label3.setGeometry(1700,620,1000,100)
        label3.show()
        
    def close2():
        label3.close()
        
    def point1(self):
        global label4
        label4 = QLabel("·",self)
        font2 = label4.font()
        font2.setBold(True)
        font2.setPointSize(300)
        label4.setStyleSheet("color: blue")
        label4.setFont(font2)
        label4.setGeometry(1700,650,200,100)
        label4.show()
        
    def close3():
        label4.close() 
    def point_blue(self):
        global label5
        label5 = QLabel("·",self)
        font2 = label5.font()
        label5.setStyleSheet("color: blue")
        font2.setBold(True)
        font2.setPointSize(300)
        label5.setFont(font2)
        label5.setGeometry(1700,650,200,100)
        label5.show()
        
    def close4():
        label5.close()
    def thank(self):
        global label6
        label6=QLabel("      실험이 모두 종료되었습니다.\n 참가하신 피험자님 고생 많으셨습니다.",self)
        font3 = label6.font()
        font3.setBold(True)
        font3.setPointSize(50)
        label6.setFont(font3)
        label6.setGeometry(1100,550,1500,300)
        label6.show()
    def rest(self):
        global label7
        label7=QLabel("                           쉬는 시간입니다.\n 5분간 휴식 후 진행 할 예정이니 휴대폰을 하거나 안정을 취하세요.",self)
        font4 = label7.font()
        font4.setBold(True)
        font4.setPointSize(50)
        label7.setFont(font4)
        label7.setGeometry(900,550,2100,300)
        label7.show()

        
class fun:
    def start_board():
        serial_port= "COM4"
        params = BrainFlowInputParams() 
        params.serial_port = serial_port 
        params.serial_number = '' 
        params.timeout = 0 
        params.other_info = '' 
        params.file = '' 
        params.mac_address = '' 
        params.ip_address = '' 
        params.ip_port = 0 
        params.ip_protocol = 0
        board = BoardShim(BoardIds.CYTON_DAISY_BOARD, params) 
        board.prepare_session()
        #board.config_board('xU060100X') 
        board.start_stream()
        return board
            
    
        
        
if __name__ == "__main__" :
    board_id=2
    pprint(BoardShim.get_board_descr(board_id))
    board = fun.start_board()

    
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    screen_rect = app.desktop().screenGeometry()
    width,height = screen_rect.width(), screen_rect.height()
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()