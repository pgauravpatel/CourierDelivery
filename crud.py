from flask import Flask,redirect,render_template,request,jsonify,url_for,session,flash
import sqlite3
import json
import base64

with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app=Flask(__name__)
app.secret_key= "something can be"

# First Page 
@app.route('/')
def first_page():
    conn=sqlite3.connect("CourierD.db")
    cur = conn.cursor()
    cur.execute("select * from rate")
    pa=cur.fetchall()
    global p
    p=pa[-1][2]
    return render_template('first_page.html')

#User Page start....
@app.route('/user')
def user_page():
    
    return render_template('user.html', p=p)
    
@app.route('/calculate', methods=['GET'])
def calculate():
    weight = request.args.get('weight')
    distance = request.args.get('distance')
    global rate
    rate= float(weight)+float(distance) * float(p)
    return jsonify({'rate': rate})
    
    
@app.route("/user_details",methods = ["POST","GET"])  
def user_details():  
    msg = "msg"  
    if request.method == "POST":  
        p_name = request.form["name"]  
        p_email = request.form["email"]  
        p_address = request.form["address"]
        p_phone = (int(request.form["phone"]))
        weight=request.form['weight']
        distance=request.form['distance']
        d_name = request.form["name1"]  
        d_email = request.form["email1"]  
        d_address = request.form["address1"]
        d_phone = (int(request.form["phone1"]))
        d_file= request.files['file1']
        img=d_file.read()
        con=sqlite3.connect("CourierD.db")  
        cur = con.cursor()  
        cur.execute("INSERT INTO 'mytable' (pname, pemail, pphone, paddress, dname, demail, dphone, daddress, dphoto, weight, distance,cost) values (?,?,?,?,?,?,?,?,?,?,?,?)",(p_name,p_email,p_phone,p_address,d_name,d_email,d_phone,d_address,img,weight,distance,rate))  
        con.commit()  
        msg = "Order successfully completed" 
        return redirect(url_for("success")) 
    
@app.route("/user_details/success")
def success():
    return render_template("success.html")

#User Page End.....


#Admin Page Start.......
    #Admin login/logout....
@app.route("/admin", methods=['GET', 'POST'])
def login():
    
    # if('user' in session and session['user'] == params['uname']):
    #     return render_template('dashboard.html', params=params)
    
    if request.method=='POST':
        username= request.form.get('usname')
        userpass= request.form.get('upass')
        if(username==params['uname'] and userpass==params['upass']):
            session['user']= username
            return redirect(url_for("Index", params=params))
        
        else:
            return render_template('admin_login.html')
    else:
            return render_template('admin_login.html')
    
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    
    if('user' in session and session['user'] == params['uname']):
        session.pop('user', None)
        
        return redirect(url_for('login'))
    
   #Admin login/logout END....
   
@app.route('/admin/dashboard')
def Index():
    if('user' in session and session['user'] == params['uname']):
        con=sqlite3.connect("CourierD.db")
        cur=con.cursor()
        cur.execute("SELECT  * FROM 'mytable'")
        data = cur.fetchall()
        photos=[]
        for photo in data:
            x= photo[9]
            photo_base64=base64.b64encode(x).decode()
            photos.append(photo_base64)
        
        cur.close()




        return render_template('admin_page.html', client=data, photos=photos,p=p  )



@app.route("/insert",methods = ["POST","GET"])  
def insert():  
    if('user' in session and session['user'] == params['uname']): 
        if request.method == "POST":  
            if request.method == "POST":  
                p_name = request.form["name"]  
                p_email = request.form["email"]  
                p_address = request.form["address"]
                p_phone = (int(request.form["phone"]))
                weight=request.form['weight']
                distance=request.form['distance']
                d_name = request.form["name1"]  
                d_email = request.form["email1"]  
                d_address = request.form["address1"]
                d_phone = (int(request.form["phone1"]))
                d_file= request.files['file1']
                img=d_file.read()
        
                con=sqlite3.connect("CourierD.db")
                
                cur = con.cursor()  
                cur.execute("INSERT INTO 'mytable' (pname, pemail, pphone, paddress, dname, demail, dphone, daddress, dphoto, weight, distance,cost) values (?,?,?,?,?,?,?,?,?,?,?,?)",(p_name,p_email,p_phone,p_address,d_name,d_email,d_phone,d_address,img,weight,distance,rate))  
                con.commit()  
                msg = "Order successfully completed" 
                return redirect(url_for("Index")) 




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    if('user' in session and session['user'] == params['uname']):
        
        
        flash("Record Has Been Deleted Successfully")
        con=sqlite3.connect("CourierD.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM mytable WHERE id=?", (id_data,))
        selected_row=cur.fetchone()
        
        cur.execute("INSERT INTO binOrder (id,pname, pemail, pphone, paddress, dname, demail, dphone, daddress, dphoto, weight, distance,cost,remarks,ddate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", selected_row )
        cur.execute("DELETE FROM 'mytable' WHERE id=?", (id_data,))
        con.commit()
        return redirect(url_for('Index'))
    
@app.route('/admin/recycleBin')
def recycleBin():
    
    con=sqlite3.connect("CourierD.db")
    cur=con.cursor()
    cur.execute("SELECT  * FROM binOrder ")
    data = cur.fetchall()
    photos=[]
    for photo in data:
        x= photo[9]
        photo_base64=base64.b64encode(x).decode()
        photos.append(photo_base64)
        
        cur.close()
    
    return render_template('recycleBin.html', client=data, photos=photos)

@app.route('/deleteRecycle/<string:id_data>', methods = ['GET'])
def deleteRecycle(id_data):
    if('user' in session and session['user'] == params['uname']):
        
        con=sqlite3.connect("CourierD.db")
        cur=con.cursor()
        
        cur.execute("DELETE FROM binOrder WHERE id=?", (id_data,))
        con.commit()
        return redirect(url_for('recycleBin'))
    
@app.route('/restore/<string:id_data>', methods = ['GET'])
def restore(id_data):
    if('user' in session and session['user'] == params['uname']):
        
        con=sqlite3.connect("CourierD.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM binOrder WHERE id=?", (id_data,))
        selected_row=cur.fetchone()
        
        cur.execute("INSERT INTO mytable (id,pname, pemail, pphone, paddress, dname, demail, dphone, daddress, dphoto, weight, distance,cost,remarks,ddate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", selected_row )
        cur.execute("DELETE FROM binOrder WHERE id=?", (id_data,))
        con.commit()
        return redirect(url_for('recycleBin'))





@app.route('/update',methods=['POST','GET'])
def update():
    if('user' in session and session['user'] == params['uname']):

        if request.method == "POST":  
            id= request.form['id']
            p_name = request.form["name"]  
            p_email = request.form["email"]  
            p_address = request.form["address"]
            p_phone = (int(request.form["phone"]))
            weight=request.form['weight']
            distance=request.form['distance']
            d_name = request.form["name1"]  
            d_email = request.form["email1"]  
            d_address = request.form["address1"]
            d_phone = (request.form["phone1"])
            remark=request.form['remark']
            delivery_date=request.form['delivery_date']
            
            rate=request.form['rate']
            con=sqlite3.connect("CourierD.db")
            cur=con.cursor()
            cur.execute("""
                UPDATE 'mytable'
                SET pname=?, pemail=?, pphone=?, paddress=?, dname=?, demail=?, dphone=?, daddress=?, weight=?, distance=?, cost=?, remarks=?, ddate=? 
                WHERE id=?
                """, (p_name,p_email,p_phone,p_address,d_name,d_email,d_phone,d_address,weight,distance,rate,remark,delivery_date,id))
            flash("Data Updated Successfully")
            con.commit()
            return redirect(url_for('Index'))
    
@app.route('/admin/add_rates', methods=['GET', 'POST'])
def add_rates():
    if('user' in session and session['user'] == params['uname']):
        if request.method == 'POST':
            weight = request.form['weight']
            distance = request.form['distance']
            rate_admin = request.form['rate']
            conn=sqlite3.connect("CourierD.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO rate(weight, distance, rate) values (?,?,?)",(weight,distance,rate_admin))  
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('Index'))

        
            
if __name__=="__main__":
    app.run(debug=True)
    
    
    

    


