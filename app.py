from flask import Flask, render_template, request, send_file
import os
import glob
import sys
from mutpy import commandline
from io import StringIO
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./files_test"
app.config['TEMPLATES_AUTO_RELOAD'] = True  # the templates are reloaded to display them in the responses

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        f1 = request.files['fileTarget']  # get the target file
        f2 = request.files['fileTest']    # get the test file
        
        if f1.filename != "" and f2.filename != "": # ensure that two files are uploaded
               
            deletePrev()   # delete the previous files (files_test)
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename)) # save the new target file
            f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename)) # save the new test file

            if confirm(f1.filename, f2.filename): # confirm that the target file is imported into the test file
            
                options = []
                operators = []
                                # get de options
                options.append(request.form.get('timeFactorInput'))  #0    
                options.append(request.form.get('stdoutCheck'))      #1
                options.append(request.form.get('expOperatorCheck')) #2
                options.append(request.form['operatorsRadios'])      #3
                
                if options[3] == "operators": # add the selected operators to the list
                        for i in range(27):
                            operator = request.form.get(str(i))
                            if operator != None:
                                operators.append(operator)
                
                mut(f1.filename, f2.filename, options, operators) # execute the mutation test
                shutil.make_archive('./zips/html_report', 'zip', './templates/html_report') # compress the result html report
                
                return render_template("results.html")            
            else:
                return render_template("home.html", error=[False,True]) # the error list is to display the alerts
        else:
            return render_template("home.html", error=[True,False])
    else:
       return render_template("home.html", error=[False,False])

def mut(f1, f2, options, operators): 
    
    # argList is the list of contains the arguments that mutpy will execute
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
    with Capturing() as output: # text output is captured
        commandline.main(sys.argv)
    f=open("txt_report/report.txt", 'w')
    text=""
    for word in output:
        text += word + "\n"
    f.write(text) # a text file is written with the capture text output
    f.close()
 
@app.route("/html_report")
def html_report():
    return render_template("/html_report/index.html")

@app.route("/txt_report")
def txt_report():
    f = open("txt_report/report.txt", "r")
    return render_template("txt_report.html", text=f.read())

@app.route("/download_html")
def download_html():
    r = "zips/html_report.zip"
    return send_file(r, as_attachment=True)

@app.route("/download_txt")
def download_txt():
    r = "txt_report/report.txt"
    return send_file(r, as_attachment=True)

@app.route("/example_files")
def example_files():
    r = "example_files/example_files.zip"
    return send_file(r, as_attachment=True)

class Capturing(list): # funtion to capture the text outputs
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
  
def deletePrev(): # delete the previous files (files_test)
    files = glob.glob("./files_test/*.py")
    for file in files:
        os.remove(file)

@app.route("/operators")
def operators():
    return render_template("operators.html")

@app.route("/info")
def info():
    return render_template("info.html")

def confirm(f1, f2): # confirm that the target file is imported into the test file
    
    f1 = f1.replace(".py","")
    f = open("./files_test/"+f2, "r")
    f3 = f.read()

    if 'from '+ f1 in f3:
        return True
    else:
        return False

if __name__=="__main__":
    app.run()