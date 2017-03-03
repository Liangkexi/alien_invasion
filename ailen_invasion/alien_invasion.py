#!coding=utf-8
import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏创建屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    #创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    #创建一个飞船
    ship = Ship(ai_settings, screen)
    #创建子弹编组
    bullets = Group()
    #创建一个外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #创建play按钮
    play_button = Button(ai_settings, screen, "Play")
    #开始游戏主循环
    while True:
        #监视键盘、鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            #更新飞船的位置
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            #每次循环重绘制屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
