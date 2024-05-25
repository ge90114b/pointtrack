import cv2  
from ultralytics import YOLO  
import os  
import pygame 
import torch
import time
from anti_shake import *
# 设置环境变量，用于在没有GUI的服务器上显示视频  
os.environ['SDL_VIDEODRIVER'] = 'x11'  
# 打开视频文件  
video_path = "1.mp4" 
pygame.init()
points=pygame.display.set_mode((800,600))
font = pygame.font.Font(None,20)
color = (255, 255, 255)
# 定义按钮类
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

# 创建两个按钮实例
button1 = Button(200, 200, 100, 50, "camera")
button2 = Button(500, 200, 100, 50, "video")

  
# 加载YOLOv8模型  
model = YOLO('yolov8n-pose.pt')  # 根据需要更改模型路径  

a = 1
while a==1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button1.is_clicked(event.pos):
                a = 0
                cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
                # 设置帧率和分辨率
                cap.set(cv2.CAP_PROP_FPS, 30)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            elif button2.is_clicked(event.pos):
                a = 0
                cap = cv2.VideoCapture(video_path) 

    points.fill((0, 0, 0))  # 填充背景色
    button1.draw(points)  # 绘制按钮
    button2.draw(points)  # 绘制按钮
    pygame.display.update()  # 更新屏幕
 
cap = cv2.VideoCapture(a)  


first=True
frame_count = 0  
fps_clock = pygame.time.Clock() 

# 遍历视频帧  
while cap.isOpened():  
    success, frame = cap.read()  
    cv2.imshow("org", frame)  
      
    if success:  
        # 在该帧上运行YOLOv8推理  
        results = model(frame)  
          
        # 在帧上可视化结果  
        annotated_frame = results[0].plot() 
          
        # 显示带注释的帧  
        cv2.imshow("YOLOv8", annotated_frame)  
        keypoints = results[0].keypoints.xy.squeeze().tolist()
        # 清除屏幕
        points.fill((0, 0, 0))
        lines=0
        # 在屏幕上显示关键点坐标
        for i, point in enumerate(keypoints):
            
            if i in [0,9,10] :
                text = font.render(f"Point {i}: {point}", True, color)
                points.blit(text, (5, 10 + lines * 30))
                lines+=1
                try:
                    print("p",point)
                    if a!=0:
                        point=antishake(point,first)
                    
                    print(point)
                                    # 更新帧计数器  
                    frame_count += 1  
                    fps = fps_clock.get_fps()  # 获取当前帧率  
                    
                    # 在pygame窗口上绘制帧率  
                    fps_text = font.render(f"FPS: {int(fps)}", True, color)  
                    points.blit(fps_text, (points.get_width() - fps_text.get_width() - 5, 5))  # 右上角位置 
                    x, y = point
                    pygame.draw.circle(points, color, (int(x), int(y)), 5)
                    normal=point

                except:
                    pass
            else:
                pass
 
          
        pygame.display.flip()  # 更新pygame窗口  
        fps_clock.tick()  # 更新时钟 
        first=False
        pygame.display.flip()
    
          
        # 如果按下'q'则中断循环  
        if cv2.waitKey(1) & 0xFF == ord("q"):  
            break  
    else:  
        break  
  
# 释放资源  
cap.release()  

cv2.destroyAllWindows()