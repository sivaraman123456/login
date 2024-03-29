from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3

app=Flask(__name__)
app.secret_key="123"

@app.route('/')
def home():
    return render_template("home.html")
#-----------------------------------------------------------------------------------
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        pass1=request.form['pass1']
        con=sqlite3.connect("data.db")
        cur=con.cursor()
        cur.execute("select * from stud where Name=? and phone=?",(name,pass1))
        data=cur.fetchone()
        if data:
            return redirect("view")
        else:
            flash("Value mismatch","danger")
    return render_template("home.html")

#-----------------------------------------------------------------------------------
@app.route("/view")
def view():
    con=sqlite3.connect("data.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from stud ")
    data=cur.fetchall()
    return render_template("view.html",data=data)

#-----------------------------------------------------------------------------------

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            email=request.form['email']
            phone=request.form['phone']
            birth=request.form['birth']
            address=request.form['address']
            con=sqlite3.connect("data.db")
            
            con.execute("create table  if not exists stud  (pid integer primary key,Name text,email text,phone integer,birth date,address text )")
            cur=con.cursor()
            cur.execute(''' insert into stud (Name,email,phone,birth,address)values(?,?,?,?,?)''',
                        (name,email,phone,birth,address))
            con.commit()
            flash("Data inserted successfully","success")

        except:
            flash("Data Not inserted ","danger")

        finally:
            return redirect(url_for('home'))
            con.close()

    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)
