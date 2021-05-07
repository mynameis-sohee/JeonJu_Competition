# from __init__ import db,abandonment_jeonju
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template, request, redirect, url_for, session
# from datetime import datetime, timedelta
# from urllib.parse import quote_plus, urlencode
# from urllib.request import Request, urlopen
# #pip install elementpath
# import xml.etree.ElementTree as ElementTree
# from urllib.parse import unquote
# import pandas as pd 
# import numpy as np
# import datetime    

# def doAction():
#     today_number = 0
#     today_kind_dog = 0
#     today_kind_cat = 0
#     today_kind_others = 0
    
#     ServiceKey =unquote('X4n1g5BDRmhABgrgNzNq3OYDVUOeslwuRL6ix9gA8E8rs5OAZUcY19tmS%2FTCLLWHKU7ozh1UTxMA5Pk1EQgk%2BA%3D%3D')

#     startday= datetime.datetime.today().strftime('%Y%m%d')
#     url = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic'
#     queryParams = '?' + urlencode({quote_plus('ServiceKey') : ServiceKey, quote_plus('org_cd'): '4640000',quote_plus('endde') : startday, quote_plus('bgnde') : '20180308',quote_plus('numOfRows'):'1000' })


#     request = Request(url + queryParams)
#     request.get_method = lambda: 'GET'
#     response_body = urlopen(request).read()
#     #print (response_body)

#     tree = ElementTree.ElementTree(ElementTree.fromstring(response_body))
#     #print(tree)

#     rootNode = tree.getroot()
#     #print(rootNode)

#     itemList = rootNode.getiterator('item')
#     #print(itemList)

#     for x in itemList:
#         desertionNo = x.findtext('desertionNo')
#         db_abandonment = abandonment_jeonju.query.filter_by(desertionNo=desertionNo).first()

#         if db_abandonment is None :
#             orgNm=x.findtext('orgNm')
#             sexCd = x.findtext('sexCd')
#             processState = x.findtext('processState')
#             neuterYn = x.findtext('neuterYn')
#             specialMark = x.findtext('specialMark')
#             careNm = x.findtext('careNm')
#             happenDt=x.findtext('happenDt')
#             happenPlace=x.findtext('happenPlace')
#             kindCd=x.findtext('kindCd')
#             colorCd=x.findtext('colorCd')
#             age=x.findtext('age')
#             weight=x.findtext('weight')
#             noticeEdt=x.findtext('noticeEdt')
#             noticeSdt=x.findtext('noticeSdt')

#             _abandonment_ = abandonment_jeonju(desertionNo=desertionNo,sexCd=sexCd,processState=processState,neuterYn=neuterYn,specialMark=specialMark,
#             careNm=careNm,orgNm=orgNm,happenDt=happenDt,happenPlace=happenPlace,kindCd=kindCd,colorCd=colorCd,age=age,weight=weight,noticeEdt=noticeEdt,noticeSdt=noticeSdt)
        
#             db.session.add(_abandonment_)
#             db.session.commit()
#             print(happenDt)
#         else: break
#     return 100

# doAction()



# # 엑셀데이터를 DB에 저장
# import pandas as pd
# import numpy
# data = pd.read_csv("C:/Users/sohee/data.csv")

# for i in range(0,len(data)):
#     desertionNo=data.iloc[i,:]['desertionNo'].astype(str)
#     noticeSdt=data.iloc[i,:]['noticeSdt'].astype(str)
#     noticeEdt=data.iloc[i,:]['noticeEdt'].astype(str)
#     careNm=data.iloc[i,:]['careNm']
#     happenDt=data.iloc[i,:]['happenDt'].astype(str)
#     happenPlace=data.iloc[i,:]['happenPlace']
#     colorCd=data.iloc[i,:]['colorCd']
#     sexCd=data.iloc[i,:]['sexCd']
#     weight=data.iloc[i,:]['weight']
#     age=data.iloc[i,:]['age']
#     neuterYn=data.iloc[i,:]['neuterYn']
#     kindCd=data.iloc[i,:]['kindCd']
#     processState=data.iloc[i,:]['processState']
    
#     _abandonment_ = abandonment(desertionNo=desertionNo,sexCd=sexCd,processState=processState,
#                                 neuterYn=neuterYn,careNm=careNm,orgNm='전라북도 전주시',
#                                 happenDt=happenDt,happenPlace=happenPlace,kindCd=kindCd,colorCd=colorCd,
#                                 age=age,weight=weight,noticeEdt=noticeEdt,noticeSdt=noticeSdt)
#     db.session.add(_abandonment_)
#     db.session.commit()



import pandas
import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://rfenexdq:CZbuZcBazut5dn0xwcXXvyXo7OuqOzc6@arjuna.db.elephantsql.com:5432/rfenexdq')
df = pandas.read_sql("SELECT * FROM abandonment_jeonju", con = engine)

df.drop(['desertionNo'],axis=1, inplace=True)
#print(df['sexCd'].value_counts()) # Q: 잘 모르는 것. 빈도가 매우 적지만 기타축종 등에는 해당되므로 냅둬야함

#입양
#print(df['processState'].value_counts())

#보호중+반환된 셀은 삭제해야겠죠? 유기가 된 동물들 중 입양될 가능성을 보는거니까. 나머지의 경우는 모두 합치는게 바람직하죠.
excep_1= df['processState']!='보호중'
excep_2= df['processState']!='종료(반환)'
df=df[excep_1 & excep_2]

#print(df['neuterYn'].value_counts()) #미상도 존재함 비율은 안한 아이들이 더 많음. 요인이 치우쳐져 있다.

df.drop(['specialMark'],axis=1, inplace=True)

#print(df['careNm'].value_counts())
#print(df['orgNm'].value_counts())
df.drop(['orgNm'],axis=1, inplace=True)

df['happenDt']=df['happenDt'].astype(int)

#print(df.info())
#print(df[df['kindCd'].str.contains('개')]['kindCd'].value_counts()) # 개 :믹스견과 품종견으로 나눔
#print(df[df['kindCd'].str.contains('고양이')]['kindCd'].value_counts()) # 한국 고양이와 품종묘로 나눔


#for i in range(0, len(df[df['kindCd'].str.contains('개')])):
#    if df['kindCd'].iloc[i,:].str.contains('[개] 믹스견') == 
#    else : df[df['kindCd'].str.contains('개')].iloc[i,:]['kindCd'] ='품종견'


df["kindCd"] = df["kindCd"].apply(lambda x: '믹스견' if x=="[개] 믹스견" else ('품종견' if ("개" in x) else ('한국묘' if (x=="[고양이] 한국 고양이") else '품종묘')))

#print(df["colorCd"].unique()) -> 예외가 많으므로 어떻게 처리할지 고민. 우선 삭제
df.drop(['colorCd'],axis=1, inplace=True)

df['age']=df['age'].str.replace("년생",'').str.replace("(",'').str.replace(")",'').astype(int)
df['age']=df['happenDt'].astype(str).str[:4].astype(int)-df['age']+1 # 발견년도 기준 나이

#df['weight']=df['weight'].str.replace("Kg",'').str.replace("(",'').str.replace(")",'') : 예외가 많으므로 우선 제거
df.drop(['weight'],axis=1, inplace=True)

df['noticeEdt']=df['noticeEdt'].astype(int)
df['noticeSdt']=df['noticeSdt'].astype(int)


############ 전처리 완료

## 모델링

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder,LabelEncoder
from sklearn.metrics import accuracy_score, plot_confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import mean_absolute_error
from random import *


df.reset_index(drop=True,inplace=True)
#df=pandas.get_dummies(df)


train,test=train_test_split(df, test_size=0.2)

target='processState'
X_train, X_val, y_train, y_val = train_test_split(train.drop([target],axis=1), train[target], test_size=0.2)
for i in X_train, X_val, y_train, y_val : i.reset_index(inplace=True, drop=True)


pipe_ordinal = make_pipeline(
    OrdinalEncoder(),
    RandomForestClassifier())

dists = {
    'randomforestclassifier__max_depth': range(10,15),
    'randomforestclassifier__min_samples_leaf': range(2,10)}

clf = GridSearchCV(
    pipe_ordinal, 
    param_grid=dists, 
    cv=2,
    scoring='accuracy'
)

clf.fit(X_train, y_train)
print('최적 하이퍼파라미터: ', clf.best_params_)
pipe_ordinal = clf.best_estimator_
pipe_ordinal.fit(X_train, y_train)

gb = pipe_ordinal.named_steps['randomforestclassifier']
importances = pandas.Series(gb.feature_importances_, X_test.columns)
print(importances)

pred = pipe_ordinal.predict(X_val)
print(accuracy_score(pred, y_val))