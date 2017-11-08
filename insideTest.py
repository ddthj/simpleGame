

square = [(0,0),
          (10,0),
          (10,10),
          (0,10)]
p = (10,0)


    def inside(point,obj):
    cords = obj
    counts = 0
    for x in range(len(cords)-1):
        if x+1 <= len(cords):
            a = cords[x]
            b = cords[x+1]
        else:
            a = cords[x]
            b = cords[0]

        if a[1] >= point[1] >= b[1] or a[1] <= point[1] <= b[1]:
            if a[0] >= point[0] and b[0] >= point[0]:
                counts += 1
    print(counts)
    if counts % 2 != 0:
        return True
    return False
    
print(inside(p,square))
