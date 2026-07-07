import onlineHandler as oh
import os
import inputs
import json
import requests
import random
import time

url = 'https://guardts.ir/api/pastes'


def main(init_addr, name):
    r = oh.create_new_file(name, init_addr+"_usr1_name")
    if r.status_code != 200:
        r = oh.create_new_file(name, init_addr+"_usr2_name")
    
    curr_addr = init_addr
    r = requests.get(url + "/" + curr_addr)
    while r.status_code != 200:
        r = requests.get(url + "/" + curr_addr)
    game_dict = json.loads(oh.read_addr(curr_addr))
    rounds = int(game_dict["game_settings"]['rounds'])
    game_func = inputs.GAMES[game_dict["game_settings"]['game']]
    question, answer, usr1, usr2, next_addr, fin_addr = game_dict["question"], game_dict["answer"], game_dict["usr1"], game_dict["usr2"], game_dict["next"], game_dict["fin_addr"]
    usr_1_name = game_dict["usr1name"]
    usr_2_name = game_dict["usr2name"]
    
    me = "usr1" if name == usr_1_name else "usr2"
    st = time.time()
    usr_inp = input(question)
    end = time.time()
    oh.create_new_file(json.dumps({"input" : usr_inp, "time" : end-st}), game_dict[me])
    if usr_inp == answer:
        print("Correct.")
    else:
        print("Incorrect. The answer was %s"%answer)
    
    print("Input took %d seconds"%(round((end - st))))  
    
    
    while requests.get(url + "/" + next_addr).status_code != 200:
        time.sleep(0.1)
    
    while requests.get(url + "/" + curr_addr + "_judgement").status_code != 200:
            time.sleep(0.1) 
        
    judgment = oh.read_addr(curr_addr + "_judgement")
    print(judgment)  
    curr_addr = next_addr
    for i in range(rounds - 1):
        r = requests.get(url + "/" + curr_addr)
        while r.status_code != 200:
            r = requests.get(url + "/" + curr_addr)
        game_dict = json.loads(oh.read_addr(curr_addr))
        rounds = int(game_dict["game_settings"]['rounds'])
        game_func = inputs.GAMES[game_dict["game_settings"]['game']]
        question, answer, usr1, usr2, next_addr, fin_addr = game_dict["question"], game_dict["answer"], game_dict["usr1"], game_dict["usr2"], game_dict["next"], game_dict["fin_addr"]
        usr_1_name = game_dict["usr1name"]
        usr_2_name = game_dict["usr2name"]
        
        me = "usr1" if name == usr_1_name else "usr2"
        
        st = time.time()
        usr_inp = input(question)
        end = time.time()
        oh.create_new_file(json.dumps({"input" : usr_inp, "time" : time.time()}), game_dict[me])
        if float(usr_inp) == float(answer):
            print("Correct.")
        else:
            print("Incorrect. The answer was %s"%answer)
        
        print("Input took %d seconds"%(round((end - st)))) 
        
        
        while requests.get(url + "/" + next_addr).status_code != 200:
            time.sleep(0.1)
        
        while requests.get(url + "/" + curr_addr + "_judgement").status_code != 200:
            pass
        
        judgment = oh.read_addr(curr_addr + "_judgement")
        print(judgment)
        curr_addr = next_addr
    
    time.sleep(1)
    res_dict = json.loads(oh.read_addr(fin_addr))
    print("%s score : %d"%(usr_1_name, res_dict["usr1"]))
    print("%s score : %d"%(usr_2_name, res_dict["usr2"]))
    print(res_dict["result"])

game_addr = input("Enter the game addr : ")
name = input("Enter your name : ")

main(game_addr, name)