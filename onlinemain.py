import onlineHandler as oh
import os
import inputs
import json
import requests
import screens
import random

url = 'https://guardts.ir/api/pastes'

def main(init_addr):
    rounds = int(inputs.game_settings['rounds'])
    game_func = inputs.GAMES[inputs.game_settings['game']]
    usr1_score = 0
    usr2_score = 0
    finish_addr = oh.generate_random_sequence(10)
    usr_1_name = oh.read_addr(init_addr + "_usr1_name")
    usr_2_name = oh.read_addr(init_addr + "_usr2_name")
    curr_addr = init_addr
    for i in range(rounds):
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
        
        r1_res, r2_res = json.loads(json.loads(r1.text)["content"]), json.loads(json.loads(r2.text)["content"])
        if r1_res["input"] == answer and r2_res["input"] != answer:
            usr1_score += 1
        elif r1_res["input"] != answer and r2_res["input"] == answer:
            usr2_score += 1
        elif  r1_res["input"] == answer and r2_res["input"] == answer:
            t1, t2 = r1_res["time"], r2_res["time"]
            if t1 < t2:
                usr1_score += 1
            elif t1 > t2:
                usr2_score += 1
            else:
                usr_1_score += 0.5
                usr_2_score += 0.5
                
        
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