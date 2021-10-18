from flask import Flask, render_template, request
import os
import glob

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./files_test"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        f1 = request.files['fileTarget']
        f2 = request.files['fileTest']
        
        if f1.filename != "" and f2.filename != "":
            deletePrev()
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
            f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))
            
        options = []
            
        options.append(request.form.get('timeFactorInput'))  #0
        options.append(request.form.get('stdoutCheck'))      #1
        options.append(request.form.get('expOperatorCheck')) #2
        options.append(request.form['operatorsRadios'])      #3
            
        return render_template("home.html")
    else:
       return render_template("home.html")
   
def deletePrev():
    files = glob.glob("./files_test/*.py")
    for file in files:
        os.remove(file)

@app.route("/operators")
def operators():
    return render_template("operators.html")

@app.route("/info")
def info():
    return render_template("info.html")


if __name__=="__main__":
    app.run()