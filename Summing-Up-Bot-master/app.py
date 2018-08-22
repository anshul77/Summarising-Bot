

from query import QueryService
from flask_restful import Api, Resource, reqparse
from flask import Flask, render_template, send_from_directory, request
from internet_conn import shorten_news, summ_from_text

app = Flask(__name__)
api = Api(app)
api.add_resource(QueryService, '/news_urls')

@app.route("/")
def home():
    return render_template("newlook.html")
#@app.route("/url1", methods = ['GET','POST'])
@app.route("/index",methods=["POST","GET"])
def index():
    print "inside app index"
    return render_template("index.html")

@app.route("/reg2",methods=["POST","GET"])
def reg2():
    return render_template("url.html")

@app.route("/templates",methods=["POST"])
def reg1():
    print "inside app index"
    text = request.form['input_text']
    print text
    var = shorten_news(text)
    print "var"
    print var
    return render_template("url.html",output_summary=var)

@app.route("/reg3",methods=["POST", "GET"])
def reg3():
    return render_template("inputtext.html")
@app.route("/templates1",methods=["POST"])
def reg4():
    print "inside app index"
    text = request.form['input_text']
    print text
    var = summ_from_text(text)
    print "var"
    print var
    return render_template("inputtext.html",output_summary=var)


@app.after_request
def after_request(response):
    print "inside app after_request"
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    try:
        app.run('localhost', port = 5000, debug = True, use_reloader = False)
    except Exception, e:
        print e
