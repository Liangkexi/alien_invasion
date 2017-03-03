#!coding=utf-8

class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动时处于活跃
        self.game_active = False
        #计分
        self.score = 0
        #最高分不应被重置
        with open("C:/Users/welwel/Desktop/ailen_invasion/high_score.ini",
            "r+") as fp:
            self.high_score = fp.read()
            if self.high_score:
                self.high_score = int(self.high_score)
            else:
                self.high_score = 0
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1