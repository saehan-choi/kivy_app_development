import turtle
import random


class PongEnv:
    def __init__(self):
        self.win = turtle.Screen()
        self.win.title("Pong")
        self.win.bgcolor("black")
        self.win.setup(width=600, height=400)
        self.win.tracer(0)

        self.left_pad = self.create_pad(-250)
        self.right_pad = self.create_pad(250)
        self.ball = self.create_ball()
        self.left_score, self.right_score = 0, 0
        self.score = self.create_scoreboard()
        
        self.register_key_events()
        
        self.action_space = [0, 1, 2, 3]

    def create_pad(self, x):
        pad = turtle.Turtle()
        pad.speed(0)
        pad.shape("square")
        pad.color("white")
        pad.shapesize(stretch_wid=5, stretch_len=1)
        pad.penup()
        pad.goto(x, 0)
        return pad

    def create_ball(self):
        ball = turtle.Turtle()
        ball.speed(50)
        ball.shape("circle")
        ball.color("white")
        ball.penup()
        ball.goto(0, 0)
        ball.dx = 0.1
        ball.dy = -0.1
        return ball

    def create_scoreboard(self):
        score = turtle.Turtle()
        score.speed(0)
        score.color("white")
        score.penup()
        score.hideturtle()
        score.goto(0, 170)
        score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))
        return score

    def register_key_events(self):
        self.win.listen()
        self.win.onkeypress(self.left_pad_up, "w")
        self.win.onkeypress(self.left_pad_down, "s")
        self.win.onkeypress(self.right_pad_up, "Up")
        self.win.onkeypress(self.right_pad_down, "Down")

    def left_pad_up(self):
        self.move_pad(self.left_pad, 20)

    def left_pad_down(self):
        self.move_pad(self.left_pad, -20)

    def right_pad_up(self):
        self.move_pad(self.right_pad, 20)

    def right_pad_down(self):
        self.move_pad(self.right_pad, -20)

    def move_pad(self, pad, dy):
        y = pad.ycor()
        y += dy
        pad.sety(y)

    def update(self):
        self.win.update()

    def close(self):
        self.win.bye()

    def get_state(self):
        left_pad_y = self.left_pad.ycor()
        right_pad_y = self.right_pad.ycor()
        ball_x = self.ball.xcor()
        ball_y = self.ball.ycor()
        ball_dx = self.ball.dx
        ball_dy = self.ball.dy

        state = [left_pad_y, right_pad_y, ball_x, ball_y, ball_dx, ball_dy]
        return state

    def step(self, action):
        self.perform_action(action)
        self.move_ball()
        self.check_wall_collision()
        self.check_pad_collision()

        state = self.get_state()
        reward = self.calculate_reward()
        done = (reward != 0)

        return state, reward, done, {}

    def perform_action(self, action):
        if action == 0:
            self.left_pad_up()
        elif action == 1:
            self.left_pad_down()
        elif action == 2:
            self.right_pad_up()
        elif action == 3:
            self.right_pad_down()

    def move_ball(self):
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

    def check_wall_collision(self):
        if self.ball.ycor() > 190:
            self.ball.sety(190)
            self.ball.dy *= -1
        if self.ball.ycor() < -190:
            self.ball.sety(-190)
            self.ball.dy *= -1

        if self.ball.xcor() > 290:
            self.score_update(left_player_scored=True)
        if self.ball.xcor() < -290:
            self.score_update(left_player_scored=False)

    def score_update(self, left_player_scored):
        self.ball.goto(0, 0)
        self.ball.dx *= -1

        if left_player_scored:
            self.left_score += 1
        else:
            self.right_score += 1

        self.score.clear()
        self.score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))

    def check_pad_collision(self):
        if self.ball.xcor() < -240 and self.ball.ycor() < self.left_pad.ycor() + 50 and self.ball.ycor() > self.left_pad.ycor() - 50:
            self.ball.setx(-240)
            self.ball.dx *= -1

        if self.ball.xcor() > 240 and self.ball.ycor() < self.right_pad.ycor() + 50 and self.ball.ycor() > self.right_pad.ycor() - 50:
            self.ball.setx(240)
            self.ball.dx *= -1

        self.update()

    def calculate_reward(self):
        reward = 0
        if self.ball.xcor() > 240:
            reward = 1
        elif self.ball.xcor() < -240:
            reward = -1
        return reward

    def reset(self):
        self.left_pad.goto(-250, 0)
        self.right_pad.goto(250, 0)
        self.ball.goto(0, 0)
        self.ball.dx = 0.1
        self.ball.dy = -0.1
        self.left_score = 0
        self.right_score = 0
        self.score.clear()
        self.score.write("Player 1: {}  Player 2: {}".format(self.left_score, self.right_score), align="center", font=("Courier", 16, "normal"))

        state = self.get_state()
        
        
        return state