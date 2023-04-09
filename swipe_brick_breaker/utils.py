import math

def intersects(rect1, rect2):
    ''' Intersects function '''
    left1 = rect1[0]
    right1 = rect1[0] + rect1[2]
    top1 = rect1[1]
    bottom1 = rect1[1] + rect1[3]

    left2 = rect2[0]
    right2 = rect2[0] + rect2[2]
    top2 = rect2[1]
    bottom2 = rect2[1] + rect2[3]    

    return not (right1 <= left2 or
                left1 >= right2 or
                bottom1 <= top2 or
                top1 >= bottom2)

def remove_collided_objects(blocks: list):
    ''' this removes the blocks when all of the hits have been made '''
    to_remove = []

    for b in blocks:
        if b.hits <= 0:
            to_remove.append(b)


    for t in to_remove:
        blocks.remove(t)

def get_vel(bx, by, mx, my, speed):
    ''' this gets the ball slope from the mouse click '''
    a = mx - bx
    b = my - by
    c = math.sqrt((a**2) + (b**2))

    vx = int(speed) * (a/c)
    vy = int(speed) * (b/c)

    return vx, vy