import pymysql
from flask import Flask, jsonify, request, render_template, redirect, session, url_for
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

app.secret_key = 'sample_secret'


db = pymysql.connect(host='localhost', user = 'root', passwd = '', db = 'backendproject', charset='utf8')

cursor = db.cursor()


parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')


class Board(Resource):
    def get(self):
        sql = "SELECT id, name FROM `board`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)
        
    
    def post(self):
        args = parser.parse_args()
        sql = "INSERT INTO `board` (`name`) VALUES (%s)"
        cursor.execute(sql, (args['name']))
        db.commit()
        
        return jsonify(status = "success", result = {"name": args["name"]})
        
    def put(self):
        args = parser.parse_args()
        sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
        cursor.execute(sql, (args['name'], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"], "name": args["name"]})
    
    
    def delete(self):
        args = parser.parse_args()
        sql = "DELETE FROM `board` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})


parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('content')
parser.add_argument('board_id')


class BoardArticle(Resource):
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `id`=%s"
            cursor.execute(sql, (board_article_id,))
            result = cursor.fetchone()
        else:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `board_id`=%s"
            cursor.execute(sql, (board_id,))
            result = cursor.fetchall()
            
        return jsonify(status = "success", result = result)

    def post(self, board_id=None):
        args = parser.parse_args()
        sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['title'], args['content'], args['board_id']))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"]})
        
        
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "UPDATE `boardArticle` SET title = %s, content = %s WHERE `id` = %s"
        cursor.execute(sql, (args['title'], args["content"], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"], "content": args["content"]})
        
        
    def delete(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
        cursor.execute(sql, (args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})
        

"""
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.
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
        sql = "INSERT INTO member (fullname,    email, pw) VALUES (%s, %s, %s)"
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
    return render_template('index.html')


@app.route('/logout') 
def logout():
    session.pop('user', None)
    return redirect(url_for('form'))





# API Resource 라우팅을 등록!
api.add_resource(Board, '/board')
api.add_resource(BoardArticle, '/board/<board_id>', '/board/<board_id>/<board_article_id>')


if __name__ == '__main__':
    app.run()
