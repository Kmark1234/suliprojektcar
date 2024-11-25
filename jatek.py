import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Autós Játék")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

 
opening_image = pygame.image.load("opening_image.png")
menu_image = pygame.image.load("menu_image.png")
start_button_image = pygame.image.load("start_button.png")
car_skins = [
    pygame.image.load("car_skin1.png"),
    pygame.image.load("car_skin2.png"),
    pygame.image.load("car_skin3.png"),
    pygame.image.load("car_skin4.png")
]
background = pygame.image.load("freepik__retouch__1347.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


start_button_image = pygame.transform.scale(start_button_image, (400, 400))
car_skins = [pygame.transform.scale(skin, (100, 60)) for skin in car_skins]


car_width, car_height = 50, 30


def show_opening_image():
    screen.blit(opening_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(6000)  


def show_menu():
    selected_car = 0  
    while True:
        screen.blit(menu_image, (0, 0))


        start_button_rect = screen.blit(start_button_image, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        car_rects = []
        for i, car_skin in enumerate(car_skins):
            x = WIDTH // 5 * (i + 1) - 50
            y = HEIGHT - 150
            rect = screen.blit(car_skin, (x, y))
            car_rects.append(rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return selected_car  
                for i, rect in enumerate(car_rects):
                    if rect.collidepoint(event.pos):
                        selected_car = i  

        for i, rect in enumerate(car_rects):
            if i == selected_car:
                pygame.draw.rect(screen, WHITE, rect.inflate(10, 10), 3)

        pygame.display.flip()


def run_game(selected_car):
    car_image = pygame.transform.scale(car_skins[selected_car], (car_width, car_height))
    car_x, car_y = 100, 700
    car_speed = 5

    map_borders = [
        pygame.Rect(50, 50, 1100, 50),
        pygame.Rect(50, 700, 1100, 50)
    ]
    finish_rect = pygame.Rect(1050, 350, 100, 100)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            car_y -= car_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            car_y += car_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            car_x += car_speed

        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        hit_border = any(car_rect.colliderect(border) for border in map_borders)

        if hit_border:
            print("Játék vége! Leértél az útról.")
            running = False

        if car_rect.colliderect(finish_rect):
            print("Győzelem! Ügyesen végigértél a pályán!")
            running = False

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), finish_rect)
        screen.blit(car_image, (car_x, car_y))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

show_opening_image()
selected_car = show_menu()
run_game(selected_car)
