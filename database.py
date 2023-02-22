from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
db_connection_string = config['db_connection_string']

engine = create_engine(db_connection_string,
    connect_args={
        "ssl":{
            "ssl_ca":"/etc/ssl/cert.pem",
        }
    })

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from data"))
        resAll= result.all()#a python list
        ret = []
        for i in resAll:
            ret.append(dict(i))
        return ret

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from data WHERE id="+id))
        rows= result.all()#a python list
        if not rows:
            return "No job with the id:"+id
        else:
            return dict(rows[0])

def add_job_to_db():
    with engine.connect() as conn:
        query = text("INSERT INTO data (title, location, salary, currency, responsibilities, requirements) VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)")
        conn.execute(query,
                    title='Web Developer', 
                    location='Remote', 
                    salary='600000', 
                    currency='INR', 
                    responsibilities='Lorem ipsum dolor', 
                    requirements='HTML,CSS,JavaScript')
        # return load_jobs_from_db()

#https://note.nkmk.me/en/python-long-string/
def add_application_to_db(job_id,data):
    with engine.connect() as conn:
        query = text("INSERT INTO applications (job_id,first_name,last_name ,email,linkedin_url, education,work_exp,resume_url) VALUES (:job_id,:first_name,:last_name ,:email,:linkedin_url,:education,:work_exp,:resume_url)")
        conn.execute(query,
                job_id=job_id,
                first_name=data['fname'],
                last_name=data['lname'],
                email = data['email'],
                linkedin_url = data['Linkedin'],
                education = data['education'],
                work_exp = data['work'],
                resume_url = data['resume'],)