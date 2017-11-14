from pygame import mixer

BGM = None
EffectSound = []

NONE, TITLE, STAGE, GAMEOVER = 0, 1, 2, 3

State_BGM = NONE


def Play_BGM():
    global BGM
    if BGM != None: BGM.play()


def Stop_BGM():
    global BGM
    if BGM != None: BGM.stop()


def Delete():
    global NONE
    global State_BGM
    global BGM
    if BGM != None: BGM.stop(); del(BGM); BGM = None
    State_BGM = NONE


def Play_Title():
    global NONE, TITLE, STAGE, GAMEOVER
    global State_BGM
    global BGM
    if State_BGM != TITLE:
        if BGM != None: BGM.stop(); del (BGM); BGM = None
        mixer.init()
        BGM = mixer.Sound('Data\\Sound\\title_bgm.wav')
        BGM.play(-1)
        State_BGM = TITLE


def Play_Stage():
    global NONE, TITLE, STAGE, GAMEOVER
    global State_BGM
    global BGM
    if State_BGM != STAGE:
        if BGM != None: BGM.stop(); del (BGM); BGM = None
        mixer.init()
        BGM = mixer.Sound('Data\\Sound\\stage_bgm.wav')
        BGM.play(-1)
        State_BGM = STAGE


def Play_GameOver():
    global NONE, TITLE, STAGE, GAMEOVER
    global State_BGM
    global BGM
    if State_BGM != GAMEOVER:
        if BGM != None: BGM.stop(); del (BGM); BGM = None
        mixer.init()
        BGM = mixer.Sound('Data\\Sound\\gameover_bgm.wav')
        BGM.play(-1)
        State_BGM = GAMEOVER