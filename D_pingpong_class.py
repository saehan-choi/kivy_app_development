import turtle
import time
import random

class PongEnv:
    def __init__(self):
        self.win = turtle.Screen()
        self.win.title("Pong")
        self.win.bgcolor("black")
        self.win.setup(width=600, height=400)
        self.win.tracer(0)

        # 좌측 패들
        self.left_pad = turtle.Turtle()
        self.left_pad.speed(0)
        self.left_pad.shape("square")
        self.left_pad.color("white")
        self.left_pad.shapesize(stretch_wid=5, stretch_len=1)
        self.left_pad.penup()
        self.left_pad.goto(-250, 0)

        # 우측 패들
        self.right_pad = turtle.Turtle()
        self.right_pad.speed(0)
        self.right_pad.shape("square")
        self.right_pad.color("white")
        self.right_pad.shapesize(stretch_wid=5, stretch_len=1)
        self.right_pad.penup()
        self.right_pad.goto(250, 0)

        # 공
        self.ball = turtle.Turtle()
        self.ball.speed(40)
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = 0.1
        self.ball.dy = -0.1

        # 점수판
        self.left_score = 0
        self.right_score = 0
        self.score = turtle.Turtle()
        self.score.speed(0)
        self.score.color("white")
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 170)
        self.score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))

        # 게임루프
        self.win.listen()
        self.win.onkeypress(self.left_pad_up, "w")
        self.win.onkeypress(self.left_pad_down, "s")
        self.win.onkeypress(self.right_pad_up, "Up")
        self.win.onkeypress(self.right_pad_down, "Down")

    # 좌측 패들을 위로 이동
    def left_pad_up(self):
        y = self.left_pad.ycor()
        y += 20
        self.left_pad.sety(y)

    # 좌측 패들을 아래로 이동
    def left_pad_down(self):
        y = self.left_pad.ycor()
        y -= 20
        self.left_pad.sety(y)

    # 우측 패들을 위로 이동
    def right_pad_up(self):
        y = self.right_pad.ycor()
        y += 20
        self.right_pad.sety(y)

    # 우측 패들을 아래로 이동
    def right_pad_down(self):
        y = self.right_pad.ycor()
        y -= 20
        self.right_pad.sety(y)

    # 화면 업데이트
    def update(self):
        
        self.win.update()

    # 게임 종료
    def close(self):
        self.win.bye()

    # 현재 상태 반환
    def get_state(self):
        # 패들과 공의 상대 위치 정보
        left_pad_y = self.left_pad.ycor()
        right_pad_y = self.right_pad.ycor()
        ball_x = self.ball.xcor()
        ball_y = self.ball.ycor()
        ball_dx = self.ball.dx
        ball_dy = self.ball.dy
        
        state = [left_pad_y, right_pad_y, ball_x, ball_y, ball_dx, ball_dy]
        return state

    def step(self, action):
        # 패들 이동
        if action == 0:
            self.left_pad_up()
        elif action == 1:
            self.left_pad_down()
        elif action == 2:
            self.right_pad_up()
        elif action == 3:
            self.right_pad_down()
        
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        # 공이 상단 벽과 충돌했을 때
        if self.ball.ycor() > 190:
            self.ball.sety(190)
            self.ball.dy *= -1

        # 공이 하단 벽과 충돌했을 때
        if self.ball.ycor() < -190:
            self.ball.sety(-190)
            self.ball.dy *= -1
            
        # 공이 우측 벽과 충돌했을 때 (좌측 선수 승리)
        if self.ball.xcor() > 290:
            self.ball.goto(0, 0)
            self.ball.dx *= -1
            self.left_score += 1
            self.score.clear()
            self.score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))

        # 공이 좌측 벽과 충돌했을 때 (우측 선수 승리)
        if self.ball.xcor() < -290:
            self.ball.goto(0, 0)
            self.ball.dx *= -1
            self.right_score += 1
            self.score.clear()
            self.score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))

        # 공이 좌측 패들과 충돌했을 때
        if self.ball.xcor() < -240 and self.ball.ycor() < self.left_pad.ycor() + 50 and self.ball.ycor() > self.left_pad.ycor() - 50:
            self.ball.setx(-240)
            self.ball.dx *= -1

        # 공이 우측 패들과 충돌했을 때
        if self.ball.xcor() > 240 and self.ball.ycor() < self.right_pad.ycor() + 50 and self.ball.ycor() > self.right_pad.ycor() - 50:
            self.ball.setx(240)
            self.ball.dx *= -1

        # 화면 업데이트
        self.update()

        # 현재 게임 상태 반환
        state = self.get_state()

        # 보상 계산
        reward = 0
        if self.ball.xcor() > 240:
            reward = 1
        elif self.ball.xcor() < -240:
            reward = -1

        # 에피소드 종료 여부 반환
        done = (reward != 0)

        return state, reward, done, {}


game = PongEnv()

while True:
    action = random.randint(0,3)
    print(game.step(action))
    game.update()

    # time.sleep(0.01)