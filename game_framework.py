class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw



class TestGameState:

    def __init__(self, name):
        self.name = name

    def enter(self):
        print("State [%s] Entered" % self.name)

    def exit(self):
        print("State [%s] Exited" % self.name)

    def pause(self):
        print("State [%s] Paused" % self.name)

    def resume(self):
        print("State [%s] Resumed" % self.name)

    def handle_events(self):
        print("State [%s] handle_events" % self.name)

    def update(self):
        print("State [%s] update" % self.name)

    def draw(self):
        print("State [%s] draw" % self.name)



running = None
stack = None


def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()



def push_state(state):
    global stack
    if (len(stack) > 0):
        # stack의 top의 pause()를 호출하고
        stack[-1].pause()
    # stack에 새로운 state를 추가하고
    stack.append(state)
    # stack에 새롭게 들어온 state의 enter()를 호출한다.
    state.enter()



def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()



def quit():
    global running
    running = False

# 현재 프레임에 진입하면 enter()를 호출하고
# 현재 프레임에서 나가면 exit()을 호출.
# 리스트 : 중복을 허용하는 자료들의 집합, 임의의 위치에 삽입, 삭제가 이루어진다.
# 스택 : 중복을 허용하는 자료들의 집합, 삽입, 삭제의 위치가 정해져 있다.
def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    while (running):
        # stack[-1] : stack top pointer
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()


def test_game_framework():
    start_state = TestGameState('StartState')
    run(start_state)



if __name__ == '__main__':
    test_game_framework()