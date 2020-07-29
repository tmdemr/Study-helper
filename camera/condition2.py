""" 조건2. 기준시간(15초) 동안  눈을 감은 비율이 높다면 Warning
    Value값이 낮을 수 록 안정                               """
import queue

time = 15 #(단위 : Sec) 큐의 길이
limit = 0.35

q=queue.Queue()

def calcTrueRatio():
    countTrue=0
    countFalse=0
    additional=0

    for i in range(q.qsize()):
        if(q.queue[i]==True):
            countTrue += 1
            additional += additionalPoint(q.qsize(),i)
        else:
            countFalse += 1

    try:
        ratio = (countTrue + additional) / q.qsize()
    except ZeroDivisionError:#0으로 나눌시 발생하는 예외처리
        return float(0)

    return ratio

def additionalPoint(qLen,i):
    """큐를 4개의 영역으로 나누어 오래된 큐영역은 additionalPoint를 적게,
       최근의 큐영역는 additionalPoint를 많이 부여하여 즉각적인 신뢰성을 높임
       """
    section = 1
    while(True):
        if(i>=(qLen/4)*section):
            section += 1
        else:
            break

    if(section==1):
        return 0
    elif(section==2):
        return 0.15
    elif(section==3):
        return 0.30
    else:
        return 0.45

def controlQueueLen(fps):
    """프레임에 비례하여 큐의 길이를 가변적으로 조절
        ex) FPS = 1, QueueLen = 15
            FPS = 2, QueueLen = 30      즉 FPS*Time = QueueLen
            FPS = 12, QueueLen = 180
    """
    while(q.qsize() > time*fps):
        q.get()#Out First Queue

def updateTime(value):
    global time
    time = float(value)

def updateLimit(value):
    global limit
    limit = int(value)/100

def checkCondition(value):
    global limit

    if (value >= limit):
        return True

