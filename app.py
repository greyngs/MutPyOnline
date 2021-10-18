from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./files_test"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        f1 = request.files['fileTarget']
        f2 = request.files['fileTest']
        
        if f1.filename != "" and f2.filename != "":
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
            f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))
            
        return render_template("home.html")
    else:
       return render_template("home.html") 

@app.route("/operators")
def operators():
    return render_template("operators.html")

@app.route("/info")
def info():
    return render_template("info.html")


if __name__=="__main__":
    app.run()