""" 조건1. 기준시간(2초) 동안 눈을 감으면  Warning
    Value값이 낮을 수 록 안정                  """

time = 2 #(단위 : Sec) 기준시간

def addValue(value,fps):
    """"프레임에 비례한 숫자 증가"""
    add = (100/time) / fps
    value += add
    return  min_max(value)

def subValue(value,fps):
    """"프레임에 비례한 숫자 감소"""
    sub = (100/time) / fps
    value -= sub
    return min_max(value)

def min_max(value):
    if(value>100):
       value=100.0
    elif(value<0):
        value=0.0
    return value

def updateTime(value):
    global time
    time = float(value)

def checkCondition(value):
    limit = 100
    if(value>=limit):
        return True