from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, timedelta
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen
#pip install elementpath
import xml.etree.ElementTree as ElementTree
from urllib.parse import unquote
import pandas as pd 
import numpy as np
import datetime
import os
    
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://rfenexdq:CZbuZcBazut5dn0xwcXXvyXo7OuqOzc6@arjuna.db.elephantsql.com:5432/rfenexdq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.secret_key = 'aaa!111/'

####################### 클래스 생성 ###################################
class purpose(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    purpose_ex = db.Column(db.String(50))
    users = db.relationship('user', backref='purpose', lazy='dynamic')
    

class user(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(10))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    purpose_id=db.Column(db.String(50), db.ForeignKey('purpose.id'))


class abandonment_jeonju(db.Model):
    desertionNo = db.Column(db.String(50), primary_key=True)
    sexCd = db.Column(db.String(50))
    processState = db.Column(db.String(50))
    neuterYn = db.Column(db.String(50))
    specialMark = db.Column(db.String(200))
    careNm = db.Column(db.String(50))
    orgNm= db.Column(db.String(50))
    happenDt= db.Column(db.String(50))
    happenPlace=db.Column(db.String(150))
    kindCd=db.Column(db.String(50))
    colorCd=db.Column(db.String(50))
    age=db.Column(db.String(50))
    weight=db.Column(db.String(50))
    noticeEdt=db.Column(db.String(50))
    noticeSdt=db.Column(db.String(50))





####################### api 생성 ##############################

def doAction():

    ServiceKey =unquote('X4n1g5BDRmhABgrgNzNq3OYDVUOeslwuRL6ix9gA8E8rs5OAZUcY19tmS%2FTCLLWHKU7ozh1UTxMA5Pk1EQgk%2BA%3D%3D')

    global startday
    startday = date.today()
    url = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic'
    queryParams = '?' + urlencode({quote_plus('ServiceKey') : ServiceKey, quote_plus('org_cd'): '4640000',quote_plus('endde') : startday.strftime('%Y%m%d'), quote_plus('bgnde') : '20180308',quote_plus('numOfRows'):'1000' })


    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    #print (response_body)

    tree = ElementTree.ElementTree(ElementTree.fromstring(response_body))
    #print(tree)

    rootNode = tree.getroot()
    #print(rootNode)

    itemList = rootNode.getiterator('item')
    #print(itemList)

    for x in itemList:
        desertionNo = x.findtext('desertionNo')
        db_abandonment = abandonment_jeonju.query.filter_by(desertionNo=desertionNo).first()

        if db_abandonment is None :
            orgNm=x.findtext('orgNm')
            sexCd = x.findtext('sexCd')
            processState = x.findtext('processState')
            neuterYn = x.findtext('neuterYn')
            specialMark = x.findtext('specialMark')
            careNm = x.findtext('careNm')
            happenDt=x.findtext('happenDt')
            happenPlace=x.findtext('happenPlace')
            kindCd=x.findtext('kindCd')
            colorCd=x.findtext('colorCd')
            age=x.findtext('age')
            weight=x.findtext('weight')
            noticeEdt=x.findtext('noticeEdt')
            noticeSdt=x.findtext('noticeSdt')

            _abandonment_ = abandonment_jeonju(desertionNo=desertionNo,sexCd=sexCd,processState=processState,neuterYn=neuterYn,specialMark=specialMark,
            careNm=careNm,orgNm=orgNm,happenDt=happenDt,happenPlace=happenPlace,kindCd=kindCd,colorCd=colorCd,age=age,weight=weight,noticeEdt=noticeEdt,noticeSdt=noticeSdt)
        
            db.session.add(_abandonment_)
            db.session.commit()
            print(happenDt)
        else: break
    return 100

doAction()



####################### @app 생성 ##############################
@app.route('/register', methods=['POST','GET'])
def register():
    data = {}

    if request.method == 'GET':
        data['purposes'] = purpose.query.all()
        return render_template('register.html', **data)
    
    elif request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        purpose_id = request.form['purpose_id']

        _user_ = user(name=name, age=age, email=email, password=password, purpose_id=purpose_id)
        db.session.add(_user_)
        db.session.commit()

        print('name: {}'.format(name))
        print('age: {}'.format(age))
        print('email: {}'.format(email))
        print('password: {}'.format(password))
        print('purpose_id: {}'.format(purpose_id))

        return ''' <script> alert("축하합니다! {}님의 회원가입이 완료되었습니다."); location.href="/" </script> '''.format(name)





@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        _email_ = request.form['email']
        _password_ = request.form['password']

        userdb = user.query.filter_by(email=_email_, password=_password_).first()

        if userdb is not None:
            _name_ = userdb.name
            session['email']=_email_
            session['name']=_name_
            return ''' <script> alert("{}님, 환영합니다."); location.href="/index" </script> '''.format(_name_)

        else:
            return ''' <script> alert("일치하는 정보가 없습니다. 다시 시도해주세요."); location.href="/" </script> '''




@app.route('/index')
def index():
    data={}
    doAction()
    lastday=startday-timedelta(days=30)
    data['mnth_adopt'] = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt<=startday.strftime('%Y%m%d')).filter(abandonment_jeonju.happenDt>=lastday.strftime('%Y%m%d')).filter(abandonment_jeonju.processState.like('%입양%')).count()    
    data['mnth_number'] = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt<=startday.strftime('%Y%m%d')).filter(abandonment_jeonju.happenDt>=lastday.strftime('%Y%m%d')).count()
    
    May = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202005%')).count()
    Jun = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202006%')).count()
    Jul = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202007%')).count()
    Aug = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202008%')).count()
    Sep = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202009%')).count()
    Oct = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202010%')).count()
    Nov = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202011%')).count()
    Dec = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202012%')).count()
    Jan21 = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202101%')).count()  
    Feb21 = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202102%')).count()
    Mar21 = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202103%')).count()
    Apr21 = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202104%')).count()
    May21 = abandonment_jeonju.query.filter(abandonment_jeonju.happenDt.like('202105%')).count()

    if 'name' in session:
        return render_template('index.html', name = session.get("name"), login=True, **data, data={"May":May, "Jun":Jun, "Jul":Jul, "Aug":Aug, "Sep":Sep, "Oct":Oct, "Nov":Nov, "Dec":Dec, "Jan21":Jan21, "Feb21":Feb21, "Mar21":Mar21,"May21":May21, "Apr21":Apr21 } )
    
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop("email")
    session.pop("name")

    return redirect('/')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/cards')
def cards():
    return render_template('cards.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')
# pip install gunicorn
# pip freeze >requirements.txt



if __name__=='__main__':
    app.run(port=5000, debug=True)