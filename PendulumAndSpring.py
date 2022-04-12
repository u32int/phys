import pygame
import math

pygame.init()

# -- General sim settings / Ustawienia -- 
sim_speed = 1 
scale = 10
# -- pygame settings -- 
WIDTH,HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = (33,35,41)
FPS = 60
FONT_SIZE = 21
FONT = pygame.font.SysFont("mono", FONT_SIZE)
pygame.display.set_caption("Pendulum sim")
# -- Constants  -- 
g = 9.81
pi = math.pi

class Button:
    def __init__(self, x, y, width, height, color, text, text_color=None) -> None:
        self.x = x   
        self.y = y   
        self.width = width   
        self.height = height   
        self.color = color   
        self.text = text
        if text_color == None:
            self.text_color = (255,255,255)
        else:
            self.text_color = text_color    
    
    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height))
        text = FONT.render(self.text, True, self.text_color)
        WIN.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def overlaps(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width:
            if mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
                return True

class Pendulum:
    def __init__(self, l, alpha, r) -> None:
        self.l = l
        self.wychylenie_max = alpha
        self.r = r
        self.direction = "r"
        self.T = 2*pi * math.sqrt(self.l/g)    
        self.cartesian_x = WIDTH - WIDTH/4

    def draw(self, t):
        omega = 2*pi/self.T
        self.alpha = self.wychylenie_max * math.sin(omega * t)
        v = self.wychylenie_max * omega * math.cos(omega * t)
        a = pow(omega,2) * self.wychylenie_max * math.sin(omega * t)

        v_text = FONT.render(f"v (rad/s) = {round(v,2)}", True, (255,255,255))
        a_text = FONT.render(f"a = {round(a,2)}", True, (255,255,255))
        alpha_rad_text = FONT.render(f"kąt (rad) = {round(self.alpha,2)}", True, (255,255,255))
        alpha_deg_text = FONT.render(f"kąt (deg) = {round(math.degrees(self.alpha),2)}", True, (255,255,255))
        stats = [alpha_deg_text,alpha_rad_text,v_text,a_text]
        for i in range(0, len(stats)):
            WIN.blit(stats[i], (WIDTH - FONT_SIZE*12, (FONT_SIZE * i + 1) + 3))

        x = math.sin(self.alpha) * self.l * scale + self.cartesian_x
        y = math.cos(self.alpha) * self.l * scale + HEIGHT/3

        pygame.draw.line(WIN, (0,0,0), (x,y), (self.cartesian_x, HEIGHT/3))
        pygame.draw.circle(WIN, (255,255,255), (x,y), self.r * scale)

class Spring:
    def __init__(self, amplitude, mass, k, r) -> None:
        self.amplitude = amplitude
        self.mass = mass
        self.k = k
        self.r = r
        self.T = 2*pi * math.sqrt(self.mass/self.k)
        self.cartesian_x = WIDTH/4

    def draw(self, t):
        omega = 2*pi/self.T
        x = self.amplitude * math.sin(omega*t)
        v = omega*self.amplitude * math.cos(omega*t)
        a = pow(omega,2) * self.amplitude * math.sin(omega * t)

        v_text = FONT.render(f"v (px/s) = {round(v,2)}", True, (255,255,255))
        a_text = FONT.render(f"a = {round(a,2)}", True, (255,255,255))
        x_text = FONT.render(f"x = {round(x,2)}", True, (255,255,255))
        stats = [x_text,v_text,a_text]
        for i in range(0, len(stats)):
            WIN.blit(stats[i], (15, (FONT_SIZE * i + 1) + 3))

        pygame.draw.line(WIN, (0,0,0), (self.cartesian_x,x+HEIGHT/2), (self.cartesian_x,HEIGHT/3))
        pygame.draw.circle(WIN, (255,255,255), (self.cartesian_x, x+HEIGHT/2), self.r)


def main():
    run = True
    fpsclock = pygame.time.Clock()

    t = 0
    w1 = Pendulum(30, pi/6, 1)
    s1 = Spring(100, 2, 1, 10)
    reset_button = Button(WIDTH-100, HEIGHT-50, 100,50, (15,15,15), "reset")
    while run:
        fpsclock.tick(FPS)
        WIN.fill(BG)
        w1.draw(t)
        s1.draw(t)
        reset_button.draw()
        t+=1/FPS * sim_speed
        
        t_text = FONT.render(f"t = {round(t,1)}s", True, (255,255,255))
        WIN.blit(t_text, (0, HEIGHT - FONT_SIZE))
        
        pygame.display.update()

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                if reset_button.overlaps(mouse_pos):
                    reset_button.color = (30,30,30)
                else:
                    reset_button.color = (15,15,15)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.overlaps(mouse_pos):
                    t = 0
                    

    pygame.quit()

if __name__ == "__main__":
    main()
