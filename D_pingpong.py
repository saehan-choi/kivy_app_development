import random
import turtle

# 게임화면 초기화
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=600, height=400)
win.tracer(0)

# 좌측 패들
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=5, stretch_len=1)
left_pad.penup()
left_pad.goto(-250, 0)

# 우측 패들
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=5, stretch_len=1)
right_pad.penup()
right_pad.goto(250, 0)

# 공
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = -0.1

# 점수판
left_score = 0
right_score = 0
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 170)
score.write("Player 1: {}  Player 2: {}".format(left_score, right_score), align="center", font=("Courier", 16, "normal"))


# 좌측 패들을 위로 이동
def left_pad_up():
    y = left_pad.ycor()
    y += 20
    left_pad.sety(y)

# 좌측 패들을 아래로 이동
def left_pad_down():
    y = left_pad.ycor()
    y -= 20
    left_pad.sety(y)

# 우측 패들을 위로 이동
def right_pad_up():
    y = right_pad.ycor()
    y += 20
    right_pad.sety(y)

# 우측 패들을 아래로 이동
def right_pad_down():
    y = right_pad.ycor()
    y -= 20
    right_pad.sety(y)


# 키 바인딩
win.listen()
win.onkeypress(left_pad_up, "w")
win.onkeypress(left_pad_down, "s")
win.onkeypress(right_pad_up, "Up")
win.onkeypress(right_pad_down, "Down")


while True:
    win.update()

    # 공의 이동
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # 공이 상단 벽과 충돌했을 때
    if ball.ycor() > 190:
        ball.sety(190)
        ball.dy *= -1

    # 공이 하단 벽과 충돌했을 때
    if ball.ycor() < -190:
        ball.sety(-190)
        ball.dy *= -1

    # 공이 우측 벽과 충돌했을 때 (좌측 선수 승리)
    if ball.xcor() > 290:
        ball.goto(0, 0)
        ball.dx *= -1
        left_score += 1
        score.clear()
        score.write("Player 1: {}  Player 2: {}".format(left_score, right_score), align="center", font=("Courier", 16, "normal"))

    # 공이 좌측 벽과 충돌했을 때 (우측 선수 승리)
    if ball.xcor() < -290:
        ball.goto(0, 0)
        ball.dx *= -1
        right_score += 1
        score.clear()
        score.write("Player 1: {}  Player 2: {}".format(left_score, right_score), align="center", font=("Courier", 16, "normal"))

    # 공이 좌측 패들과 충돌했을 때
    if ball.xcor() < -240 and ball.ycor() < left_pad.ycor() + 50 and ball.ycor() > left_pad.ycor() - 50:
        ball.setx(-240)
        ball.dx *= -1

    # 공이 우측 패들과 충돌했을 때
    if ball.xcor() > 240 and ball.ycor() < right_pad.ycor() + 50 and ball.ycor() > right_pad.ycor() - 50:
        ball.setx(240)
        ball.dx *= -1

