from flask import Flask , render_template,flash, url_for , request,redirect,session
# url_for is used to get the url for a function
# render_template is for redirecting and flask is send the msg(pop up)
from contentManagement import content
TOPIC_DICT = content()

# TO GET CONNECTED TO DATABASE
from dbconnect import connection

#FOR SIGNUP FORM WE NEED WTFORMS(used to make form in python)
from wtforms import Form,TextField,validators, ValidationError,PasswordField,BooleanField

#for hashing the value of password
from passlib.hash import sha256_crypt

# to remove sql injection
from pymysql import escape_string as thwart
import gc


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("main.html")

#THIS IS FOR OUR START LEARNING(dual decoator as same as dashboad )
#@app.route("/slashboard/") 
@app.route("/dashboard/")
def dashboard():
  #WE ARE PASSING VALUES FROM OUR PAGE TO HERE IN TOPIC_DICT(change in dashboard.html)
   return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)

# ---------------------------------------------------------------

@app.route("/header/")
def header():
  #return ("This is our dashboard")
   return render_template("header.html")


@app.errorhandler(404)
def page_not_found(e):
  #return ("This is our dashboard")
   return render_template("404.html")


@app.route("/slashboard/")
def slashboard():
   try:
      return render_template("dashboard.html",TOPIC_DICT=slas)
   except Exception as e:
      return render_template("500.html",error=e)
  #return ("This is our dashboard")
   return render_template("404.html")

# -------------------------------------------------

class registerform(Form):
   username = TextField('Username',[validators.Length(min=3,max=20)])
   email = TextField('Email',[validators.Length(min=8,max=60)])
   password = PasswordField('Password',[validators.Required(),
                        validators.EqualTo('confirm',message="Password doesnt match!")])

   confirm = PasswordField('Repeat Password')
# the below field is for the checkbox
   accept_tos =  BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)',[validators.Required()])



@app.route("/register/", methods = ["GET","POST"])
def register_page():
   try:
      cur,conn = connection()
      
      form = RegistrationForm(request.form)

# below mean that form is POST and Validated as required
      if request.method == "POST" and form.validate():
         username = form.username.data 
         email = form.email.data
         password = sha256_crypt.encrypt((str(form.password.data)))
         
         #CHECKING THAT WHETHER WE HAVE ANY USER WITH THIS NAME IN DATABASE
               #thwart(username)=> impiles we are not allowing to execute more querries(sql injection)
         x = cur.execute("SELECT * FROM project WHERE username = (%s)",(thwart(username)))
         if int(len(x)) > 0:
            print("This username is already taken! Try some other name.")
            return render_template("register.html",form=form)

         else :
            cur.execute("INSERT INTO project (username,password,email,tracking) VALUES (%s,%s,%s,%s)",
                        (thwart(username),thwart(password),thwart(email),thwart("introduction-to-python-programming")))

            conn.commit()
            cur.close()
            conn.close()
            gc.collect() # to save memory basically we import gc but neccessary

            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
      
      #if nothing of above statements get executed   
      return render_template("register.html",form=form)
      #return("hii")

   except Exception as e:
      return(str(e))
      
#----------------------------------------------------------------------------------------

# WE ARE USING GET AND POST METHOD
@app.route("/login/", methods = ["GET","POST"])
def login_page():
   error=None
   try:
      if request.method == "POST":
         attempt_username = request.form['username']
         attempt_password = request.form['password']
         
         #print(attempt_username)
         flash(attempt_username)

      # it will keep on moving to dashboard because if function is going on!!
         if attempt_username =="admin" and attempt_password == "password":
            return redirect(url_for('dashboard'))   # it will move for the dashboard function(which will show its path)

         else:
            error = "Invalid Credinatial !! Please try it again later."

      return render_template("login.html")



   except Exception as e:
      flash(e)
      return render_template("login.html" , error = error) #error is used to show the error for debugging
   

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
