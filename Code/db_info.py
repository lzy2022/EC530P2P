# EC530 Project 2 By Zhiyuan Liu
# This file contains the function and constants about the data base
from os.path import exists
import sqlite3

class DB_acc_info:
    
    # initialize the empty dict
    def __init__(self, addr):
        global db_addr
        db_addr = './Sever.db'
        if exists(addr):
            db_addr = addr
        else:
            print("db file not exist\n")
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("SELECT user_id FROM user_pw", ())
        users = cur.fetchall()
        self.user_list = {}
        self.user_ip_list = {}
        self.uid_list = []
        for user_id in users:
            self.user_list[user_id] = False
            self.user_ip_list[user_id] = ''
            self.uid_list.append(user_id)
        con.close()
            
    def varify_user(self, u_id, pw):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("SELECT * FROM user_pw WHERE user_id = ?", (u_id,))
        user = cur.fetchone()
        con.close()
        # check if the id not exist
        if user == None:
            return False
        if user[1] != pw:
            return False
        return True
    
    def set_user_state(self, u_id, state):
        self.user_list[u_id] = state
        
    def set_user_ip(self, u_id, ip):
        self.user_ip_list[u_id] = ip
            
    def user_login(self, user_id, pw, u_ip):
        if self.varify_user(user_id, pw) == False:
            return False
        else:
            self.set_user_state(user_id, True)
            self.set_user_ip(user_id, u_ip)
        return True
            
    def user_logout(self, user_id, pw):
        if self.varify_user(user_id, pw) == False:
            return False
        else:
            self.set_user_state(user_id, False)
            self.set_user_ip(user_id, '')
        return True
    
    def get_user_list(self):
        ip_dic = {}
        for user in self.uid_list:
            if self.user_list[user] == True:
                if self.user_ip_list[user] != '':
                    ip_dic[user] = self.user_ip_list[user]
        return ip_dic
    