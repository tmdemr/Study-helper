# -- coding: utf-8 --
# schedulerdao import
from dao import schedulerdao
from flask import Flask, request, render_template, session
import pygame

import pymysql

pygame.init()
app = Flask(__name__)
app.secret_key = 'session_password'
def selectDB(sql_data): #데이터베이스 설정 함수
    conn = pymysql.connect(host='localhost',
                           user='pi',
                           password='raspberry',
                           db='suppoter',
                           charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
     
    # SQL문 실행
    sql = sql_data
    curs.execute(sql)
    
    # 데이타 Fetch
    rows = curs.fetchall()
    # Connection 닫기
    conn.close()
    #print(rows)
    return rows

def signUpDB(user_id, user_password):
    conn = pymysql.connect(host='localhost',
                           user='pi',
                           password='raspberry',
                           db='suppoter',
                           charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
     
    # SQL문 실행
    sql = "insert into user_info values('" + user_id + "', '" + user_password + "')"
    curs.execute(sql)
    
    conn.commit()
    
    # Connection 닫기
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user_id = request.form['loginId']
    user_password = request.form['password']
    
    # selectDB 넣어서 아이디 비밀번호 확인하기
    rows=selectDB("select if(user_password='"+ user_password + "', 1, 0) from user_info where user_id='" + user_id +"'")
    rows=str(rows)
    
    if str(rows[2:3]) == "1":
        session['userid']=request.form['loginId']
        return render_template("loginsuccess.html", check="로그인 성공")
    else :
        return render_template("loginfail.html", check="로그인 실패")
    
    

@app.route("/signUp", methods=["POST"])
def signUp():
    user_id = request.form['loginId']
    user_password = request.form['password']
    
    signUpDB(user_id,user_password)
    
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop('userid', None)
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("user.html")


@app.route('/bar') # bar 그래프 출력 페이지
def bar():
    user_id = session['userid']
    rows=selectDB("select DATE_FORMAT(study_date, '%m월%d일') study_date, TIME_FORMAT(study_time, '%h.%i') study_time from study_manager where id='" + user_id + "'")
    
    date_list = []
    time_list = []
    
    for row in rows:
        study_date = row[0]
        study_time = row[1]
        date_list.append(study_date)
        time_list.append(study_time)

    return render_template('bar_chart.html', title='2020년 공부 시간', max=20, time_data=time_list, date_data=date_list)

# 공부 계획 관리
@app.route("/study_schedule")
def study_schedule():
    return render_template("study_schedule.html")

@app.route("/white_noise")
def white_noise():
    soundObj = pygame.mixer.Sound('/var/www/scheduler/static/music/rain.wav')
    soundObj.play(0)
    return render_template("user.html")

# schedule 처리 get/post로 접근가능
@app.route("/scheduler",methods=["GET","POST","PUT","DELETE"])
def scheduler():
    # 요청이 get이면
    if request.method == 'GET':
        # fullCalendar에서 start와 end를 yyyy-mm-dd 형식의 parameter로 넘겨준다.
        start = request.args.get('start')
        end = request.args.get('end')
        # schedulerdao.getScheduler에 start와 end를 Dictoionary형식으로 넘겨준다.
        return schedulerdao.getScheduler({'start':start , 'end' : end})

    #요청이 post면
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        allDay = request.form['allDay']

        # Dictoionary 형식의 schedule 변수를 만든다. 추후 parameter를 받게 수정예정
        schedule = {'title' : title, 'start' : start, 'end' : end, 'allDay' : allDay}
        # schedule을 입력한다.
        return  schedulerdao.setScheduler(schedule)

    #요청이 delete면
    if request.method == 'DELETE':
        id = request.form['id']
        return  schedulerdao.delScheduler(id)

    #요청이 put이면
    if request.method == 'PUT':
        schedule = request.form
        return schedulerdao.putScheduler(schedule)

if __name__ =='__main__':
    app.run(port=7072, debug='true')
