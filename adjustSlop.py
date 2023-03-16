# can use random testing and metamorphic testing later
def adjustSlop(xList, yList,error):
    y_adjust = []
    pre_x = 0
    pre_y = 0
    pre_y_adjust = 0
    for i in range(0,len(xList) - 1):
        x1 = xList[i]
        y1 = yList[i]
        #print("index:" , i,  "y1; x1:",y1,",", x1)
        k1 = (y1 - pre_y) / (x1 - pre_x)
        k2 = k1 + float(error)
        #k2 = k1
        y2 = k2 * (x1 - pre_x) + pre_y_adjust
        pre_x = x1
        pre_y = y1
        pre_y_adjust = y2
        y_adjust.append(y2)

    return y_adjust