import pygame
import random

class Object:
    def __init__(self, x, y, speedX, speedY, image, imageID):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.image = image
        self.imageID = imageID

pygame.init()

#colors
WHITE = (255, 255, 255)

#screen & image settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
IMAGE_WIDTH, IMAGE_HEIGHT = 100, 100

#object settings
speedX, speedY = 0.1, 0.1 #object speed
seed = random.randint(3, 15) #object seed
#seed = 3

running = True
objects = []
j = 0
counter = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

images = []
images.append(pygame.image.load('Images/rock.png'))
images.append(pygame.image.load('Images/scissors.png'))
images.append(pygame.image.load('Images/paper.png'))

soundRock = pygame.mixer.Sound('Sounds/rock.mp3')
soundScissors = pygame.mixer.Sound('Sounds/scissors.mp3')
soundPaper = pygame.mixer.Sound('Sounds/paper.mp3')
#soundbg = pygame.mixer.Sound('Sounds/tokyodrift.mp3')

for i in range(seed):
    if j == 3:
        j = 0
    images[j] = pygame.transform.scale(images[j], (IMAGE_WIDTH, IMAGE_HEIGHT))
    x = random.randint(0, SCREEN_WIDTH-100)
    y = random.randint(0, SCREEN_HEIGHT-100)
    objects.append(Object(x, y, speedX, speedY, images[j], j))
    j += 1

def battle(obj1, obj2):
    if(obj1.imageID == 0 and obj2.imageID == 2):
        return False
    if(obj1.imageID == 2 and obj2.imageID == 0):
        return True
    if(obj1.imageID < obj2.imageID):
        return True
    else:
        return False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(seed):
        obj = objects[i]

        obj.x += obj.speedX
        obj.y += obj.speedY

        if obj.x <= 0 or obj.x + 100 >= SCREEN_WIDTH:
            obj.speedX *= -1
        if obj.y <= 0 or obj.y + 100 >= SCREEN_HEIGHT:
            obj.speedY *= -1

    for obj1 in objects:
        obj1Coll = pygame.Rect(obj1.x, obj1.y, obj1.image.get_width(), obj1.image.get_height())
        for obj2 in objects:
            obj2Coll = pygame.Rect(obj2.x, obj2.y, obj2.image.get_width(), obj2.image.get_height())
            if obj1Coll.colliderect(obj2Coll):
                overlap_left = obj2Coll.right - obj1Coll.left
                overlap_right = obj1Coll.right - obj2Coll.left
                overlap_top = obj2Coll.bottom - obj1Coll.top
                overlap_bottom = obj1Coll.bottom - obj2Coll.top

                if (obj1.image != obj2.image):
                    if (battle(obj1, obj2)):
                        obj2.image = obj1.image
                        obj2.imageID = obj1.imageID
                        if(obj1.imageID == 0):
                            soundRock.play()
                        elif(obj1.imageID == 1):
                            soundScissors.play()
                        else:
                            soundPaper.play()
                    else:
                        obj1.image = obj2.image
                        obj1.imageID = obj2.imageID
                        if (obj2.imageID == 0):
                            soundRock.play()
                        elif (obj2.imageID == 1):
                            soundScissors.play()
                        else:
                            soundPaper.play()

                    if overlap_left < overlap_right and overlap_left < overlap_top and overlap_left < overlap_bottom:
                        obj1.speedX *= -1
                        obj2.speedX *= -1
                        break
                    elif overlap_right < overlap_left and overlap_right < overlap_top and overlap_right < overlap_bottom:
                        obj1.speedX *= -1
                        obj2.speedX *= -1
                        break
                    else:
                        obj1.speedY *= -1
                        obj2.speedY *= -1
                        break

    screen.fill(WHITE)

    for i in range(seed):
        obj = objects[i]
        screen.blit(obj.image, (obj.x, obj.y))

    pygame.display.update()

pygame.quit()
