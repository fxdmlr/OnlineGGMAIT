import onlineHandler as oh
import os
import inputs
import json
import requests
import screens
import random
import time

url = 'https://guardts.ir/api/pastes'

def main(init_addr):
    rounds = int(inputs.game_settings['rounds'])
    game_func = inputs.GAMES[inputs.game_settings['game']]
    usr1_score = 0
    usr2_score = 0
    finish_addr = oh.generate_random_sequence(10)
    
    r_usr1_name = requests.get(url + "/" + init_addr + "_usr1_name")
    usr_1_name_flag = False
    if r_usr1_name.status_code == 200:
        usr_1_name = oh.read_addr(init_addr + "_usr1_name")
        print("%s has joined the room!"%usr_1_name)
        usr_1_name_flag = True
        
    r_usr2_name = requests.get(url + "/" + init_addr + "_usr2_name")
    usr_2_name_flag = False
    if r_usr2_name.status_code == 200:
        usr_2_name = oh.read_addr(init_addr + "_usr2_name")
        print("%s has joined the room!"%usr_2_name)
        usr_2_name_flag = True
        
    while r_usr1_name.status_code != 200 or r_usr2_name.status_code != 200:
        r_usr1_name = requests.get(url + "/" + init_addr + "_usr1_name")
        if r_usr1_name.status_code == 200 and not usr_1_name_flag:
            usr_1_name = oh.read_addr(init_addr + "_usr1_name")
            print("%s has joined the room!"%usr_1_name)
            usr_1_name_flag = True
            
        r_usr2_name = requests.get(url + "/" + init_addr + "_usr2_name")

        if r_usr2_name.status_code == 200 and not usr_2_name_flag:
            usr_2_name = oh.read_addr(init_addr + "_usr2_name")
            print("%s has joined the room!"%usr_2_name)
            usr_2_name_flag = True
        
        time.sleep(0.1)
    
    usr_1_name = oh.read_addr(init_addr + "_usr1_name")
    usr_2_name = oh.read_addr(init_addr + "_usr2_name")
    curr_addr = init_addr
    for i in range(rounds):
        judgment = ""
        question, answer = game_func(inputs.inpt_dict)
        usr1 = oh.generate_random_sequence(10)
        usr2 = oh.generate_random_sequence(10)
        next_addr = oh.generate_random_sequence(10)
        if i == rounds - 1:
            next_addr = finish_addr
        sub_dict = {"question" : question, "answer" : answer, "usr1": usr1, "usr2":usr2, "next":next_addr, "fin_addr":finish_addr, "usr1name":usr_1_name, "usr2name":usr_2_name}
        sub_dict.update({"inpt_dict" : inputs.inpt_dict, "game_settings" : inputs.game_settings})
        string = json.dumps(sub_dict)
        
        oh.create_new_file(string, curr_addr)
        
        r1, r2 = requests.get(url + "/" + usr1), requests.get(url + "/" + usr2)
        while not (r1.status_code == 200 and r2.status_code == 200):
            r1, r2 = requests.get(url + "/" + usr1), requests.get(url + "/" + usr2)
            time.sleep(0.1)
        
        r1_res, r2_res = json.loads(json.loads(r1.text)["content"]), json.loads(json.loads(r2.text)["content"])
        if float(r1_res["input"]) == float(answer) and float(r2_res["input"]) != float(answer):
            usr1_score += 1
            judgment = "point to %s"%usr_1_name
        elif float(r1_res["input"]) != float(answer) and float(r2_res["input"]) == float(answer):
            usr2_score += 1
            judgment = "point to %s"%usr_2_name
        elif  float(r1_res["input"]) == float(answer) and float(r2_res["input"]) == float(answer):
            t1, t2 = r1_res["time"], r2_res["time"]
            if t1 < t2:
                usr1_score += 1
                judgment = "point to %s"%usr_1_name
            elif t1 > t2:
                usr2_score += 1
                judgment = "point to %s"%usr_2_name
            else:
                usr_1_score += 0.5
                usr_2_score += 0.5
                judgment = "half a point to both players."
        
        oh.create_new_file(judgment, curr_addr + "_judgement")   
        
        curr_addr = next_addr
    
    result = "DRAW"
    if usr1_score > usr2_score:
        result = "%s wins"%usr_1_name
    elif usr1_score < usr2_score:
        result = "%s wins"%usr_2_name
    
    stat_dict = {"usr1" : usr1_score, "usr2" : usr2_score, "result":result}
    oh.create_new_file(json.dumps(stat_dict), finish_addr)
    return
    
        
def main_usr():
    game_addr = oh.generate_random_sequence(10)
    print("Your game address is %s"%game_addr)
    print("".join(["_" for i in "Your game address is %s"%game_addr]))
    
    n = screens.menu_screen() - 1
    inputs.inpt_dict = {}
    inputs.game_settings = {'game' : n}
    for prompt, key in inputs.GAME_SETTING_PARAMS[0]:
        val = input(prompt + " : ")
        inputs.game_settings.update({key : val})
        
    for prompt, key in inputs.GAME_PARAMS[n]:
        val = input(prompt + " : ")
        inputs.inpt_dict.update({key : val})
    
    
    
    
    if int(inputs.game_settings['mode']) == 1:
        main(game_addr)
    
while True:
    main_usr()
    print()