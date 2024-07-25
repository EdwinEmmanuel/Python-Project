from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)
#MySQL Connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="accord"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#Loading Home Page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql="SELECT * FROM billing"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)

#New User
@app.route("/AddUsers",methods=['Get','Post'])
def AddUsers():
    if request.method=='Post':
        medname=request.form['medname']
        mobile=request.form['mobile']
        quantity=request.form['quantity']
        price=request.form['price']
        con=mysql.connection.cursor()
        sql="insert into billing (MedName,Mobile,Quantity,Price) value (%s,%s,%s,%s)"
        con.execute(sql,[medname,mobile,quantity,price])
        mysql.connection.commit()
        con.close()
        flash('User Details Updated')
        return redirect(url_for("home.html"))
    return render_template("AddUsers.html")
#update user
@app.route("/edituser/<string:medcode>",methods=['Get','Post'])

def edituser(medcode):
    con=mysql.connection.cursor()
    if request.method=='Post':
        medname=request.form['medname']
        mobile=request.form['mobile']
        quantity=request.form['quantity']
        price=request.form['price']
        sql="update billing set Medname=%s,Mobile=%s,Quantity=%s,Price=%s"
        con.execute(sql,[medname,mobile,quantity,price])
        mysql.connection.commit()
        con.close()
        flash('User Details Updated')
        return redirect(url_for("home.html"))
        con=mysql.connection.cursor()
    sql="select * from billing where medcode=%s"
    con.execute(sql,[medcode])
    res=con.fetchone()
    return render_template("edituser.html",datas=res)
    
@app.route("/edituser/<string:medcode>",methods=['Get','Post'])
#Delete User
def deleteUser():
    con=mysql.connection.cursor()
    sql="delete from billing where medcode=%s"
    con.execute(sql,medcode)
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect("home") 

if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)