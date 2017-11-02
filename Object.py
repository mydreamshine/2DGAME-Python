from pico2d import *


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
        # 위치
        self.x, self.y = pos_x, pos_y

        # 생성 및 활동(객체 처리) 시간
        self.currentTime = get_time()

        # 활동 플래그
        self.idle_state = True # 대기 상태(이동하지 않는 상태)
        self.move_state = False # 이동하는 상태

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

        self.PrevIMAGEs = None # 잔상
        self.draw_Previmages = False # 잔상 플래그

        self.Fade_Out = False # Fade-Out 플래그
        self.Fade_In = False # Fade-in 플래그
        self.Num_opacify = 1.0 # 불투명도

        self.stack_Frame, self.current_Frame = 0.0, 0 # 활동 시간에 따른 프레임 누적, 누적된 프레임에 따른 현재 프레임
        self.count_PrevFrame = 0
        self.frameTime = 0 # 프레임 재생시간
    def __del__(self):
        if len(self.moveimage) > 0: self.moveimage.clear()
        if len(self.idleimage) > 0: self.idleimage.clear()
        if self.PrevIMAGEs != None: del (self.PrevIMAGEs)

    # 이동 이미지 소스 등록 (이미지 경로, 애니메이션 프레임 갯수)
    def Apped_moveimage(self, path_image, count_animated_frames = 1):
        self.moveimage.append(CImage(path_image, count_animated_frames))
        self.moveimage_index = len(self.moveimage) - 1
        self.FRAMES_PER_ACTION_move = count_animated_frames
        self.MoveFrameWidth = self.Size_Width = self.moveimage[-1].property.w
        self.MoveFrameHeight = self.Size_Height = self.moveimage[-1].property.h

    # idle 이미지 소스 등록 (이미지 경로, 애니메이션 프레임 갯수)
    def Apped_idleimage(self, path_image, count_animated_frames = 1):
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

    # 이동속도 지정
    def Set_moveSpeed(self, Speed_x = 0.0, Speed_y = 0.0):
        self.RUN_SPEED_KMPH_x, self.RUN_SPEED_KMPH_y = Speed_x, Speed_y  # 추상적 객체 속도

        # 속도 최저값 조정
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
    def Move(self):
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
        if self.Num_opacify < 0.0: self.Num_opacify = 0.0
        elif self.Num_opacify > 1.0: self.Num_opacify = 1.0

        # 잔상
        if self.draw_Previmages:
            for PrevPoint in range(0, self.count_PrevFrame):
                prevFrame = self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].Frame
                (PrevX, PrevY) = (self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].x, self.PrevIMAGEs[self.count_PrevFrame - (PrevPoint + 1)].y)
                if self.move_state:
                    self.moveimage[self.moveimage_index].property.opacify((PrevPoint + 1.0) / (len(self.PrevIMAGEs) * 2) * self.Num_opacify)
                    self.moveimage[self.moveimage_index].property.clip_draw(prevFrame * self.MoveFrameWidth, 0, self.MoveFrameWidth, self.MoveFrameHeight, PrevX, PrevY, self.Size_Width, self.Size_Height)
                elif self.idle_state:
                    self.idleimage[self.idleimage_index].property.opacify((PrevPoint + 1.0) / (len(self.PrevIMAGEs) * 2) * self.Num_opacify)
                    self.idleimage[self.idleimage_index].property.clip_draw(prevFrame * self.idleFrameWidth, 0, self.idleFrameWidth, self.idleFrameHeight, PrevX, PrevY, self.Size_Width, self.Size_Height)

        # 객체 상태에 따른 이미지
        if self.move_state:
            self.moveimage[self.moveimage_index].property.opacify(self.Num_opacify)
            self.moveimage[self.moveimage_index].property.clip_draw(self.current_Frame * self.MoveFrameWidth, 0, self.MoveFrameWidth, self.MoveFrameHeight, self.x, self.y, self.Size_Width, self.Size_Height)
        elif self.idle_state:
            self.idleimage[self.idleimage_index].property.opacify(self.Num_opacify)
            self.idleimage[self.idleimage_index].property.clip_draw(self.current_Frame * self.idleFrameWidth, 0, self.idleFrameWidth, self.idleFrameHeight, self.x, self.y, self.Size_Width, self.Size_Height)