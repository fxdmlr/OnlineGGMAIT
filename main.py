import gamerunner as gr
import screens
import inputs

def main():
    n = screens.menu_screen() - 1
    game = inputs.GAMES[n]
    inputs.inpt_dict = {}
    inputs.game_settings = {'game' : game}
    for prompt, key in inputs.GAME_SETTING_PARAMS[0]:
        val = input(prompt + " : ")
        inputs.game_settings.update({key : val})
        
    for prompt, key in inputs.GAME_PARAMS[n]:
        val = input(prompt + " : ")
        inputs.inpt_dict.update({key : val})
    
    if int(inputs.game_settings['mode']) == 1:
        gr.static_runner()
    
while True:
    main()
    