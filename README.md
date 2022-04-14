# EC530_Project4
## Intro
This RESTful API is designed and powered uing google cloud sever. When posting http request with speech file, please encode the speech file as '.wav' with sample rate = 16000Hz and single track

 [Github Structure](#Github-Structure)
 
 [Setting up Back-end Sever](#Setting-up-Back-end-Sever)
 
 [Functions of RESTful API & Request Formates](#Functions-of-RESTful-API-and-Request-Formates)
 
 [----Post Speech File](#Post-Speech-File)
 
 [----Get Task State](#Get-Task-State)
 
 [----Get Task Result](#Get-Task-Result)
 
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
        
## Functions of RESTful API and Request Formates
The following parts contain formates and functions that can be called from the front-end side using http requests. Users need to import the following python modules:

        import requests
        import json
        
### Post Speech File
The address to post the file is [http://'sever_address'/s2t/]. Posting a speech file can be done using the following request: 

        BASE = "http://ec530pj4.uk.r.appspot.com/"
        # speech file should have sample rate = 16000 and single track
        with open([Speech File Location], 'rb') as s_file: 
          response = requests.post(BASE + "s2t/" + '[any digit]', files={'file': s_file})
        
[response] containse a dictionary with key = {'task_id'}. task_id is the sever-side queued task id created for this post request, user can use task_id to track the completion states of the task and request for the task result.

### Get Task State
The address to get task state is [http://'sever_address'/task_state/].

        BASE = "http://ec530pj4.uk.r.appspot.com/"
        response = requests.get(BASE + "task_state/" + str([task_id]))
        
[response] containse a dictionary with key = {'task_id', 'task_state'}. task_state can have the following value, representing different states of the task:
        0: Free to start
        1: Working
        2: Completed
        
### Get Task Result
The address to get task result is [http://'sever_address'/s2t/[task_id]]. [task_id] is the queued task id of the previous post request:

        BASE = "http://ec530pj4.uk.r.appspot.com/"
        response = requests.get(BASE + "s2t/" + str([task_id]))
        
[response] containse a dictionary with key = {'result'}. [result] is converted text message.
                                                                                        
## Session Examples
The first step is to download the database framework using the module [db_setup.py], the downloaded framework is named [Example_db.db]. The example then sets up a local sever connected to []Example_db.db and open the default python http port :5000, the address of the sever is http://127.0.0.1:5000/
![alt text](https://github.com/lzy2022/S2022_EC530_Project2/raw/main/Images/EX1.PNG)
