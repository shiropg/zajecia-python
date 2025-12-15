import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (20, 20, 20)
WHITE = (220, 220, 220)
BLUE = (30, 144, 255)
GRAY = (100, 100, 100)

class TankSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Symulacja Zbiornika")
        self.clock = pygame.time.Clock()

        self.center_x = WIDTH // 2
        self.start_y = 100
        self.top_h = 80; self.mid_h = 200; self.bot_h = 80
        self.w_top_wide = 300; self.w_mid = 200; self.w_bot_narrow = 40

        self.total_height = self.top_h + self.mid_h + self.bot_h
        self.current_level = 0.0

        self.is_filling = False
        self.is_draining = False
        self.flow_rate = 2.0

        self.liquid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._pre_render_liquid_shape()

    def _pre_render_liquid_shape(self):
        p1 = (self.center_x- self.w_top_wide//2, self.start_y)
        p2 = (self.center_x + self.w_top_wide//2, self.start_y)
        p3 = (self.center_x + self.w_mid//2, self.start_y + self.top_h)
        p4 = (self.center_x- self.w_mid//2, self.start_y + self.top_h)
        p5 = (self.center_x + self.w_mid//2, self.start_y + self.top_h + self.mid_h)
        p6 = (self.center_x- self.w_mid//2, self.start_y + self.top_h + self.mid_h)
        p7 = (self.center_x + self.w_bot_narrow//2, self.start_y + self.total_height)
        p8 = (self.center_x- self.w_bot_narrow//2, self.start_y + self.total_height)

        self.tank_points = [p1, p2, p3, p5, p7, p8, p6, p4]

        pygame.draw.polygon(self.liquid_surface, BLUE, self.tank_points)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.is_filling = not self.is_filling
                elif event.key == pygame.K_DOWN:
                    self.is_draining = not self.is_draining
                elif event.key == pygame.K_r:
                    self.current_level = 0
                    self.is_filling = False; self.is_draining = False

    def update(self):
        if self.is_filling and self.current_level < self.total_height:
            self.current_level += self.flow_rate

        if self.is_draining and self.current_level > 0:
            self.current_level-= self.flow_rate

        self.current_level = max(0.0, min(self.current_level, self.total_height))

    def draw(self):
        self.screen.fill(BLACK)

        pygame.draw.polygon(self.screen, GRAY, self.tank_points, 4)

        if self.current_level > 0:
            current_liquid = self.liquid_surface.copy()
            empty_height = self.total_height- self.current_level
            liquid_top_y = self.start_y + empty_height
            clear_rect = pygame.Rect(0, 0, WIDTH, liquid_top_y)
            current_liquid.fill((0,0,0,0), clear_rect, special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(current_liquid, (0,0))
        
        if self.is_filling and self.current_level < self.total_height:
            pygame.draw.line(self.screen, BLUE, (self.center_x, self.start_y- 50), (self.center_x, self.start_y + (self.total_height- self.current_level)), 8)

        if self.is_draining and self.current_level > 0:
            pygame.draw.line(self.screen, BLUE, (self.center_x, self.start_y + self.total_height), (self.center_x, HEIGHT), 6)

        self.draw_ui()
        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.SysFont("Arial", 20)
        status_in = "OTWARTY" if self.is_filling else "ZAMKNIETY"
        status_out = "OTWARTY" if self.is_draining else "ZAMKNIETY"
        percent = int((self.current_level / self.total_height) * 100)
        self.screen.blit(font.render(f"Poziom: {percent}%", True, WHITE), (10, 10))
        self.screen.blit(font.render(f"Góra: {status_in}", True, WHITE), (10, 40))
        self.screen.blit(font.render(f"Dół: {status_out}", True, WHITE), (10, 70))

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    TankSimulation().run()