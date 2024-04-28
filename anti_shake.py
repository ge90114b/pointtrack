import math
lastx = 0
lasty = 0

max=300

def antishake(coordinate,first):
    global lastx, lasty, is_first_call,max
    if first:
        lastx, lasty = coordinate
        return coordinate
    else:
        if abs(coordinate[0] - lastx) > max:
            x = lastx
        else:
            x = coordinate[0]
        if abs(coordinate[1] - lasty) > max:
            y = lasty
        else:
            y = coordinate[1]
        return [x, y]
if __name__=="__main__":
    while 1:
        a=float(input())
        b=float(input())
        print(antishake([a,b]))

        