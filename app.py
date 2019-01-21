import pyglet
from gameArea import GameArea
from settings import *
import socket
import threading
from enum import Enum

INPUT = None
AUTHOR = None

class Input(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def twitchStart(e):
    def send_message(message):
        s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))

    while True:
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:
        for line in str(s.recv(1024)).split('\\r\\n'):
            parts = line.split(':')
            if len(parts) < 3:
                continue

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                message = parts[2][:len(parts[2])]

            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            print(username + ": " + message)
            if message == "Hey":
                send_message("Welcome to my stream, " + username)
            elif message.lower() == 'up':
                setInput(Input.UP, username)
            elif message.lower() == 'down':
                setInput(Input.DOWN, username)
            elif message.lower() == 'left':
                setInput(Input.LEFT, username)
            elif message.lower() == 'right':
                setInput(Input.RIGHT, username)

            if message.__contains__('kokot'):
                send_message('Sám seš kokot ' + username + ' 4Head')

def setInput(input, username):
    global INPUT, AUTHOR
    if INPUT is None:
        INPUT = input
        AUTHOR = username

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0

        self.area = GameArea(self, 50, self.height - 150)

    def on_draw(self):
        self.clear()
        self.area.draw()

    def update(self, input):
        if(self.area.isPlayable()):
            global INPUT
            #self.area.update()

            if INPUT is not None:
                self.area.addAuthor(AUTHOR)
                if INPUT is Input.UP:
                    self.area.moveUp()
                elif INPUT is Input.DOWN:
                    self.area.moveDown()
                elif INPUT is Input.LEFT:
                    self.area.moveLeft()
                elif INPUT is Input.RIGHT:
                    self.area.moveRight()
            INPUT = None
        else:
            self.area.reset()

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='twitch',
                          target=twitchStart,
                          args=(e,))
    t1.start()

    window = GameWindow(1280, 720, "Twitch 2048", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()

