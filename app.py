import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL

from werkzeug.utils import secure_filename
from datetime import datetime
from itertools import groupby
import cv2
import numpy as np
import math
import re

import mysql.connector
from mysql.connector import Error


UPLOAD_FOLDER1 = 'static/request_img'
UPLOAD_FOLDER2 = 'static/response_img'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)

app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2


app.secret_key = 'your secret key'
''''
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'onuorah12'
app.config['MYSQL_DB'] = 'ai_art_db'
 
#db = MySQL(app)


'''

db = mysql.connector.connect(
  host="127.0.0.1",
  database='ai_art_db',
  user="root",
  password="onuorah12"
)

'''
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'learnorg_gbeleyi'
app.config['MYSQL_PASSWORD'] = '5I&QOl[8$0h,'
app.config['MYSQL_DB'] = 'learnorg_gbeleyi_db'
 
#db = MySQL(app)

db = mysql.connector.connect(
  host="localhost",
  database='learnorg_gbeleyi_db',
  user="learnorg_gbeleyi",
  password="5I&QOl[8$0h,"
)
'''




@app.route('/')
def tea():
    #return ("Hello world")    

    #cursor = db.connection.cursor()

    #cursor = db.cursor()

    cursor = db.cursor(buffered=True)

    #count level 1
    lev1 = cursor.execute("SELECT file_name FROM request_sample_tb WHERE level='1' ORDER BY id DESC")    

    #count level 2
    lev2 = cursor.execute("SELECT file_name FROM request_sample_tb WHERE level='2' ORDER BY id DESC")

    #count level 3
    lev3 = cursor.execute("SELECT file_name FROM request_sample_tb WHERE level='3' ORDER BY id DESC")
    

    return render_template("tea.html",cnt1=lev1,cnt2=lev2,cnt3=lev3)




    
@app.route('/home', methods =['GET'])
def index():
    args = request.args
    sel_level = args.get('level')
    #task = request.args.get("task")

    #check for task - DELETE OR UPDATE
    msg=''
    if 'task' in args:   
        if 'loggedin' in session and session['level']=="admin":
            task = args.get('task')
            sel_id = args.get('value')
            if  task == 'del': 
                cursor = db.cursor(buffered=True)
    
                cursor.execute('DELETE FROM request_sample_tb WHERE id = "'+sel_id+'"')              
                db.commit()
                msg="deleted"
           
    #return ("Hello world")    

    #creating variable for connection
   
    cursor = db.cursor(buffered=True)

    #executing query
    cursor.execute("SELECT name,file_name,level,id,description, outlier_limit FROM request_sample_tb WHERE level='"+sel_level+"' ORDER BY id DESC")
    #fetching all records from database
    data=cursor.fetchall()
    


    #second table
    if 'loggedin' in session and session['level']=="user":
        cursor.execute('SELECT * FROM response_tb WHERE user_name = "'+session['username']+'"')
    elif 'loggedin' in session and session['level']=="admin":
        cursor.execute('SELECT * FROM response_tb') #show all user for admin
    else:
        cursor.execute("SELECT * FROM response_tb")
    #fetching all records from database
    data2=cursor.fetchall()

    cursor.close()
    #rows = data()
    #for row in rows:
    #    print(row)

    if sel_level=='1':
        level_text="Still-Life Drawings"
    elif sel_level=='2':
        level_text="Life Drawings"  
    elif sel_level=='3':
        level_text="Biological Drawings"  
    

    #returning back to index.html with all records from MySQL which are stored in variable data    
    return render_template("index.html",val=data, val2=data2, level=level_text, msg=msg)




#LOGIN and REG

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
       
        cursor = db.cursor(buffered=True)

        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['id'] = account['id']
            #session['username'] = account['username']

            session['id'] = account[0]
            session['username'] = account[1]
            session['level'] = account[4]
            msg = 'Logged in successfully !'
            #return render_template('index.html', msg = msg)
            #return render_template('index.html', msg = msg)
            return redirect(url_for('tea'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    msg = ''
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('level', None)
    msg = 'You have logout now'
    #return redirect(url_for('login'))
    return render_template('login.html', msg = msg)
 

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = db.cursor(buffered=True)

        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts (username, password, email, level) VALUES (%s, %s, %s, %s)', (username, password, email, 'user'))
            db.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

    
@app.route('/profile')
def profile():
        # Check if user is loggedin
        if 'loggedin' in session:
            # We need all the account info for the user so we can display it on the profile page
           

            cursor = db.cursor(buffered=True)


            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
            # Show the profile page with account info
            return render_template('profile.html', account=account)
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))

    


@app.route('/adm_add', methods =['GET'])
def adm_add():
    if 'loggedin' in session and session['level']=="admin":

        args = request.args
       
        msg=''
        if 'task' in args:
                task = args.get('task')  
                sel_id = args.get('value')  
               
                cursor = db.cursor(buffered=True)

                cursor.execute('SELECT * FROM request_sample_tb WHERE id = "'+sel_id+'"')  
                data_preview = cursor.fetchone()            
               
                msg="Edit"
              
                return render_template('adm_add.html', preview=data_preview)
        else:
                return render_template('adm_add.html')
        
    else:
        return redirect(url_for('login'))    
    
 
@app.route('/adm_add_process', methods = ['POST', 'GET'])
def adm_add_process():
    if 'loggedin' in session:

        if request.method == 'POST':

            name = request.form['name']
            detail = request.form['detail']
            level = request.form['level']
            
            
            # if user does not select file, browser also
            # submit a empty part without filename

            if "edit_id" in request.form: # Edit Record
                edit_id = request.form['edit_id'] 

               
                cursor = db.cursor(buffered=True)
            
                cursor.execute('UPDATE request_sample_tb SET name="'+name+'", description="'+detail+'" WHERE id = "'+edit_id+'"')              
                db.commit()

             
                return redirect('adm_add?task=edit&value='+edit_id+'&level='+level+'&msg=1')

            else: #Add  Record 

                file=request.files['img1'] 

                if file.filename == '':
                    #flash('No file part')
                    return redirect("adm_add?msg=0")

                #if file and allowed_file(file.filename):       

                now = str(datetime.now())
                filename = secure_filename(now+file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))  


                #------------------------------------ This section set the limit for the outlier -------------------------------        
                path = "static/request_img/"+filename
            
                img1 = cv2.imread(path)
                hh1, ww1 = img1.shape[:2]
                cx1 = ww1 // 2
                cy1 = hh1 // 2

            
                img2 = cv2.imread(path)
                hh2, ww2 = img2.shape[:2]
                cx2 = ww2 // 2
                cy2 = hh2 // 2

                # specify crop size and crop both images
                wd = 1450
                ht = 1450
                xoff = wd // 2
                yoff = ht // 2
                img1_crop = img1[cy1-yoff:cy1+yoff, cx1-xoff:cx1+xoff]
                img2_crop = img2[cy2-yoff:cy2+yoff, cx2-xoff:cx2+xoff]

                # convert to grayscale
                gray1 = cv2.cvtColor(img1_crop,cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(img2_crop,cv2.COLOR_BGR2GRAY)

                # threshold
                thresh1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

                # erode thresh2 to get black lines approx as thick as thresh1
                # apply close and open morphology to fill tiny black and white holes and save as mask
                kernel = np.ones((13,13), np.uint8)
                thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_ERODE, kernel)

                # do shape matching (the smaller the distance the better the match)
                match_diff = cv2.matchShapes(thresh1, thresh2, cv2.CONTOURS_MATCH_I2, 0)

                outlier_limit = round(match_diff,4)  

                #outlier_limit = match_diff 

                req_raw_data=outlier_limit
                #req_raw_data=""

               
                #--------------------------------------------------------------------------   

                
                cursor = db.cursor(buffered=True)

                cursor.execute("INSERT INTO request_sample_tb (file_name, name, description, outlier_limit, req_raw_data, level) VALUES(%s,%s,%s,%s,%s,%s)",(filename, name, detail, outlier_limit, req_raw_data, level))
                db.commit()
                #cursor.close()
                #flash('Done')
                #return f"Done!!"

                return redirect(url_for('adm_add')) 
               

               
 

@app.route("/prediction", methods=["POST"])
#@app.route("/prediction")
def prediction():

    filename1=request.form['img1'] 
    path = "static/request_img/"+filename1
    #img1 = cv2.imread(path)
    #print(path)
   
   

    img2=request.files['img2'] 
    now = str(datetime.now())
    filename2 = secure_filename(now+img2.filename)  

   
    
    img2.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename2)) 
    #img2 = cv2.imread("static/response_img/"+filename2)


    # -----------------------------------------------------------------------------------
    #img1 = cv2.imread('love.jpg')
    img1 = cv2.imread(path)
    hh1, ww1 = img1.shape[:2]
    cx1 = ww1 // 2
    cy1 = hh1 // 2

    # read hand drawn figure and find center
    #img2 = cv2.imread('drawn_figure.jpg')
    img2 = cv2.imread("static/response_img/"+filename2)
    hh2, ww2 = img2.shape[:2]
    cx2 = ww2 // 2
    cy2 = hh2 // 2

    # specify crop size and crop both images
    wd = 1450
    ht = 1450
    xoff = wd // 2
    yoff = ht // 2
    img1_crop = img1[cy1-yoff:cy1+yoff, cx1-xoff:cx1+xoff]
    img2_crop = img2[cy2-yoff:cy2+yoff, cx2-xoff:cx2+xoff]

    # convert to grayscale
    gray1 = cv2.cvtColor(img1_crop,cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_crop,cv2.COLOR_BGR2GRAY)

    # threshold
    thresh1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]   

    # erode thresh2 to get black lines approx as thick as thresh1
    # apply close and open morphology to fill tiny black and white holes and save as mask    
    kernel = np.ones((13,13), np.uint8)
    thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_ERODE, kernel)

    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    #thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel)

    # do shape matching (the smaller the distance the better the match)
    match_diff = cv2.matchShapes(thresh1, thresh2, cv2.CONTOURS_MATCH_I2, 0)
    round_val = round(match_diff,4)

    #cv2.imwrite('thresh1.jpg',thresh1)
    #cv2.imwrite('thresh2.jpg',thresh2)

   
       
   
    #-----------------------------------------------------------------------------------------


    #insert the response details to response_tb
    req_img=filename1    
    res_img = filename2
    diff_value= round_val
    user_name=request.form['user_id'] 
    req_id=request.form['req_id'] 
    level=request.form['level'] 
    date_saved = datetime.now()

    
    cursor = db.cursor(buffered=True)

    cursor.execute("INSERT INTO response_tb (request_img , user_response_img, diff_value, user_name,request_id,date_saved) VALUES(%s,%s,%s,%s,%s,%s)",(req_img, res_img, diff_value, user_name, req_id, date_saved))
    db.commit()

    #return render_template("prediction.html",data = str(round_val))
    return redirect("more?id="+req_id+"&level="+level+"&page=1")

    #cv2.waitKey(0)




# Helper function for pagination using MySQL cursor

@app.route('/more', methods = ['GET'])
def more():
    args = request.args
    req_id = args.get('id')
    level = args.get('level')
    
   
    if level=='1':
        level_name="Still-Life Drawings"
    elif level=='2':
        level_name="Life Drawings" 
    elif level=='3':
        level_name="Biological Drawings" 

    #check for task - DELETE OR UPDATE
    msg=''
    if 'task' in args:   
        if 'loggedin' in session and session['level']=="admin":
            task = args.get('task')
            value = args.get('value')
            if  task == 'del':      
                
                cursor = db.cursor(buffered=True)
   
                cursor.execute('DELETE FROM response_tb WHERE id = "'+value+'"')              
                db.commit()
                msg="deleted"

    
    conn = db.cursor(buffered=True)

    #executing query
    conn.execute('SELECT * FROM request_sample_tb WHERE id='+req_id+'')
   
    request_record = conn.fetchall()
    data=request_record

    #-----------Pagination-------------   
    page = int(args.get('page'))
    per_page = 10
    elem_to_display = per_page
    offset = (page - 1) * elem_to_display

    if 'loggedin' in session and session['level']=="user":
        conn.execute('SELECT * FROM response_tb WHERE request_id='+req_id+' AND user_name = "'+session['username']+'" ORDER BY id DESC')
    elif 'loggedin' in session and session['level']=="admin":
        #conn.execute('SELECT * FROM response_tb WHERE request_id='+req_id+' ORDER BY id DESC')
        conn.execute('SELECT * FROM response_tb WHERE request_id='+req_id+' ORDER BY id DESC LIMIT %s OFFSET %s', (elem_to_display, offset,))
   
    else:
        #conn.execute('SELECT * FROM response_tb WHERE request_id='+req_id+' ORDER BY id DESC')
        conn.execute('SELECT * FROM response_tb WHERE request_id='+req_id+' ORDER BY id DESC LIMIT %s OFFSET %s', (elem_to_display, offset,))

    
    response_record = conn.fetchall()
    data2=response_record


    conn.execute('SELECT COUNT(*) FROM response_tb WHERE request_id='+req_id+'')
    total_items = conn.fetchone()[0]

    total_pages = (total_items + per_page - 1) // per_page
   
    return render_template('more.html', request=data, response=data2, page=page, total_pages=total_pages, msg=msg, id=req_id,level=level,level_value=level_name)

    #return render_template("more.html",data=req_id)
   
if __name__ == "__main__":
    app.run(debug=True)