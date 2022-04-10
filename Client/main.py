import json
from matplotlib.pyplot import cla
from db_info import DB_acc_info
import random
import copy
import sys
import datetime
import time
import requests
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

db_addr = './Client.db'
db_ac = DB_acc_info(db_addr)
SEVER_BASE = "http://127.0.0.1:5000/"
        
class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == 'localhost':
            host = '127.0.0.1'
        self.local_port = port
        self.local_ip = host
        self.id = host, port
        self.user_id = ''
        self.user_pw = ''
        self.chat_uid = ''
        self.user_list = {}
        self.login_state = False
    
    def startProtocol(self):
        while(self.login_state == False):
            self.user_id = input('User ID: ')
            self.user_pw = input('Pass Word: ')
            response = requests.post(SEVER_BASE + "/login", 
                                     files={'u_id': self.user_id.encode(encoding='UTF-8'),
                                            'pw': self.user_pw.encode(encoding='UTF-8'),
                                            'port': str(self.local_port).encode(encoding='UTF-8')})
            if((response.json())['message'] == 'Loged in'):
                self.local_ip = (response.json())['client_ip']
                self.login_state = True
                break
            else:
                print('Login Failed...')
        self.update_user_list()
        print('Now loged in as ' + self.user_id)
        reactor.callInThread(self.text_UI)
        
    def datagramReceived(self, datagram, addr):
        msg = json.loads(datagram.decode('utf-8'))
        user_id_s = msg['user_id_s']
        content = msg['content']
        time = msg['time']
        if(content == '__SYNC'):
            sync_result = self.sync_all_msg()
        elif(content == '__q'):
            pass
        else:
            self.receive_msg(user_id_s, content, time)
    
    def send_msg(self, user_id_r, content, time):
        msg = {}
        msg['user_id_s'] = self.user_id
        msg['content'] = content
        msg['time'] = time
        encoded_msg = json.dumps(msg).encode('utf-8')
        self.transport.write(encoded_msg, 
                             (self.user_list[user_id_r][0],int(self.user_list[user_id_r][1])))
    
    def send_sync_request(self, user_id_r):
        if user_id_r in self.user_list.keys():
            self.send_msg(user_id_r, '__SYNC', '100000')
    
    def sync_all_msg(self):
        self.update_user_list()
        msg_list = db_ac.get_msg_pend()
        sent_count = 0
        fail_count = 0
        online_list = self.user_list.keys()
        for msg in msg_list:
            if msg['to'] in online_list:
                self.send_msg(msg['to'], msg['content'], msg['time'])
                db_ac.syn_msg_pend(msg['to'], msg['time'], msg['content'])
                sent_count += 1
            else:
                fail_count += 1
        return [sent_count, fail_count]
        
    def update_user_list(self):
        response = requests.get(SEVER_BASE + "/online_list")
        self.user_list = (response.json())['user_list']

    def receive_msg(self, user_id_s, content, time):
        db_ac.save_msg(user_id_s, self.user_id, time, content, 'SYN', 'N')
        if user_id_s != self.chat_uid:
            print('***New Message From ' + user_id_s + '***')
        return True

    def chatbox_minitor(self):
        while True:
            time.sleep(0.5)
            msg_list = db_ac.get_msg_chat_ndis(self.chat_uid)
            if(msg_list != []):
                for msg in msg_list:
                    if(msg['content'] == '__q'):
                        db_ac.del_msg__q()
                        self.chat_uid = ''
                        break
                    print('From ' + msg['from'] + ' To ' + msg['to'] + ' At ' + msg['time'] + ':')
                    print(msg['content'] + '\n')
                

    def text_UI(self):
        info = '''
        -r: Refresh online user list & resend all pending message
        -l: List all online users
        -c: Open a chat session with <user_id> 
            (message will be saved locally if <user_id> is not online.
            use -r to resend all pending message when <user_id> is online)
        -q: Logout and Quit (then use Ctrl + C to quit the program)'''
        while True:
            command = input(info + '\n')
            if(command == '-r'):
                self.update_user_list()
                msg_result = self.sync_all_msg()
                print('Refreshed Online State...')
                print('Synchronized ' + str(msg_result[0]) + ' Message')
                print('Failed ' + str(msg_result[1]) + ' Message')
                pass
            elif(command == '-l'):
                print('Following Users Are ONLINE: ')
                online_list = self.user_list.keys()
                for user_id in online_list:
                    print(user_id)
                pass
            elif(command == '-c'):
                db_ac.del_msg__q()
                online_list = self.user_list.keys()
                self.chat_uid = input('Enter a user_id to open the chat room: ')
                db_ac.init_msg_chat(self.chat_uid)
                self.update_user_list()
                self.send_sync_request(self.chat_uid)
                msg_result = self.sync_all_msg()
                print('Now opened a chat room with' + self.chat_uid)
                print('Type __q to quite the chat room')
                reactor.callInThread(self.chatbox_minitor)
                while True:
                    msg_content = input()
                    self.update_user_list()
                    online_list = self.user_list.keys()
                    current_t = str(datetime.datetime.now())
                    if self.chat_uid in online_list:
                        self.send_msg(self.chat_uid, msg_content, current_t)
                        db_ac.save_msg(self.user_id, self.chat_uid, current_t, msg_content, 'SYN', 'N')
                    else:
                        db_ac.save_msg(self.user_id, self.chat_uid, current_t, msg_content, 'ASYN', 'N')
                    if msg_content == '__q':
                        break
                            
            elif(command == '-q'):
                response = requests.post(SEVER_BASE + "/logout", 
                                         files={'u_id':self.user_id.encode(encoding='UTF-8'),
                                                'pw': self.user_pw.encode(encoding='UTF-8')})
                return True
            else:
                print('Invalid Command: ' + command)
            
    
if __name__ == "__main__":
    port = int(input('Please Select A Port (2000~5000): '))
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()