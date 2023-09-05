# required: pygame, opencv-python
import pygame
import cv2
import numpy as np

def readMyVideo(status):
    path = "drop.avi" if status else "flame.avi"
    clip = cv2.VideoCapture(path)
    # w = clip.get(cv2.CAP_PROP_FRAME_WIDTH)
    # h = clip.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = clip.get(cv2.CAP_PROP_FPS)
    return clip,fps

def imgResize(img):
    size=(SCREEN_WIDTH,SCREEN_HEIGHT)
    base_pic=np.zeros((size[1],size[0],3),np.uint8)
    h,w=img.shape[:2]
    ash=size[1]/h
    asw=size[0]/w
    if asw<ash:
        sizeas=(int(w*asw),int(h*asw))
    else:
        sizeas=(int(w*ash),int(h*ash))
    img = cv2.resize(img,dsize=sizeas)
    base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
    int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=img

    return base_pic

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

status = 0
ioStatus = 0
clip,fps = readMyVideo(status)

#def readStatus():
#    return ioStatus

pygame.init()
# screen = pygame.display.set_mode((1920,1080))

CHANGE_STATUS = pygame.USEREVENT + 1
#pygame.time.set_timer(CHANGE_STATUS, 2000)

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_s:
                ioStatus = abs(ioStatus-1)
                #clip,fps = readMyVideo(status)
        if event.type == CHANGE_STATUS:
                #status = abs(status-1)
                clip,fps = readMyVideo(status) 
    if status!=ioStatus:
        status=ioStatus
        pygame.event.post(pygame.event.Event(CHANGE_STATUS))

    ret, frame = clip.read()
    if ret:
        #frame = cv2.resize(frame, (1920, 1080))
        image = pygame.image.frombuffer(imgResize(frame), (SCREEN_WIDTH, SCREEN_HEIGHT), "BGR")
        screen.blit(image, (0,0))
    else:
        clip.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()


