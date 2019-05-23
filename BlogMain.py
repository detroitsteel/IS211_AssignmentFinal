#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controller for Website Brain Blog"""

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
postsinlist = {}
uname = ''
pp = ''
loggy = False
curuserid = 0
post_id = 0
loginerror = 'Username and Password Incorrect, Please try again'

def credvalid(uid, pww):
    loggy = False
    with lite.connect('blog.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM usr;")
        rows = cur.fetchall()
        for row in rows:
            if uid == row[1]:
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
        cur.execute("select p.p_id, u.uid, u.u_id, p.title, p.pub_date, "
                    "p.poot from post p left join usr u on p.u_id = u.u_id ")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                postlist[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
    return

def postsinload(uname):
    with lite.connect('blog.db') as con:
        cur = con.cursor()
        cur.execute("select p.p_id, u.uid, u.u_id, p.title, p.pub_date, "
                    "p.poot from post p left join usr u on p.u_id = u.u_id "
                    "where u.uid =  ? order by p.pub_date desc"
                    , (uname,))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                postsinlist[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
                global curuserid
                curuserid = int(row[2])
    return

###############Start HTTP Routing###############################################

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
        curdte = datetime.today()
        try:
            if title == '' or poot == '':
                InErr = 'Incorrect Value Enterd, Try Again'
                app.logger.error(InErr)
                raise Exception(InErr)
            else:
                with lite.connect('blog.db') as con1:
                    cur1 = con1.cursor()
                    cur1.execute("INSERT INTO post(u_id, title, pub_date, poot)"
                                 " VALUES(?, ?, ?, ?);"
                                 , (curuserid, title, curdte, poot))
                postsinload(uname)
                return render_template('dashboard.html', postlist = postsinlist)
        except(Exception) as e:
            postsinload(uname)
            error = 'SQL Insert Error, Please Try Again.'
            return render_template('./add.html', error = e)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/edtpost', methods = ['GET'])
def edtpostlink():
    if loggy:
        global post_id
        post_id = int(request.args.get('p_id'))
        epostlist = [postsinlist[post_id]]
        return render_template('./edit.html', postlist = epostlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/edtpost', methods = ['POST'])
def edtpost():
    if loggy:    
        title = request.form['title']
        poot = request.form['poot']
        curdte = datetime.today()
        try:
            if title == '' or poot == '':
                InErr = 'Incorrect Value Enterd, Try Again'
                app.logger.error(InErr)
                raise Exception(InErr)
            else:
                with lite.connect('blog.db') as con1:
                    cur1 = con1.cursor()
                    cur1.execute("UPDATE post SET title = ?, pub_date = ? "
                                 ", poot = ? where p_id = ?;"
                                 , (title, curdte, poot, post_id))
                postsinload(uname)
                return render_template('dashboard.html', postlist = postsinlist)
        except(Exception) as e:
            postsinload(uname)
            error = 'SQL Insert Error, Please Try Again.'
            return render_template('./add.html', error = e)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/dltpost', methods = ['GET'])
def dltpostlink():
    if loggy:
        global post_id
        post_id = int(request.args.get('p_id'))
        epostlist = [postsinlist[post_id]]
        return render_template('./delete.html', postlist = epostlist)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)

@app.route('/dltpost', methods = ['POST'])
def dltpost():
    if loggy:    
        try:
            with lite.connect('blog.db') as con1:
                cur1 = con1.cursor()
                cur1.execute("DELETE FROM post where p_id = ?;", (post_id,))
            global postsinlist
            postsinlist = {}
            postsinload(uname)
            return render_template('dashboard.html', postlist = postsinlist)
        except(Exception) as e:
            postsinload(uname)
            error = 'SQL Insert Error, Please Try Again.'
            return render_template('./delete.html', error = e)
    else:
        app.logger.error(loginerror, uname, pp)
        return render_template('login.html', error = loginerror)
##########################  End of HTTP Handlers################################
if __name__ == '__main__':
    postload()
    app.run()
