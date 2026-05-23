"""
Source under analysis for the (b) sequence diagram.
Original pygame collision simulation provided in the homework brief.
"""

import pygame
import math
import random
import itertools
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
FPS = 60
WIN_WIDTH = 1024
WIN_HEIGHT = 768
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Collisions')

# ---- 全域變數 ----
collidables = []
gravity = 0.5
draw_attractions = False
expansion = 0.2
current_obj = {
    "pos": Vector2(0, 0),
    "velocity": Vector2(0, 0),
    "radius": 1,
    "mass": 1,
    "colour": (255, 0, 0),
}


def random_colour():
    return (random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255))


def draw_collidables():
    for obj in collidables:
        obj["pos"] += obj["velocity"]
        pygame.draw.circle(window, obj["colour"],
                           obj["pos"], int(obj["radius"]), 0)


def calculate_movement():
    for o in collidables:
        other_objs = [x for x in collidables if x is not o]
        for other in other_objs:
            direction = other["pos"] - o["pos"]
            magnitude = other["pos"].distance_to(o["pos"])
            if magnitude == 0:
                continue
            n_direction = direction.normalize()
            clamped_mag = max(5, min(15, magnitude))
            strength = ((gravity * o["mass"] * other["mass"]) /
                        (clamped_mag ** 2)) / other["mass"]
            applied_force = Vector2(n_direction * strength)
            other["velocity"] -= applied_force
            if draw_attractions:
                pygame.draw.line(window, (255, 255, 255),
                                 o["pos"], other["pos"], 1)


def handle_collisions():
    """偵測兩兩碰撞，較大的吸收較小的。"""
    to_remove = set()
    for a, b in itertools.combinations(collidables, 2):
        if id(a) in to_remove or id(b) in to_remove:
            continue
        distance = a["pos"].distance_to(b["pos"])
        if distance < a["radius"] + b["radius"]:
            # 較大的吸收較小的
            bigger, smaller = (a, b) if a["mass"] >= b["mass"] else (b, a)
            total_mass = bigger["mass"] + smaller["mass"]
            # 動量守恆計算新速度
            bigger["velocity"] = (
                (bigger["velocity"] * bigger["mass"] +
                 smaller["velocity"] * smaller["mass"]) / total_mass
            )
            bigger["mass"] = total_mass
            # 體積相加（面積近似）後反推半徑
            bigger["radius"] = math.sqrt(bigger["radius"] ** 2 +
                                          smaller["radius"] ** 2)
            to_remove.add(id(smaller))

    collidables[:] = [obj for obj in collidables if id(obj) not in to_remove]


def draw_current_object():
    global current_obj, expansion
    current_obj["pos"] = Vector2(mouse_pos)
    # 超出範圍就反轉膨脹方向
    if not (1 < current_obj["radius"] < 20):
        expansion *= -1
    current_obj["radius"] += expansion
    current_obj["mass"] = current_obj["radius"]
    pygame.draw.circle(window, (255, 0, 0),
                       current_obj["pos"],
                       int(current_obj["radius"]), 0)


# ---- 主迴圈 ----
running = True
while running:
    clock.tick(FPS)
    window.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_a:
                draw_attractions = not draw_attractions
            elif event.key == pygame.K_c:
                collidables.clear()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵：放置新物件
                collidables.append({
                    "pos": Vector2(mouse_pos),
                    "velocity": Vector2(0, 0),
                    "radius": current_obj["radius"],
                    "mass": current_obj["mass"],
                    "colour": random_colour(),
                })

    calculate_movement()
    handle_collisions()
    draw_collidables()
    draw_current_object()

    pygame.display.update()

pygame.quit()
