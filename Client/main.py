from ast import arg
from flask import Flask, url_for, jsonify, request
from flask_restful import Api, Resource, reqparse
from numpy import require
from db_info import DB_acc_info
import random
import copy
import sys
import requests

app = Flask(__name__)
api = Api(app)

db_addr = './Sever.db'

db_ac = None

class User_Login(Resource):
    def post(self): 
        u_id = request.files['u_id'].read()
        pw = request.files['pw'].read()
        u_id = u_id.decode(encoding='UTF-8')
        pw = pw.decode(encoding='UTF-8')
        u_ip = request.remote_addr
        state = db_ac.user_login(u_id, pw, u_ip)
        if state == True:
            return {'message':'Loged in', 'client_ip': u_ip}, 200
        else:
            return {'message':'Login falied'}, 400

class User_Logout(Resource):
    def post(self):
        u_id = request.files['u_id'].read()
        pw = request.files['pw'].read()
        u_id = u_id.decode(encoding='UTF-8')
        pw = pw.decode(encoding='UTF-8')
        state = db_ac.user_logout(u_id, pw)
        if state == True:
            return {'message':'Loged out'}, 200
        else:
            return {'message':'Logout falied'}, 400

class Get_User_List(Resource):
    def get(slef):
        return {'user_list': db_ac.get_user_list()}

    
api.add_resource(User_Login, '/login')
api.add_resource(User_Logout, '/logout')
api.add_resource(Get_User_List, '/online_list')




user_list = {}
db_addr = './Sever.db'
db_ac = None
user_id = ''
local_port = 4999
SEVER_BASE = "http://127.0.0.1:5000/"

def update_user_list():
    response = requests.get(SEVER_BASE + "/online_list")
    user_list = (response.json())['user_list']
    



if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_addr = sys.argv[1]
    db_ac = DB_acc_info(db_addr)
    app.run(debug=True)