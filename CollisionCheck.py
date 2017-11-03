from pico2d import *
import Object

COLLSION_FRICTION = 0.3 # 탄성 계수


class Rect:
    def __init__(self, LEFT = 0.0, TOP = 0.0, RIGHT = 0.0, BOTTOM = 0.0):
        self.left, self.top, self.right, self.bottom = LEFT, TOP, RIGHT, BOTTOM

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
    if Move_Object.Left() < Canvas_Boundary.left:
        Move_Object.x += Canvas_Boundary.left - Move_Object.Left()
        return True
    if Move_Object.Top() > Canvas_Boundary.top:
        Move_Object.y -= Move_Object.Top() - Canvas_Boundary.top
        return True
    if Move_Object.Right() > Canvas_Boundary.right:
        Move_Object.x -= Move_Object.Right() - Canvas_Boundary.right
        return True
    if Move_Object.Bottom() < Canvas_Boundary.bottom:
        Move_Object.y += Canvas_Boundary.bottom - Move_Object.Bottom()
        return True