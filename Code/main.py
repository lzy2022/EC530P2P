from flask import Flask, url_for, jsonify, request
from flask_restful import Api, Resource, reqparse
from numpy import require
from db_info import DB_acc_info
import sys
import rsa

app = Flask(__name__)
api = Api(app)

db_addr = './Sever.db'
key_addr = './SeverKey_Private.pem'

db_ac = None
sever_key_private = None

class User_Login(Resource):
    def post(self): 
        u_id = rsa.decrypt(request.files['u_id'].read(), sever_key_private)
        pw = rsa.decrypt(request.files['pw'].read(), sever_key_private)
        port = request.files['port'].read()
        key = request.files['key'].read()
        u_id = u_id.decode(encoding='UTF-8')
        pw = pw.decode(encoding='UTF-8')
        port = port.decode(encoding='UTF-8')
        key = key.decode(encoding='UTF-8')
        u_ip = request.remote_addr
        state = db_ac.user_login(u_id, pw, u_ip, port, key)
        if state == True:
            return {'message':'Loged in', 'client_ip': u_ip}, 200
        else:
            return {'message':'Login falied'}, 400

class User_Logout(Resource):
    def post(self):
        u_id = rsa.decrypt(request.files['u_id'].read(), sever_key_private)
        pw = rsa.decrypt(request.files['pw'].read(), sever_key_private)
        u_id = u_id.decode(encoding='UTF-8')
        pw = pw.decode(encoding='UTF-8')
        state = db_ac.user_logout(u_id, pw)
        if state == True:
            return {'message':'Loged out'}, 200
        else:
            return {'message':'Logout falied'}, 400
        
class New_User(Resource):
    def post(self):
        u_id = rsa.decrypt(request.files['u_id'].read(), sever_key_private)
        pw = rsa.decrypt(request.files['pw'].read(), sever_key_private)
        u_id = u_id.decode(encoding='UTF-8')
        pw = pw.decode(encoding='UTF-8')
        state = db_ac.add_user(u_id, pw)
        if state == True:
            return {'message': 'User Added'}, 200
        else:
            return {'message': 'Please Use Another User ID'}, 400

class Get_User_List(Resource):
    def get(slef):
        return {'user_list': db_ac.get_user_list()}

    
api.add_resource(User_Login, '/login')
api.add_resource(User_Logout, '/logout')
api.add_resource(Get_User_List, '/online_list')
api.add_resource(New_User, '/reg')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_addr = sys.argv[1]
    db_ac = DB_acc_info(db_addr)
    sever_f = open(key_addr,'r')
    sever_key_private = rsa.PrivateKey.load_pkcs1(sever_f.read(), 'PEM')
    sever_f.close() 
    app.run(debug=True)