import console_utils as cu
import inputs
import time
import os

def static_runner():
    score = 0
    times = 0
    os.system('clear')
    rounds = int(inputs.game_settings['rounds'])
    game_func = inputs.game_settings['game']
    
    for i in range(rounds):
        res, duration, answer = game_func(inputs.inpt_dict, i + 1)
        if answer == 'restart':
            return static_runner()
        
        times += duration
        if res:
            score += 1
            print('Correct. Input took %ds.'%round(duration))
        
        else:
            print('Incorrect. The answer was %s.\nInput took %ds.' % (str(answer), round(duration)))
        
    
    score_string = 'You scored %d/%d or %d percent.'%(score, rounds, round(100 * score / rounds))
    time_string = 'You took, on average, %d seconds per item.'%round(times/rounds)
    exit_string = 'Press Enter to continue...'
    
    print(score_string)
    print(time_string)
    print(exit_string)
    z = input()

