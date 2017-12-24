from pico2d import *
import Object

COLLSION_FRICTION = 0.5 # 탄성 계수


class Rect:
    def __init__(self, LEFT = 0.0, TOP = 0.0, RIGHT = 0.0, BOTTOM = 0.0):
        self.left, self.top, self.right, self.bottom = LEFT, TOP, RIGHT, BOTTOM


# 교차 영역(사각형)
def intersectRect_s(intersect, Rect1, Rect2):
    VCollision = False
    HCollision = False

    # 수평 충돌
    if Rect1.left < Rect2.right and Rect1.right > Rect2.left:
        HCollision = True
        intersect.left = max(Rect1.left, Rect2.left)
        intersect.right = min(Rect1.right, Rect2.right)
    # 수직 충돌
    if Rect1.top > Rect2.bottom and Rect1.bottom < Rect2.top:
        VCollision = True
        intersect.top = min(Rect1.top, Rect2.top)
        intersect.bottom = max(Rect1.bottom, Rect2.bottom)

    return VCollision and HCollision


# 교차 영역(사각형)
def intersectRect(intersect, Object1, Object2):
    VCollision = False
    HCollision = False

    # 수평 충돌
    if Object1.Left() < Object2.Right() and Object1.Right() > Object2.Left():
        HCollision = True
        intersect.left = max(Object1.Left(), Object2.Left())
        intersect.right = min(Object1.Right(), Object2.Right())
    # 수직 충돌
    if Object1.Top() > Object2.Bottom() and Object1.Bottom() < Object2.Top():
        VCollision = True
        intersect.top = min(Object1.Top(), Object2.Top())
        intersect.bottom = max(Object1.Bottom(), Object2.Bottom())

    return VCollision and HCollision

# 충돌처리(사각형)
def Collision_MoveWithHold(Moved_Object, Hold_Object):
    global COLLSION_FRICTION
    intersect = Rect()

    if intersectRect(intersect, Moved_Object, Hold_Object):
        # 교차 영역 크기
        nInterWidth = abs(intersect.right - intersect.left)
        nInterHeight = abs(intersect.top - intersect.bottom)

        #위아래 체크
        if(nInterWidth > nInterHeight):
            if intersect.top == Hold_Object.Top():
                Moved_Object.y += nInterHeight
            elif intersect.bottom == Hold_Object.Bottom():
                Moved_Object.y -= nInterHeight

            #탄성 처리
            Moved_Object.RUN_SPEED_KMPH_y *= -COLLSION_FRICTION
            Moved_Object.Set_moveSpeed(Moved_Object.RUN_SPEED_KMPH_x, Moved_Object.RUN_SPEED_KMPH_y)

            #점프 플래그 초기화
            Moved_Object.JUMP = False
            Moved_Object.DOUBLEJUMP = False
        #좌우 체크
        else:
            if intersect.left == Hold_Object.Left():
                Moved_Object.x -= nInterWidth
            elif intersect.right == Hold_Object.Right():
                Moved_Object.x += nInterWidth
            # 탄성 처리
            Moved_Object.RUN_SPEED_KMPH_x *= -COLLSION_FRICTION
            Moved_Object.Set_moveSpeed(Moved_Object.RUN_SPEED_KMPH_x, Moved_Object.RUN_SPEED_KMPH_y)
        del (intersect); return True
    else: del(intersect); return False


# 충돌처리(캔버스)
def Collsion_WndBoundary(Move_Object, Canvas_Boundary):
    global COLLSION_FRICTION
    if Move_Object.Left() < Canvas_Boundary.left:
        Move_Object.x += Canvas_Boundary.left - Move_Object.Left()
        # 탄성 처리
        Move_Object.RUN_SPEED_KMPH_x *= -COLLSION_FRICTION
        Move_Object.Set_moveSpeed(Move_Object.RUN_SPEED_KMPH_x, Move_Object.RUN_SPEED_KMPH_y)
        return True
    if Move_Object.Top() > Canvas_Boundary.top:
        Move_Object.y -= Move_Object.Top() - Canvas_Boundary.top
        # 탄성 처리
        Move_Object.RUN_SPEED_KMPH_y *= -COLLSION_FRICTION
        Move_Object.Set_moveSpeed(Move_Object.RUN_SPEED_KMPH_x, Move_Object.RUN_SPEED_KMPH_y)
        return True
    if Move_Object.Right() > Canvas_Boundary.right:
        Move_Object.x -= Move_Object.Right() - Canvas_Boundary.right
        # 탄성 처리
        Move_Object.RUN_SPEED_KMPH_x *= -COLLSION_FRICTION
        Move_Object.Set_moveSpeed(Move_Object.RUN_SPEED_KMPH_x, Move_Object.RUN_SPEED_KMPH_y)
        return True
    if Move_Object.Bottom() < Canvas_Boundary.bottom:
        Move_Object.y += Canvas_Boundary.bottom - Move_Object.Bottom()
        # 탄성 처리
        Move_Object.RUN_SPEED_KMPH_y *= -COLLSION_FRICTION
        Move_Object.Set_moveSpeed(Move_Object.RUN_SPEED_KMPH_x, Move_Object.RUN_SPEED_KMPH_y)
        # 점프 플래그 초기화
        Move_Object.JUMP = False
        Move_Object.DOUBLEJUMP = False
        return True