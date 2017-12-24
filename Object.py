from pico2d import *
import json
import Phisics
import CollisionCheck

Canvas_SIZE = None
Ground_Size = None

fade = None
fade_dark = None
character = None
ObjectList = None
info_list = None


class info:
    def __init__(self):
        self.name = None
        self.x, self.y = 0.0, 0.0
        self.image = None
        self.row, self.col= 1, 1
        self.left, self.bottom = 0, 0
        self.jumpWidth, self.jumpHeight = 0, 0
        self.width, self.height = 0, 0

    def __del__(self):
        if self.name != None: del(self.name)
        if self.image != None: del(self.image)

    def draw(self):
        self.image.clip_draw(self.left + self.jumpWidth * (self.col - 1) if self.col > 0 else 0,
                             self.bottom + self.jumpHeight * (self.row - 1) if self.row > 0 else 0,
                             self.width, self.height, self.x, self.y)


class CImage:
    def __init__(self, image_path = None, frames = 0):
        self.property = load_image(image_path)
        self.FRAMES_PER_ACTION = frames


class CFrame:
    def __init__(self):
        self.x, self.y = 0, 0
        self.Frame = 0


class CObject:

    PIXEL_PER_METER = 10.0 / 0.3  # 속도단위에 따른 상대적 객체 속도 (10픽셀당 30cm)
    FADE_SPEED = 1.1

    def __init__(self, pos_x = 0.0, pos_y = 0.0):
        # 이름
        self.name = None

        # 위치
        self.x, self.y = pos_x, pos_y

        # 활동 영역
        self.GroundField = CollisionCheck.Rect()

        # 생성 및 활동(객체 처리) 시간
        self.currentTime = get_time()

        # 활동 플래그
        self.idle_state = True # 대기 상태(이동하지 않는 상태)
        self.move_state = False # 이동하는 상태
        self.nonFriction = False # 비마찰 운동
        self.AffectedGravity = False # 중력장 간섭 플래그
        self.Accel_left_state = False # 왼쪽으로 가속중인 상태
        self.Accel_right_state = False  # 오른쪽으로 가속중인 상태
        # 점프 플래그
        self.JUMP = False
        self.DOUBLEJUMP = False

        # 이동 및 프레임 재생 속도
        self.RUN_SPEED_KMPH_x, self.RUN_SPEED_KMPH_y = 0.0, 0.0 # 추상적 객체 속도
        self.RUN_SPEED_PPS_x = (self.RUN_SPEED_KMPH_x * 1000.0 / 3600.0) * self.PIXEL_PER_METER # 실제 객체 속도
        self.RUN_SPEED_PPS_y = (self.RUN_SPEED_KMPH_y * 1000.0 / 3600.0) * self.PIXEL_PER_METER  # 실제 객체 속도

        # 이동 및 프레임 재생 시간
        self.TIME_PER_ACTION = 1.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION_move = 0
        self.FRAMES_PER_ACTION_idle = 0

        # 오브젝트 이미지 소스 설정
        self.moveimage_index = 0 # 이동 이미지 종류 인덱스
        self.idleimage_index = 0 # idle 이미지 종류 인덱스
        self.moveimage = [] # 이동 이미지 소스
        self.idleimage = []  # idle 이미지 소스
        self.Size_Width = 0 # 오브젝트 가로크기
        self.Size_Height = 0  # 오브젝트 세로크기
        self.MoveFrameWidth = 0 # 이동 이미지 프레임 가로크기
        self.MoveFrameHeight = 0  # 이동 이미지 프레임 세로크기
        self.idleFrameWidth = 0 # idle 이미지 프레임 가로크기
        self.idleFrameHeight = 0  # idle 이미지 프레임 세로크기
        self.SlideRapping = True # 슬라이드 랩핑 애니메이션 플래그

        self.PrevIMAGEs = None # 잔상
        self.draw_Previmages = False # 잔상 플래그

        self.Fade_Out = False # Fade-Out 플래그
        self.Fade_In = False # Fade-in 플래그
        self.Num_opacify = 1.0 # 불투명도

        self.stack_Frame, self.current_Frame = 0.0, 0 # 활동 시간에 따른 프레임 누적, 누적된 프레임에 따른 현재 프레임
        self.count_PrevFrame = 0
        self.frameTime = 0 # 프레임 재생시간

    def __del__(self):
        while len(self.moveimage) > 0: self.moveimage.pop()
        while len(self.idleimage) > 0: self.idleimage.pop()
        if self.PrevIMAGEs != None: del (self.PrevIMAGEs)
        if self.name != None: del (self.name)
        if self.GroundField != None: del(self.GroundField)

    # 이동 이미지 소스 등록 (이미지 경로, 애니메이션 프레임 갯수)
    def Append_moveimage(self, path_image, count_animated_frames = 1):
        self.moveimage.append(CImage(path_image, count_animated_frames))
        self.moveimage_index = len(self.moveimage) - 1
        self.FRAMES_PER_ACTION_move = count_animated_frames
        self.MoveFrameWidth = self.Size_Width = self.moveimage[-1].property.w
        self.MoveFrameHeight = self.Size_Height = self.moveimage[-1].property.h

    # idle 이미지 소스 등록 (이미지 경로, 애니메이션 프레임 갯수)
    def Append_idleimage(self, path_image, count_animated_frames = 1):
        self.idleimage.append(CImage(path_image, count_animated_frames))
        self.idleimage_index = len(self.idleimage) - 1
        self.FRAMES_PER_ACTION_idle = count_animated_frames
        self.idleFrameWidth = self.Size_Width = self.idleimage[-1].property.w
        self.idleFrameHeight = self.Size_Height = self.idleimage[-1].property.h

     # 그려질 이동 이미지 종류 설정
    def Set_moveFrames(self, index):
        self.moveimage_index = index
        self.FRAMES_PER_ACTION_move = self.moveimage[index].FRAMES_PER_ACTION
        self.MoveFrameWidth = self.Size_Width = self.moveimage[index].property.w
        self.MoveFrameHeight = self.Size_Height = self.moveimage[index].property.h
        self.stack_Frame = 0
        self.current_Frame = 0
        self.count_PrevFrame = 0

     # 그려질 idle 이미지 종류 설정
    def Set_idleFrames(self, index):
        self.idleimage_index = index
        self.FRAMES_PER_ACTION = self.idleimage[index].FRAMES_PER_ACTION
        self.idleFrameWidth = self.Size_Width = self.idleimage[index].property.w
        self.idleFrameHeight = self.Size_Height = self.idleimage[index].property.h
        self.stack_Frame = 0
        self.current_Frame = 0
        self.count_PrevFrame = 0

    # 잔상 그리기
    def Draw_PrevImages(self, Flag = False, count_previmage = 0):
        if Flag and self.PrevIMAGEs == None:
            self.PrevIMAGEs = [CFrame() for i in range(count_previmage)]
        self.draw_Previmages = Flag
        self.count_PrevFrame = 0

    # 위치 지정
    def Set_Pos(self, x = 0.0, y = 0.0):
        self.x, self.y = x, y

    def Set_GroundField(self, RectField):
        self.GroundField.left, self.GroundField.top, self.GroundField.right, self.GroundField.bottom = RectField.left, RectField.top, RectField.right, RectField.bottom

    # 이동속도 지정
    def Set_moveSpeed(self, Speed_x = 0.0, Speed_y = 0.0):
        self.RUN_SPEED_KMPH_x, self.RUN_SPEED_KMPH_y = Speed_x, Speed_y  # 추상적 객체 속도

        # 속도 최저값 조정
        round(self.RUN_SPEED_PPS_x, 4)
        round(self.RUN_SPEED_PPS_y, 4)
        self.RUN_SPEED_KMPH_x = 0.0 if abs(self.RUN_SPEED_KMPH_x) < 0.001 else self.RUN_SPEED_KMPH_x
        self.RUN_SPEED_KMPH_y = 0.0 if abs(self.RUN_SPEED_KMPH_y) < 0.001 else self.RUN_SPEED_KMPH_y

        # 객체속도 지정
        self.RUN_SPEED_PPS_x = (self.RUN_SPEED_KMPH_x * 1000.0 / 3600.0) * self.PIXEL_PER_METER  # 실제 객체 속도
        self.RUN_SPEED_PPS_y = (self.RUN_SPEED_KMPH_y * 1000.0 / 3600.0) * self.PIXEL_PER_METER  # 실제 객체 속도

        #움직임 상태 플래그 결정
        if self.RUN_SPEED_PPS_x == 0.0 and self.RUN_SPEED_PPS_y == 0.0 and self.move_state == True:
            self.move_state = False
            self.idle_state = True
            self.stack_Frame = 0
            self.current_Frame = 0
            self.count_PrevFrame = 0
        elif (self.RUN_SPEED_PPS_x != 0.0 or self.RUN_SPEED_PPS_y != 0.0) and self.move_state == False:
            self.move_state = True
            self.idle_state = False
            self.stack_Frame = 0
            self.current_Frame = 0
            self.count_PrevFrame = 0

    # 애니메이션 속도(프레임 재생속도) 지정
    def Set_frameSpeed(self, Speed = 1.0):
        self.TIME_PER_ACTION = Speed
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

    # 객체 활동주기 측정
    def Set_ActiveTime(self):
        self.frameTime = get_time() - self.currentTime
        self.currentTime += self.frameTime

    # 지정된 이동속도에 따라 이동
    def Move(self, FrictionFactor = 1.0):
        if self.Accel_left_state: # 왼쪽으로 가속
            Phisics.Apply_Accelaration_X(self, -1)
        elif self.Accel_right_state: # 오른쪽으로 가속
            Phisics.Apply_Accelaration_X(self, 1)
        elif not self.nonFriction:
            Phisics.Apply_Friction_X(self, FrictionFactor)  # 이동속도 감속

        distance_x = self.RUN_SPEED_PPS_x * self.frameTime
        distance_y = self.RUN_SPEED_PPS_y * self.frameTime

        if self.PrevIMAGEs != None:
            self.count_PrevFrame += 1 if self.count_PrevFrame < len(self.PrevIMAGEs) else 0
            p_index = self.count_PrevFrame - 1  # 제일 마지막에 기록된 point부터 거꾸로 좌표값 교환
            while p_index > 0:
                self.PrevIMAGEs[p_index].Frame = self.PrevIMAGEs[p_index - 1].Frame
                self.PrevIMAGEs[p_index].x = self.PrevIMAGEs[p_index - 1].x
                self.PrevIMAGEs[p_index].y = self.PrevIMAGEs[p_index - 1].y
                p_index -= 1

            self.PrevIMAGEs[0].Frame = self.current_Frame - 1 if self.current_Frame > 0 else 0
            self.PrevIMAGEs[0].x = self.x
            self.PrevIMAGEs[0].y = self.y

        self.x += distance_x
        self.y += distance_y

        # 객체 활동주기 지정
        self.Set_ActiveTime()

    # 크기 지정
    def Size(self, w, h):
        self.Size_Width, self.Size_Height = w, h

    # 오브젝트의 Boundary 위치
    def Left(self):
        return self.x - self.Size_Width / 2
    def Top(self):
        return self.y + self.Size_Height / 2
    def Right(self):
        return self.x + self.Size_Width / 2
    def Bottom(self):
        return self.y - self.Size_Height / 2

    def Scale(self, valScale = 1.0):
        self.Size_Width = (self.MoveFrameWidth if self.move_state else self.idleFrameWidth) * valScale
        self.Size_Height = (self.MoveFrameHeight if self.move_state else self.idleFrameHeight) * valScale

    def Active_Fade_Out(self):
        self.Fade_Out = True
        self.Fade_In = False

    def Active_Fade_In(self):
        self.Fade_Out = False
        self.Fade_In = True

    # 프레임에 따라 그리기
    def draw(self):
        # 프레임 결정
        self.stack_Frame += (self.FRAMES_PER_ACTION_move if self.move_state else self.FRAMES_PER_ACTION_idle)  * self.ACTION_PER_TIME * self.frameTime
        self.current_Frame = int(self.stack_Frame) % (self.FRAMES_PER_ACTION_move if self.move_state else self.FRAMES_PER_ACTION_idle)

        # Fade 효과
        if self.Fade_Out and self.Num_opacify > 0.0:
            self.Num_opacify -= self.FADE_SPEED * self.frameTime
        elif self.Fade_In and self.Num_opacify < 1.0:
            self.Num_opacify += self.FADE_SPEED * self.frameTime
        if self.Num_opacify < 0.0: self.Num_opacify = 0.0; self.Fade_Out = False
        elif self.Num_opacify > 1.0: self.Num_opacify = 1.0; self.Fade_In = False

        # 잔상
        if self.draw_Previmages:
            for PrevPoint in range(0, self.count_PrevFrame):
                prevFrame = self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].Frame
                (PrevX, PrevY) = (self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].x, self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].y)
                if self.move_state:
                    self.moveimage[self.moveimage_index].property.opacify((PrevPoint + 1.0) / (len(self.PrevIMAGEs) * 3) * self.Num_opacify)
                    self.moveimage[self.moveimage_index].property.clip_draw(prevFrame * self.MoveFrameWidth, 0, self.MoveFrameWidth, self.MoveFrameHeight, PrevX, PrevY, self.Size_Width, self.Size_Height)
                elif self.idle_state:
                    self.idleimage[self.idleimage_index].property.opacify((PrevPoint + 1.0) / (len(self.PrevIMAGEs) * 3) * self.Num_opacify)
                    self.idleimage[self.idleimage_index].property.clip_draw(prevFrame * self.idleFrameWidth, 0, self.idleFrameWidth, self.idleFrameHeight, PrevX, PrevY, self.Size_Width, self.Size_Height)

        # 객체 상태에 따른 이미지
        if self.move_state:
            self.moveimage[self.moveimage_index].property.opacify(self.Num_opacify)
            self.moveimage[self.moveimage_index].property.clip_draw(\
                self.current_Frame * self.MoveFrameWidth, 0,\
                self.MoveFrameWidth, self.MoveFrameHeight,\
                self.x, self.y, self.Size_Width, self.Size_Height)
        elif self.idle_state:
            self.idleimage[self.idleimage_index].property.opacify(self.Num_opacify)
            self.idleimage[self.idleimage_index].property.clip_draw(\
                self.current_Frame * self.idleFrameWidth, 0,\
                self.idleFrameWidth, self.idleFrameHeight,\
                self.x, self.y, self.Size_Width, self.Size_Height)

    def handle_events(self, event):
        # 캐릭터 잔상 On/Off
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            if self.draw_Previmages: self.Draw_PrevImages(False)
            else: self.Draw_PrevImages(True)

        # 캐릭터 물리(가속, 관성, 탄성, 중력)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):  # 캐릭터 오른쪽으로 가속
            self.Accel_right_state = True
            self.Accel_left_state = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):  # 캐릭터 왼쪽으로 가속
            self.Accel_right_state = False
            self.Accel_left_state = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            self.Accel_left_state = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.Accel_right_state = False

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):  # 캐릭터 점프
            if not self.JUMP or not self.DOUBLEJUMP:
                Phisics.Apply_Jump(self)
                self.DOUBLEJUMP = True if self.JUMP else False
                self.JUMP = True


   # 파일포맷에 따른 오브젝트 생성↓

def create_infoFrom(file_path):
    info_file = open(file_path, 'r')
    info_dic = json.load(info_file)
    info_file.close()

    info_list_source = []
    for name in info_dic:
        info_object = info()
        info_object.name = name

        info_object.image = load_image(info_dic[name]['ImagePath'])
        info_object.left = info_dic[name]['left']
        info_object.bottom = info_dic[name]['bottom']
        info_object.width = info_dic[name]['width']
        info_object.height = info_dic[name]['height']
        info_object.jumpWidth = info_dic[name]['jumpWidth']
        info_object.jumpHeight = info_dic[name]['jumpHeight']
        info_object.row = info_dic[name]['row']
        info_object.col = info_dic[name]['col']
        info_object.x = info_dic[name]['x']
        info_object.y = info_dic[name]['y']

        info_list_source.append(info_object)

    return info_list_source


def create_ObjectsFrom(file_path):
    global fade, fade_dark, character, Canvas_SIZE
    Objects_file = open(file_path, 'r')

    Objects_dic = json.load(Objects_file)
    Objects_file.close()

    Object_list_source = {}
    for name in Objects_dic:
        Object_source = CObject()
        Object_source.name = name
        Object_source.Append_idleimage(Objects_dic[name]['ImagePath'])
        Object_source.Append_moveimage(Objects_dic[name]['ImagePath'])
        Object_source.Set_Pos(Objects_dic[name]['x'], Objects_dic[name]['y'])
        Object_source.nonFriction = True if Objects_dic[name]['nonFriction'] == 1 else False
        Object_source.AffectedGravity = True if Objects_dic[name]['AffectedGravity'] == 1 else False
        if Objects_dic[name]['ActiveFadeOut'] == 1:
            Object_source.Active_Fade_Out()
        if Objects_dic[name]['ActiveFadeIn'] == 1:
            Object_source.Num_opacify = 0.0
            Object_source.Active_Fade_In()
        Object_source.Num_opacify = Objects_dic[name]['Opacify']
        if Objects_dic[name]['DrawPrevImage'] == 1:
            Object_source.Draw_PrevImages(True, Objects_dic[name]['nPrevImage'])

        if Object_source.name == "fade":
            fade = Object_source
        elif Object_source.name == "fade_dark":
            fade_dark = Object_source
            fade_dark.x = Canvas_SIZE.right
            fade_dark.Size_Width = 0
        elif Object_source.name == "character":
            character = Object_source
            character.JUMP = character.DOUBLEJUMP = True
        else:
            Object_list_source[name] = Object_source

    return Object_list_source


def DeleteObjects():
    global fade, fade_dark, character, ObjectList, ThornList, info_list
    if fade != None: del (fade); fade = None
    if fade_dark != None: del (fade_dark); fade_dark = None
    if character != None: del (character); character = None
    if ObjectList != None:
        ObjectList.clear()
        ObjectList = None
    if info_list != None:
        while len(info_list) > 0: info_list.pop()
        info_list = None

def DeleteCanvas():
    global Canvas_SIZE, Ground_Size
    if Canvas_SIZE != None: del (Canvas_SIZE); Canvas_SIZE = None
    if Ground_Size != None: del (Ground_Size); Ground_Size = None
