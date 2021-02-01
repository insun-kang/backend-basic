## USER API

- register 
  - fullname, email, pw로부터 받은 값을 db에 저장

- login
  - email, pw를 db에서 찾아 일치하는지 여부를 판단하고 session에 값을 저장 후 board 페이지로 넘어감
  - email, pw가 불일치 할 때는 '회원이 아닙니다.', pw가 불일치 할 때는 '비밀번호가 다릅니다.'를 출력시켰습니다.
  - 로그인이 성공했을 시에는 환영 메시지와 함께 board페이지로 넘어가게 됩니다.

- logout
  - 세션값을 비워줌으로써 login해제
  - 로그아웃 성공시 '로그아웃 했습니다.'메시지 출력

## board, boardArticle

-수업시간에 했던 내용을 사용했습니다...

## code(user api)


index.html을 만들어서 그 안에 register, login, logout을 실행 할 수 있게 만들었습니다.


```
import pymysql
from flask import Flask, jsonify, request, render_template, redirect, session, url_for
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

app.secret_key = 'sample_secret'


db = pymysql.connect(host='localhost', user = 'root', passwd = '', db = 'backendproject', charset='utf8')

cursor = db.cursor()



        

"""
User APIs : 유저 SignUp / Login / Logout

"""

# session을 위한 secret_key 설정
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
def home():
    return render_template('index.html')

   

@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        fullname=request.form['fullname']
        email=request.form['email']
        pw=request.form['pw']
        sql = "INSERT INTO member (fullname, email, pw) VALUES (%s, %s, %s)"
        cursor.execute(sql, (fullname, email, pw))
        db.commit()
   
        return redirect(request.url)
    return render_template('index.html')




@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method =='POST':
        email=request.form['email']
        pw=request.form['pw']

        sql = "SELECT * FROM member WHERE email=%s"
        rows_count=cursor.execute(sql, email)

        if rows_count >0:
            user_info=cursor.fetchone()

            if pw==user_info[3]:
                session['email']=email
                return ''' <script> alert("안녕하세요~ {}님"); location.href="/form" </script> '''.format(email)


            else:
                return'비밀번호가 틀렸습니다.'
        else:
            return '회원이 아닙니다.'
    return render_template('index.html')

@app.route('/form')
def form():
    if 'email' in session:
        return redirect(url_for('board'))
    return redirect(url_for('board'))


@app.route('/logout') 
def logout():  
    session.pop('email', None)
    return ''' <script> alert("로그아웃 되었습니다."); location.href="/" </script> '''



# API Resource 라우팅을 등록!
api.add_resource(Board, '/board')
api.add_resource(BoardArticle, '/board/<board_id>', '/board/<board_id>/<board_article_id>')


if __name__ == '__main__':
    app.run()
```
