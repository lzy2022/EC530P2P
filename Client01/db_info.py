# EC530 Project 2 By Zhiyuan Liu
# This file contains the function and constants about the data base
from os.path import exists
from socket import MsgFlag
import sqlite3
from time import time

from flask import get_flashed_messages

class DB_acc_info:
    
    # initialize the empty dict
    def __init__(self, addr):
        global db_addr
        db_addr = './Client.db'
        if exists(addr):
            db_addr = addr
        else:
            print("db file not exist\n")
    
    def save_msg(self, s_uid, r_uid, time, msg, syn_state = 'SYN', dis_state = 'N'):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("INSERT INTO msg (user_id_s, user_id_r, content, time, syn_state, dis_state) VALUES (?, ?, ?, ?, ?, ?)",
                (s_uid, r_uid, msg, time, syn_state, dis_state,))
        con.commit()
        con.close()
        return True
    
    def get_msg_chat(self, u_id):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("SELECT * FROM msg WHERE user_id_r = ? OR user_id_s = ? ORDER BY time ASC", (u_id, u_id,))
        u = cur.fetchall()
        con.close()
        msg_list = []
        for row in u:
            msg_list.append({'from': row[0], 'to': row[1], 'time': row[3], 'content': row[2]})
        return msg_list 
    
    def get_msg_chat_ndis(self, u_id):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("SELECT * FROM msg WHERE (user_id_r = ? OR user_id_s = ?) AND dis_state = ? ORDER BY time ASC", (u_id, u_id, 'N',))
        u = cur.fetchall()
        cur.execute("UPDATE msg SET dis_state = ? WHERE (user_id_r = ? OR user_id_s = ?) AND dis_state = ?", ('Y', u_id, u_id, 'N',))
        con.commit()
        con.close()
        msg_list = []
        for row in u:
            msg_list.append({'from': row[0], 'to': row[1], 'time': row[3], 'content': row[2]})
        return msg_list 
    
    def del_msg__q(self):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("DELETE FROM msg WHERE content = ?", ('__q',))
        con.commit()
        con.close()
    
    def init_msg_chat(self, u_id):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("UPDATE msg SET dis_state = ? WHERE user_id_r = ? OR user_id_s = ?", ('N', u_id, u_id,))
        con.commit()
        con.close()        
        return True
    
    def get_msg_pend(self):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("SELECT * FROM msg WHERE syn_state = ?", ('ASYN',))
        u = cur.fetchall()
        con.close()
        msg_list = []
        for row in u:
            msg_list.append({'from': row[0], 'to': row[1], 'time': row[3], 'content': row[2]})
        return msg_list 
    
    def syn_msg_pend(self, r_uid, time, msg):
        con = sqlite3.connect(db_addr)
        cur = con.cursor()
        cur.execute("UPDATE msg SET syn_state = ? WHERE user_id_r = ? AND content = ? AND time = ?", ('SYN', r_uid, msg, time,))
        con.commit()
        con.close()
    