#！coding=utf-8

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人"""
    
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像
        self.image = pygame.image.load("C:/Users/welwel/Desktop/ailen_invasion/images/alien.bmp")
        self.rect = self.image.get_rect()
        
        #每个外星人最初位置在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.recr.height
        
        #存储外星人准确位置
        self.x = float(self.rect.x)
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit()