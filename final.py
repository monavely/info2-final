import pyxel
import random
import math

field_size = 150

class Star:
    speed = -3
   
    def __init__(self):
        self.restart()
       
    def move(self):
        self.x -= self.vx * Star.speed
        self.y += self.vy * Star.speed
        if (self.y < 0) or (self.y >= field_size):
            self.vy = -self.vy

    def restart(self):
        self.x = field_size - 1 
        self.y = pyxel.rndi(0, field_size - 1)
        angle = pyxel.rndi(120, 240)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def draw(self):
        size = 15
        num_points = 5
        angle_increment = 360 / (2 * num_points)

        x_points = []
        y_points = []

        for i in range(num_points * 2):
            radius = size if i % 2 == 0 else size / 2
            theta = math.radians(i * angle_increment)
            x = self.x + radius * math.cos(theta)
            y = self.y + radius * math.sin(theta)
            x_points.append(x)
            y_points.append(y)

        for i in range(num_points * 2):
            pyxel.line(x_points[i], y_points[i], x_points[(i + 1) % (num_points * 2)], y_points[(i + 1) % (num_points * 2)], 10)


class Tinkerbell:
    def __init__(self):
        self.x = 20
        self.y = field_size / 2
        self.size = field_size / 5

    def catch(self, star):
        if (self.y - field_size / 10 <= star.y <= self.y + field_size / 10) and star.x <= 20:
            pyxel.play(1, 1, loop=False)
            star.restart()
            return True
        else:
            return False
        
class App:
    def __init__(self):
        pyxel.init(field_size, field_size)
        pyxel.load('editor.pyxres')  

        self.stars = [Star()]
        self.tinkerbell = Tinkerbell() 
        self.alive = False
        self.life = 10
        self.receive = 0
        self.score = 10
        self.game_over = False

        pyxel.run(self.update, self.draw)

    def update(self):

        if not self.alive:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.alive = True
            return

        self.tinkerbell.y = pyxel.mouse_y
        for b in self.stars:
            b.move()
        
            if self.tinkerbell.catch(b):
                Star.speed -= 0.2
                self.score -= 1
                self.receive += 1
                if self.receive >= 10:
                    self.alive = False
                    self.game_over = True
        
            elif b.x < 0: 
                pyxel.play(0,0,loop=False)
                b.restart()
                Star.speed -= 0.2
                self.life -= 0
                self.alive = (self.life > 0)
            
            if self.score <= 0:
                self.alive = False
                self.game_over = True

    def draw(self):

        if not self.alive and not self.game_over:
            pyxel.cls(0) 
            pyxel.text(field_size/2-40, field_size/2-20, "Press SPACE to start", 7)
        elif self.alive:
            pyxel.cls(1)
            for b in self.stars:
                b.draw()
            pyxel.blt(15, self.tinkerbell.y - self.tinkerbell.size/2, 0, 0,0,16,16,1)
            pyxel.text(5, 5, "HP: " + str(self.score), 7)
        else:
            pyxel.cls(0) 
            pyxel.text(field_size/2-20, field_size/2-20, "Game Over!!!", 7)

App()
