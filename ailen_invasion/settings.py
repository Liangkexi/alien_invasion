#!coding=utf-8

class Settings():
    """存储所有设置的类"""
    
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 800
        self.screen_height = 500
        self.bg_color = (230, 230, 230)
        #飞船设置
        #每次移动1.5像素
        self.ship_limit = 3
        self.ship_speed_factor = 1.5
        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 2
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        #外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移动，为-1表示向左
        self.fleet_direction = 1
        #设置游戏难度等级阶梯
        self.speedup_scale = 1.1
        #分值提高比例
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        #fleet_direction为1表示向右移动，为-1表示向左
        self.fleet_direction = 1
        #计分
        self.alien_points = 50
    def increase_speed(self):
        """提高速度&分值设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(">>>level:",self.alien_speed_factor,"\n",
            ">>>分值:",self.alien_points)