#!coding=utf-8

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键按下"""
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        #向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹数量未超阈值，创建子弹"""
    #创建子弹并加入bullets中
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
            
def check_keyup_events(event, ship):
    """响应按键松开"""
    if event.key == pygame.K_RIGHT:
        #停止向右移动
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        #停止向左移动
        ship.moving_left = False
        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, 
                ship, aliens, bullets, mouse_x, mouse_y)
def check_play_button(ai_settings, screen, stats, sb, play_button,
        ship, aliens, bullets, mouse_x, mouse_y):
    """单击鼠标开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏
        ai_settings.initialize_dynamic_settings()
        #重置游戏统计
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        #创建新的外星人，并将飞船置于底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘制屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    #如果处于非活动状态就绘制play_button
    if not stats.game_active:
        play_button.draw_button()
    #使得最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #print(">>>len of bullets: ", len(bullets))
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人碰撞"""
    #检查是否有子弹击中了外星人
    #如果击中就删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #删除现有子弹并创建新一组外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳的外星人数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算外星人行数"""
    available_space_y = (ai_settings.screen_height - 
        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建第一个外星人并加入当前行中"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算可以创建几个
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建第一个外星人并加入当前行中
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应对策"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """将整体外星人向下移动，并改变其方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """相应飞船与外星人相撞"""
    #将ships_left减一
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #更新计分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建新的外星人，并将飞船置于底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达窗口底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船碰撞一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break    
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查外星人是否位于屏幕边缘
    并更新外星人群中所有外星人
    """
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        print(">>>Ship hit!!!")
def check_high_score(stats, sb):
    """检查是否产生最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open("C:/Users/welwel/Desktop/ailen_invasion/high_score.ini",
            "w") as fp:
            fp.write(str(stats.score))