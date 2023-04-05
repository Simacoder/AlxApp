import datetime
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, title, body):
        self.title = title
        self.body = body 


class ReportSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


report_schema =  ReportSchema()
reports_schema =  ReportSchema(many = True)



@app.route('/get', methods = ['GET'])

def get_reports():
    all_reports = Reports.query.all()
    results = report_schema.dump(all_reports)
    return jsonify(results)


@app.route('/get/<id>/', methods = ['GET'])
def  post_details(id):
     report = Reports.query.get(id)
     return report_schema.jsonify(report)

@app.route('/add', methods = ['POST'])
def add_reports():
    title = request.json['title']
    body = request.json['body']


    reports = Reports(title, body)
    db.session.add(reports)
    db.session.commit()
    return report_schema.jsonify(reports)



@app.route('/update/<id>/', methods = ['PUT'])
def update_reports(id):
    report = Reports.query.get(id)

    title = request.json['title']
    body = request.json['body']

    report.title = title
    report.body = body

    db.session.commit()
    return report_schema.jsonify(report)

@app.route('/delete/<id>/', methods = ['DELETE'])
def report_delete(id):
    report = Reports.query.get(id)
    db.session.delete(report)
    db.session.commit()

    return report_schema.jsonify(report)

if __name__ == "__main__":
    app.run(debug= True)
