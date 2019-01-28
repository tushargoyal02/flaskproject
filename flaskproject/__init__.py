from flask import Flask , render_template
from contentManagement import content
TOPIC_DICT = content()


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("main.html")

#THIS IS FOR OUR START LEARNING(dual decoator as same as dashboad )
#@app.route("/slashboard/") 
@app.route("/dashboard/")
def dashboard():
  #   WE ARE PASSING VALUES FROM OUR PAGE TO HERE IN TOPIC_DICT(change in dashboard.html)
   return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)


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




if __name__ == "__main__":
    app.run(debug=True)
