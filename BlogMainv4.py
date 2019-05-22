#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controller for Website Todo List with Form"""

import re
import logging
from logging import FileHandler
import traceback
import sqlite3 as lite
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
file_handler = FileHandler("./logfile.log")
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
con = None
postlist = {}
postlist1 = ()
postsinlist = {}
postsinlist1 = ()
qzlist = {}
qzscrlist = {}
uname = ''
pp = ''
loggy = False
curuserid = 0
loginerror = 'Username and Password Incorrect, Please try again'

def credvalid(uid, pww):
    loggy = False
    with lite.connect('blog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM usr;")
        rows = cur.fetchall()
        print (rows, rows[1])
        for row in rows:
            print (row, row[1], row[2])
            if uid == row[1]:
                print row[1]
                if pww == row[2]:
                    global loggy
                    loggy = True
                    return loggy
                else:
                    global loggy
                    loggy = False
                    return loggy
        global loggy
        loggy = False
        return loggy
    
def postload():
    with lite.connect('blog.db') as con:
        cur = con.cursor()
        cur.execute("select u.uid, p.p_id, p.title, p.pub_date, p.poot "
                    "from usrPost up "
                    "left join usr u "
                    "on u.u_id = up.u_id "
                    "left join post p "
                    "on p.p_id = up.p_id "
                    "order by p.pub_date desc")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                postlist[row[0]] = [row[1], row[2], row[3], row[4]]
            print postlist
            print (sorted(postlist.items(), key = lambda kv:(kv[1], kv[0])))
            postlist1 = sorted(postlist.items(), key = lambda kv:(kv[1], kv[0]))
            print postlist1
    return

def postsinload(uname):
    with lite.connect('blog.db') as con:
        cur = con.cursor()
        cur.execute("select u.uid, p.p_id, p.title, p.pub_date, p.poot "
                    "from usrPost up "
                    "left join usr u "
                    "on u.u_id = up.u_id "
                    "left join post p "
                    "on p.p_id = up.p_id "
                    "where u.uid = ?", (uname,))
                    #"order by p.pub_date desc"
        rows = cur.fetchall()
        print ('11111111111111111111111111111111', uname)
        if rows:
            for row in rows:
                postsinlist[row[0]] = [row[1], row[2], row[3], row[4]]
            print ('((()()()()()()()()(', postsinlist[uname][0])
            print (sorted(postsinlist.items(), key = lambda kv:(kv[1], kv[0])))
            #postsinlist1 = sorted(postsinlist.items(), key = lambda kv:(kv[1], kv[0]))
            #print postsinlist1
    return
################################################################################
def qzload():
    with lite.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM quiz")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                qzlist[row[0]] = [row[1], row[2], row[3]]

    return

def qzscrload(stuid):
    print type(stuid)
    qzscrlist.clear()
    rwct = 0
    with lite.connect('hw13.db') as con:
        cur = con.cursor()
        cur.execute("SELECT s.id, s.first_name, s.last_name, q.subject, "
                     "q.q_date, qs.score FROM students s left join "
                     "quizScore qs on qs.stu_id = s.id left join quiz q "
                     "on q.id = qs.q_id where s.id = ?", (stuid))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                qzscrlist[rwct] = [row[0], row[1], row[2], row[3],
                row[4], row[5]]
                rwct += 1
    return 

################################################################################

@app.route('/')
def home():
    return render_template('home.html', postlist = postlist)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods = ['POST'])
def logincheck():
    global uname
    uname = request.form['Username']
    global pp
    pp = request.form['Password']
    credvalid(uname, pp)
    if loggy:
        print ('**********************************', uname)
        postsinload(uname)
        postsingle = postsinlist
        return render_template('dashboard.html', postlist = postsingle)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)
    
@app.route('/addpost')
def newpostlink():
    if loggy:
        return render_template('./add.html')
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addpost', methods = ['POST'])
def addpost():
    if loggy:    
        title = request.form['title']
        poot = request.form['poot']
        curdte = datetime.now()
        curuserid = int(postsinlist[uname][0])
        try:
            if title == '' or poot == '':
                InErr = 'Incorrect Value Enterd, Try Again'
                app.logger.error(InErr)
                raise Exception(InErr)
            else:
                with lite.connect('blog.db') as con1:
                    cur1 = con1.cursor()
                    cur1.execute("INSERT INTO post(title, pub_date, poot) "
                                 "VALUES(?, ?, ?);"
                                 , (title, curdte, poot))
                    cur1.execute("INSERT INTO usrPost(title, pub_date, poot) "
                                 "VALUES(?, ?, ?);"
                                 , (title, curdte, poot))
                    
                postsinload(uname)
                return render_template('dashboard.html', postlist = postsinlist)
        except(Exception) as e:
            postsinload(uname)
            error = 'SQL Insert Error, Please Try Again.'
            return render_template('./add.html', error = e)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addqz')
def qzurlink():
    if loggy:
        return render_template('./quiz/addqz.html', qzlist = qzlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addqz', methods = ['POST'])
def addqz():
    if loggy:
        try:
            QzSub = request.form['QzSubj']
            QCnt = int(request.form['QCnt'])
            QzDte = request.form['QzDte']
            with lite.connect('hw13.db') as con1:
                cur1 = con1.cursor()
                cur1.execute("INSERT INTO quiz(subject, q_cnt, q_date) VALUES(?, ?, ?);"
                             , (QzSub, QCnt, QzDte))
            qzload()
            return render_template('./quiz/addqz.html', qzlist = qzlist)
        except Exception as e:
            qzload()
            app.logger.error(traceback.format_exc())
            err = 'Invalid Entry, Please Try Again'
            return render_template('./quiz/addqz.html', qzlist = qzlist,
                                   error = err)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)
    
@app.route('/viewstu', methods = ['GET'])
def stuqzurlink():
    if loggy:
        stuid = request.args.get('stuid')
        qzscrload(stuid)
        return render_template('./student/viewstu.html', stuvwlist = qzscrlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addstuqz')
def stuqzuraddlink():
    if loggy:
        stuidlist = stulist.keys()
        qzidlist = qzlist.keys()
        return render_template('./results/addstuqz.html', stulist = stulist
                               , qzlist = qzidlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/addstuqz', methods = ['Post'])
def SaveStuQz():
    if loggy:
        try:
            stuid = request.form['StuID']
            qzuid = request.form['QzID']
            qzscr = request.form['QzScr']
            with lite.connect('hw13.db') as con1:
                cur1 = con1.cursor()
                cur1.execute("INSERT INTO quizScore (stu_id, q_id, score) "
                             "VALUES(?, ?, ?);", (stuid, qzuid, qzscr))
            return render_template('./results/addstuqz.html',stulist = stulist
                                   ,qzlist = qzlist)#redirect('/login')
        except Exception as e:
            app.logger.error(traceback.format_exc())
            err = 'Invalid Entry, Please Try Again'
            return render_template('./results/addstuqz.html',stulist = stulist
                                   ,qzlist = qzlist, error = err)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

if __name__ == '__main__':
    postload()
    qzload()
    app.run()
