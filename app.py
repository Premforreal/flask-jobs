from flask import Flask,render_template,jsonify,request,url_for,redirect
from database import load_jobs_from_db,add_job_to_db,load_job_from_db,add_application_to_db
app = Flask(__name__) #name: how the script is invoked

@app.route('/')
def home():
    arr = load_jobs_from_db()
    return render_template('home.html',jobs=arr)
 
#https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405
#https://stackoverflow.com/questions/9871705/to-display-this-page-firefox-must-send-information-that-will-repeat-any-action
@app.route('/',methods=['POST'])
def addJob():
    data  = request.form
    add_job_to_db(data)
    return(redirect('/'))

@app.route('/jobs/<id>')
def showJob(id):
    arr=load_job_from_db(id)
    # return redirect(url_for('home'))
    return render_template('job.html',job=arr)

@app.route('/jobs/<id>/apply',methods=['post'])
def apply(id):
    job=load_job_from_db(id)
    data  = request.form
    for i in data:
        if not data[i]:
            return ("<p>Error! Please fill out the necessary fields</p>")
    add_application_to_db(id, data)
    return render_template('submitted.html',application=data,job=job)


@app.route('/api/jobs')
def returnJSON():
    arr = load_jobs_from_db()
    return jsonify(arr)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)