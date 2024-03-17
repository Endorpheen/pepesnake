import pygame
import random

# Инициализация PyGame
pygame.init()
pygame.mixer.init()  # Инициализация mixer

# Загрузка музыки и звуков
pygame.mixer.music.load("/home/end0/CODE/pepesnake/yablochko.mp3")  # Замените "yablochko.mp3" на путь к вашему музыкальному файлу
game_music = pygame.mixer.Sound("/home/end0/CODE/pepesnake/super-mario.wav")  # Замените "super-mario.mp3" на путь к вашему музыкальному файлу
collision_sound = pygame.mixer.Sound("/home/end0/CODE/pepesnake/sound_effect_2.mp3")  # Замените "sound_effect_2.mp3" на путь к вашему звуковому файлу

# Класс Snake (змейка)
class Snake:
    def __init__(self, x, y, block_size):
        self.size = 1
        self.elements = [(x, y)]
        self.directions = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": True}
        self.block_size = block_size
        self.head = pygame.Rect(self.elements[0][0], self.elements[0][1], block_size, block_size)

    def move(self):
        cur = self.elements[0]
        x = cur[0]
        y = cur[1]
        if self.directions["UP"]:
            y -= self.block_size
        elif self.directions["DOWN"]:
            y += self.block_size
        elif self.directions["LEFT"]:
            x -= self.block_size
        elif self.directions["RIGHT"]:
            x += self.block_size

        # Проверка выхода за пределы экрана и перемещение на противоположную сторону
        if x < 0:
            x = screen_width - self.block_size
        elif x >= screen_width:
            x = 0
        if y < 0:
            y = screen_height - self.block_size
        elif y >= screen_height:
            y = 0

        self.elements.insert(0, (x, y))
        if len(self.elements) > self.size:
            self.elements.pop()
        self.head = pygame.Rect(x, y, self.block_size, self.block_size)

    def draw(self, screen):
        for x, y in self.elements:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, self.block_size, self.block_size))

# Класс Food (еда)
class Food:
    def __init__(self, block_size, obstacles):
        self.block_size = block_size
        self.position = (0, 0)
        self.generate_position(screen_width, screen_height, obstacles)

        # Загрузка изображения биткоина
        self.image = pygame.image.load("/home/end0/CODE/pepesnake/bitcoin.png")  # Замените "bitcoin.png" на путь к вашему изображению
        self.image = pygame.transform.scale(self.image, (block_size, block_size))

    def generate_position(self, screen_width, screen_height, obstacles):
        valid_position = False
        while not valid_position:
            x = random.randint(0, (screen_width - self.block_size) // self.block_size) * self.block_size
            y = random.randint(0, (screen_height - self.block_size) // self.block_size) * self.block_size
            potential_position = (x, y)
            valid_position = True

            # Проверка расстояния от препятствий
            for obstacle in obstacles:
                obstacle_rect = pygame.Rect(obstacle.position[0], obstacle.position[1], obstacle.size[0], obstacle.size[1])
                food_rect = pygame.Rect(potential_position[0], potential_position[1], self.block_size, self.block_size)

                # Получаем центры прямоугольников
                obstacle_center = pygame.math.Vector2(obstacle_rect.center)
                food_center = pygame.math.Vector2(food_rect.center)

                # Вычисляем расстояние между центрами прямоугольников
                if obstacle_center.distance_to(food_center) < 3 * self.block_size:
                    valid_position = False
                    break
                                                    
        self.position = potential_position

    def draw(self, screen):
        screen.blit(self.image, self.position)

# Класс Obstacle (препятствие)
class Obstacle:
    def __init__(self, block_size):
        self.block_size = block_size
        self.size = (5 * block_size, 5 * block_size)
        self.position = (0, 0)
        self.generate_position(screen_width, screen_height)

    def generate_position(self, screen_width, screen_height):
        x = random.randint(0, (screen_width - self.size[0]) // self.block_size) * self.block_size
        y = random.randint(0, (screen_height - self.size[1]) // self.block_size) * self.block_size
        self.position = (x, y)    

        # Загрузка изображений для анимации препятствий
        self.images = [
            pygame.image.load("/home/end0/CODE/pepesnake/biden.png"),
            pygame.image.load("/home/end0/CODE/pepesnake/biden2.png")
        ]
        # Масштабирование изображений до размера препятствия
        self.images = [pygame.transform.scale(image, self.size) for image in self.images]
        
        self.current_frame = 0
        self.animation_speed = 0.1
    
    def draw(self, screen):
        # Отрисовка текущего кадра анимации препятствий
        screen.blit(self.images[int(self.current_frame)], self.position)
        
        # Обновление текущего кадра анимации
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.images):
            self.current_frame = 0                

class LeaderBoard:
    def __init__(self, file_path):
        self.file_path = file_path
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.file_path, 'r') as file:
                scores = []
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 2:
                            name, score = parts
                            scores.append((name, int(score)))
                        else:
                            # Обработка некорректных строк
                            print(f"Некорректная строка в файле: {line}")
        except FileNotFoundError:
            scores = []
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def save_scores(self):
        with open(self.file_path, 'w') as file:
            for name, score in self.scores:
                file.write(f"{name},{score}\n")

    def add_score(self, name, score):
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        self.save_scores()

    def draw(self, screen, font):
        leaderboard_text = font.render("Таблица лидеров:", True, (255, 255, 255))
        screen.blit(leaderboard_text, (10, 60))
        y = 100
        for i, (name, score) in enumerate(self.scores[:8], start=1):
            score_text = font.render(f"{i}. {name}: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, y))
            y += 40

# Инициализация PyGame
pygame.init()
pygame.mixer.init()  # Инициализация микшера звуков

# Загрузка звукового файла
eat_sound = pygame.mixer.Sound("/home/end0/CODE/pepesnake/obozhrusja-i-pomru-molodoj.mp3")  # Замените на путь к вашему звуковому файлу

# Настройка окна
screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Моя игра")

# Загрузка фонового изображения
background_image = pygame.image.load("/home/end0/CODE/pepesnake/pepefrog.png")  # Замените "background.png" на путь к вашему изображению
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Создание объектов змейки и еды
block_size = 20
snake = Snake(screen_width // 2, screen_height // 2, block_size)
obstacles = [Obstacle(block_size) for _ in range(5)]  # Создание 5 препятствий
food = Food(block_size, obstacles)

# Шрифт для отображения длины змейки и стартового экрана
font = pygame.font.Font(None, 36)

def draw_score(screen, score, font):
    score_text = font.render(f"Length: {score}", True, (255, 0, 0))
    score_background = pygame.Rect(0, 0, 150, 50)
    pygame.draw.rect(screen, (0, 0, 0), score_background)
    screen.blit(score_text, (10, 10))

# Цикл игры
clock = pygame.time.Clock()
running = True
start_screen = True
game_over = False
leaderboard = LeaderBoard("/home/end0/CODE/pepesnake/scores.txt") # Создание объекта таблицы лидеров

while True:
    # Отображение стартового экрана
    if start_screen:
        screen.fill((0, 0, 0))
        start_text = font.render("Для начала игры нажмите любую кнопку", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_text, text_rect)
        pygame.display.flip()

      # Воспроизведение музыки на стартовом экране
        pygame.mixer.music.play(-1)  # Бесконечное воспроизведение  

        # Ожидание нажатия любой клавиши
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    start_screen = False
                    waiting = False
                    pygame.mixer.music.stop()  # Остановка музыки при запуске игры
                    game_music.play(-1)  # Воспроизведение музыки игры

    # Игровой цикл
    while not start_screen and not game_over:
        clock.tick(10)  # Ограничение FPS

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not snake.directions["DOWN"]:
                    snake.directions.update({"UP": True, "DOWN": False, "LEFT": False, "RIGHT": False})
                elif event.key == pygame.K_DOWN and not snake.directions["UP"]:
                    snake.directions.update({"UP": False, "DOWN": True, "LEFT": False, "RIGHT": False})
                elif event.key == pygame.K_LEFT and not snake.directions["RIGHT"]:
                    snake.directions.update({"UP": False, "DOWN": False, "LEFT": True, "RIGHT": False})
                elif event.key == pygame.K_RIGHT and not snake.directions["LEFT"]:
                    snake.directions.update({"UP": False, "DOWN": False, "LEFT": False, "RIGHT": True})

        # Обновление игрового процесса
        snake.move()
        if snake.head.colliderect(pygame.Rect(food.position[0], food.position[1], block_size, block_size)):
            snake.size += 1
            eat_sound.play()  # Воспроизведение звука
            food.generate_position(screen_width, screen_height, obstacles)
            for obstacle in obstacles:
                obstacle.generate_position(screen_width, screen_height)

        for obstacle in obstacles:
            if snake.head.colliderect(pygame.Rect(obstacle.position[0], obstacle.position[1], obstacle.size[0], obstacle.size[1])):
                game_over = True
                game_music.stop()  # Остановка музыки игрового процесса
                collision_sound.play()  # Воспроизведение звука столкновения
                break

        # Отрисовка
        screen.blit(background_image, (0, 0))  # Отрисовка фонового изображения
        snake.draw(screen)
        food.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Отображение длины змейки
        draw_score(screen, snake.size, font)

        pygame.display.flip()

        # Экран конца игры
    if game_over:
        screen.fill((0, 0, 0))
        # Загрузка и отображение изображения лица человека
        face_image = pygame.image.load("/home/end0/CODE/pepegametest/trump-face.png")
        face_image = pygame.transform.scale(face_image, (200, 200))
        face_rect = face_image.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(face_image, face_rect)

        # Отображение текста конца игры и создателя
        game_over_text = font.render(f"Конец игры, ваш счет: {snake.size}", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(game_over_text, text_rect)
        created_by_text = font.render("Created by end0", True, (255, 255, 255))
        created_by_rect = created_by_text.get_rect(center=(screen_width // 2, screen_height - 50))
        screen.blit(created_by_text, created_by_rect)

        # Отображение запроса на ввод имени
        name_text = font.render("Введите ваше имя:", True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))
        screen.blit(name_text, name_rect)
        pygame.display.flip()

        # Инициализация переменной для имени игрока
        name = ""
        enter_pressed = False

        # Цикл ввода имени игрока
        while not enter_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        enter_pressed = True
                        leaderboard.add_score(name, snake.size)
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                    # Отображение текущего вводимого имени
                    screen.fill((0, 0, 0))  # Очищаем экран
                    # Повторно отображаем все элементы, так как экран очищен
                    screen.blit(face_image, face_rect)
                    screen.blit(game_over_text, text_rect)
                    screen.blit(created_by_text, created_by_rect)
                    screen.blit(name_text, name_rect)
                    # Отображаем введенное имя
                    name_surface = font.render(name, True, (255, 255, 255))
                    screen.blit(name_surface, (screen_width // 2 - name_surface.get_width() // 2, screen_height // 2 + 200))
                    pygame.display.flip()
        
        # Отрисовка списка лидеров
        screen.fill((0, 0, 0))  # Очистка экрана для отрисовки списка лидеров
        # ... [код отрисовки фона и текста, если необходимо] ...
        leaderboard.draw(screen, font)  # Отрисовка списка лидеров
        pygame.display.flip()

        # Ожидание действия пользователя для выхода с экрана списка лидеров
        waiting_for_user_to_proceed = True
        while waiting_for_user_to_proceed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_user_to_proceed = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_user_to_proceed = False

        # Перезапуск игры
        start_screen = True
        game_over = False
        snake = Snake(screen_width // 2, screen_height // 2, block_size)
        food.generate_position(screen_width, screen_height, obstacles)
        for obstacle in obstacles:
            obstacle.generate_position(screen_width, screen_height)
        pygame.mixer.music.stop()  # Остановка музыки при конце игры

# Выход из PyGame
#    pygame.quit()