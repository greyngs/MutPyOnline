from flask import Flask, render_template, request
import os
import glob
import sys
from mutpy import commandline
from io import StringIO
import shutil

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
        operators = []
        
        options.append(request.form.get('timeFactorInput'))  #0
        options.append(request.form.get('stdoutCheck'))      #1
        options.append(request.form.get('expOperatorCheck')) #2
        options.append(request.form['operatorsRadios'])      #3
        
        if options[3] == "operators":
                for i in range(27):
                    operator = request.form.get(str(i))
                    if operator != None:
                        operators.append(operator)
        
        mut(f1.filename, f2.filename, options, operators)
        shutil.make_archive('./zips/html_report', 'zip', './templates/html_report')
        
        return render_template("home.html")
    else:
       return render_template("home.html")

def mut(f1, f2, options, operators): 
    
    argList = ['mut.py', '-t', './files_test/'+f1, '-u', './files_test/'+f2, '-m', '--report-html', 'templates/html_report', '--coverage']
    
    argList.append('-f')
    argList.append(options[0])
    
    if options[1] == "stdout":
        argList.append('-d')

    if options[2] == "expOperators":
        argList.append('-e')

    if options[3] == "operators":
        argList.append('-o')
        for op in operators:
            argList.append(op)
    
    sys.argv = argList
    with Capturing() as output:
        commandline.main(sys.argv)
    f=open("txt_report/report.txt", 'w')
    text=""
    for word in output:
        text += word + "\n"
    f.write(text)
    f.close()
 
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
  
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