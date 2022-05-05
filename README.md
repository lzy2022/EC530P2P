# EC530 P2P Project
## Intro
This project contains a P2P chat app (client application & user discover sever). The user discover sever is implement using RESTful API; client application is a twisted sever sending / recieving packages from other clients / sever.

 [Github Structure](#Github-Structure)
 
 [Setting up Back-end Sever](#Setting-up-Back-end-Sever)
 
 [Session Examples](#Session-Examples)
 
 

## Github Structure
### Top Level
    - .github
    - Code (*Code for sever-end application)
    - Client (*Code for client-end application)
    - Client01 & Client02 (Testing copy)
    - Flake8_Styles
    - requirements.txt
    - README.md
#### Code 
    - main.py
          main.py contains the main function of Sever. This file is used to launch the back-end server
    - requirements.txt
          Config info for google cloud sever
    - Sever.db
          Database of the sever, contains user IDs & passwords
    - db_info
          Module for database interface
    - SeverKey_Private.pem
          Private key for the sever
    - API_test.py
          A test session
#### Client
    - main.py
          Contains the main function of client application
    - Client.db
          Database of the client application, stores all the chat messages send from/to the local account
    - db_info.py 
          Module for database interface
    - SeverKey_Public.pem
          Public key to communicate with the sever
    - test.py
          A test session
    - ClientKey_Private.pem & ClientKey_Public.pem
          These two files would be generated after running the clent application, stores a pair of keys used to communicate with other client applications
  
## Setting up Back-end Sever
This project is designed for google cloud. To set up the sever, just run the following line in the Code folder:
        gcloud app deploy

The google cloud sever should have the following APIs enabled:

        google-api-python-client
        google-cloud-tasks==2.7.1

The sever-end application is based on RESTful Flask, communicates with the client-end through http calls. Following functions are supported by the sever:

    - https://sever_addr/login:
          User login with user ID & password (both encrypted), submitting their public key so that other clients can communicate with them. 
    - https://sever_addr/logout:
          User logout with user ID & password (both encrypted)
    - https://sever_addr/online_list:
          Get all the online user IDs and their public keys
    - https://sever_addr/reg:
          Register a new account with user ID & password (both encrypted) 

After user login with user ID & password, the client application would upload the public key and pull the newest online list (contains user IDs & public keys of other users)from the sever. Then 
                                                                                        
## Session Examples
The first step is to create the client application in a seperate folder. The client application would create a new key set if there is no key found in the current folder.

The user first need to register for a new account:
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/1.PNG)

Login with the new account
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/2.PNG)
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/3.PNG)

Sent message to anouther user test02 (test02 does not have to be online)
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/4.PNG)

test02 would receive info that **New Message From test01**
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/5.PNG)

chat room can be opened and start a chat session
![alt text](https://github.com/lzy2022/EC530P2P/raw/main/images/6.PNG)
