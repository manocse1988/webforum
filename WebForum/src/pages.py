"""
Author: Manoj Kumar Panneer Selvam
Purpose: This module has all the business logic to process web request created using OOPS and annotation model
"""
from src.share import dbconnect
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_restful import Api
from flask_cors import *

app = Flask(__name__,template_folder="../templates/")
api = Api(app)
CORS(app)

class pages():

    @app.route("/login/",)
    def login():
        return render_template('login.html')

    @app.route("/",)
    def index():
        return render_template('index.html')

    @app.route("/topicpage/",methods=["GET", "POST"])
    def topicpage():
        return render_template('topicpage.html')

    @app.route("/main/",methods=["GET", "POST"])
    def mainpage():
        return render_template('main.html')

    @app.route("/signup/",methods=["GET", "POST"])
    def signup():
        userdetails = {}
        return render_template('signup.html',data=userdetails)

    def recordfilter(resultset):
        recpair = {}
        records = resultset

        for rec in range(len(records)):
            vcount = str(rec)
            recpair[vcount] = records[rec]

        return recpair

    def getTopicPanel(pusername,ptopicid,ptopicname,pemoji,pcolor):
        return '<div id="rowtopic" class="row" style="' + pcolor + '">' \
               '<div class="col-md-2 ml-8"><li class="fas">&#xf007;</i>' + pusername.strip() + '</div>' \
               '<div class="col-md-9 ml-8" id="' + str(ptopicid) + '">' \
               '<a href="javascript:getposts(' + str(ptopicid) + ',\'' + ptopicname.strip() + '\',0, 24' + ')">' + ptopicname.strip() + '</a>' \
               '</div>' \
               '<div class="col-md-1 ml-8" id="emoji' + str(ptopicid) + '">' \
               '<a href="javascript:favoritefunc(' + str(ptopicid) +')">' + pemoji + '</a>' \
               '</div>' \
               '</div>'


    def getTextArea(ptopicid, ptopicname, pmin, pmax, pmaxrecords):
        return  '<ul class="pager">' \
                '<li class="previous"><a href="javascript:pager(\'pre\',' + ptopicid + ',\'' +  ptopicname.strip() + '\',' + str(pmin) + ',' + str(pmax) + ',' + str(pmaxrecords) + ')">Previous</a></li>' \
                '<li class="next"><a href="javascript:pager(\'nxt\',' + ptopicid + ',\'' +  ptopicname.strip() + '\',' + str(pmin) + ',' + str(pmax) + ',' + str(pmaxrecords) + ')">Next</a></li></ul>'\
                '<div class="form-group" id="postcomnt">' \
                '<textarea class="form-control" rows="4" id="comment"></textarea><div style="padding: 5px;"></div>' \
                '<input id="btnpostcomnt" type="button" onclick="javascript:fpostcomnt(' + ptopicid + ',\'' +  ptopicname.strip() + '\')" value="Post Comment" class="btn btn-primary btn-sm" />' \
                '</div>'


    @app.route("/createuser/",methods=["POST"])
    def createuser():
        try:
            content = {}

            content = dict(request.values)

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "insert into wusers values( '" + content['wusername']  + "','" + \
                                                     content['wpassword']  + "','" + \
                                                     content['wfirstname'] + "','" + \
                                                     content['wlastname']  + "','" + \
                                                     content['wemail']     + "')"
            cursor.execute(query)

            connectparam.commit()

            dbconnect.fdisconnect(connectparam)

            return "<h2> " + content['wusername'] + " - User created successfully!! </h2> <a href=" + url_for('index') + "> Login </a>",  200
        except:
            return "Caught technical error",  200

    @app.route("/searchtopic/",methods=["GET", "POST"])
    def searchtopic():
        try:
            ptopicname = request.args.get('topicname')

            vuserid = request.args.get('userid')

            content = '<div>'

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wusers.wusername, topicid, topicname from " \
                    "(topics left join wusers on topics.wuserid = wusers.wuserid) where topics.topicname like '%" + ptopicname + "%'"

            query1 = "select * from favoritetopic where favoritetopic.wuserid = " + vuserid

            cursor.execute(query)

            results = cursor.fetchall()

            cursor.execute(query1)

            results1 = cursor.fetchall()

            switch = "head"

            dbconnect.fdisconnect(connectparam)

            if results:
                for vusername, vtopicid, vtopicname in results:

                    for vftopicid, vfuserid in results1:
                        if vftopicid == vtopicid:
                            vemoji = '<li class="em em-heart" style="align: right;"></li>'
                            break
                    else:
                        vemoji = '<li class="em em-orange_heart" style="align: right;"></li>'

                    if switch == "head":
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavender;")
                        switch = "body"
                    else:
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavenderblush;")
                        switch = "head"

                content = content + "</div>"

                return content,  200
            else:
                return "No results found...",  200

        except:
            return "Caught technical error",  200

    @app.route("/modifyuser/",methods=["GET", "POST"])
    def modifyuser():
        try:
            content = {}

            content = dict(request.values)

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "update wusers set wusername ='" + content['wusername']  + "', " + \
                                      "wpassword ='" + content['wpassword']  + "', " + \
                                      "wfirstname ='" + content['wfirstname']  + "', " + \
                                      "wlastname ='" + content['wlastname']  + "', " + \
                                      "email ='" + content['wemail']  + "' WHERE wuserid = " + content['userid']

            cursor.execute(query)

            connectparam.commit()

            dbconnect.fdisconnect(connectparam)

            return "<h2> User modified successfully!! </h2>",  200
        except:
            return "Caught technical error",  200

    @app.route("/createtopic/",methods=["GET", "POST"])
    def createtopic():
        try:
            content = {}

            content = dict(request.values)

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "insert into topics values( '" + content['topicname']  + "','"  + \
                                                    "false"                +  "','" + \
                                                    content['userid']      + "')"
            cursor.execute(query)

            connectparam.commit()

            dbconnect.fdisconnect(connectparam)

            return "<h2> Topic added successfully!! </h2>",  200
        except:
            return "Caught technical error",  200

    @app.route('/authorize/',methods=["GET", "POST"])
    def authorize():
        try:
             pusername = request.form["wusername"]
             ppassword = request.form["wpassword"]

             if pusername == "":
                 return render_template('index.html')

             connectparam = dbconnect.fconnect()

             cursor = connectparam.cursor()

             cursor.execute("select wuserid from wusers where wusername = '" + pusername + "'" + " and wpassword = '" + ppassword + "'")

             query = cursor.fetchone()

             dbconnect.fdisconnect(connectparam)

             if query:
                 return redirect(url_for('mainpage', username=pusername,userid=query[0]))
             else:
                 return render_template('index.html')
        except:
            return "Caught technical error",  200

    @app.route("/userprofile/",methods=["GET", "POST"])
    def userprofile():
        try:
            querystring = {}

            querystring = dict(request.values)

            vuserid = querystring["userid"]

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wfirstname, wlastname, email, wusername, wpassword from" \
                    " wusers where wusers.wuserid = " + vuserid

            cursor.execute(query)

            results = cursor.fetchall()

            dbconnect.fdisconnect(connectparam)

            userdetails = {"wfirstname": str(results[0][0]).strip() ,
                           "wlastname": str(results[0][1]).strip(),
                           "wemail": str(results[0][2]).strip(),
                           "wusername": str(results[0][3]).strip(),
                           "wpassword": str(results[0][4]).strip()}

            return render_template('signup.html', data=userdetails)

        except:
            return "Caught technical error",  200

    @app.route("/gettopics/",methods=["GET"])
    def gettopics():
        try:
            querystring = {}

            querystring = dict(request.values)

            content = '<div>'

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wusers.wfirstname, topics.topicid, topics.topicname from " \
                    "topics join wusers on topics.wuserid = wusers.wuserid"

            query1 = "select * from favoritetopic where favoritetopic.wuserid = " + querystring["userid"]

            cursor.execute(query)

            results = cursor.fetchall()

            cursor.execute(query1)

            results1 = cursor.fetchall()

            dbconnect.fdisconnect(connectparam)

            switch = "head"

            if results:
                for vusername, vtopicid, vtopicname in results:

                    for vftopicid, vfuserid in results1:
                        if vftopicid == vtopicid:
                            vemoji = '<li class="em em-heart" style="align: right;"></li>'
                            break
                    else:
                        vemoji = '<li class="em em-orange_heart" style="align: right;"></li>'

                    if switch == "head":
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavender;")
                        switch = "body"
                    else:
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavenderblush;")
                        switch = "head"

                content += "</div>"

                return content,  200
            else:
                return "No topics found",  200
        except:
            return "Caught technical error",  200

    @app.route("/mytopics/",methods=["GET"])
    def mytopics():
        try:
            vuserid = request.args.get('userid')

            content = '<div>'

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wusers.wfirstname, topicid, topicname from " \
                    "(topics left join wusers on topics.wuserid = wusers.wuserid) where topics.wuserid=" + vuserid

            query1 = "select * from favoritetopic where favoritetopic.wuserid = " + vuserid

            cursor.execute(query)

            results = cursor.fetchall()

            cursor.execute(query1)

            results1 = cursor.fetchall()

            dbconnect.fdisconnect(connectparam)

            switch = "head"

            if results:
                for vusername, vtopicid, vtopicname in results:

                    for vftopicid, vfuserid in results1:
                        if vftopicid == vtopicid:
                            vemoji = '<li class="em em-heart" style="align: right;"></li>'
                            break
                    else:
                        vemoji = '<li class="em em-orange_heart" style="align: right;"></li>'

                    if switch == "head":
                        content = content + pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavender;")
                        switch = "body"
                    else:
                        content = content + pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavenderblush;")
                        switch = "head"

                content = content + "</div>"

                return content,  200
            else:
                return "No topics found",  200

        except:
            return "Caught technical error",  200

    @app.route("/myfavorites/",methods=["GET"])
    def myfavorites():
        try:
            vuserid = request.args.get('userid')

            content = '<div>'

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wusers.wfirstname, favoritetopic.topicid, topics.topicname  " \
                    "from ((favoritetopic left join topics on favoritetopic.topicid = topics.topicid) " \
                    "left join wusers on topics.wuserid = wusers.wuserid) where favoritetopic.wuserid = " + str(vuserid)

            cursor.execute(query)

            results = cursor.fetchall()

            dbconnect.fdisconnect(connectparam)

            switch = "head"

            if results:
                for vusername, vtopicid, vtopicname in results:

                    vemoji = '<li class="em em-heart" style="align: right;"></li>'

                    if switch == "head":
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavender;")
                        switch = "body"
                    else:
                        content += pages.getTopicPanel(vusername,vtopicid,vtopicname,vemoji,"background-color:lavenderblush;")
                        switch = "head"

                content = content + "</div>"

                return content,  200
            else:
                return "No favorite topics found...",  200
        except:
            return "Caught technical error",  200

    @app.route("/postfavorite/",methods=["POST"])
    def postfavorite():
        try:
            content = {}

            content = dict(request.values)

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select * from favoritetopic where " \
                    "favoritetopic.wuserid = " + content['userid'] + " and favoritetopic.topicid = " + content['topicid']

            cursor.execute(query)

            results = cursor.fetchone()

            if results:
                query = "delete from favoritetopic where " \
                        "favoritetopic.wuserid = " + content['userid'] + " and favoritetopic.topicid = " + content['topicid']

                cursor.execute(query)

                connectparam.commit()

                dbconnect.fdisconnect(connectparam)

                return "Deleted",  200
            else:
                query = "insert into favoritetopic values( '" + content['topicid']  + "','" + \
                                                                content['userid']      + "')"
                cursor.execute(query)

                connectparam.commit()

                dbconnect.fdisconnect(connectparam)

                return "Added",  200
        except:
            return "Caught technical error",  200

    @app.route("/getposts/",methods=["get"])
    def getposts():
        try:
            querystring = {}

            querystring = dict(request.values)

            vtopicid = str(querystring["topicid"])

            vtopicname = str(querystring["topicname"])

            vmin = int(querystring["minindex"])

            vmax = int(querystring["maxindex"])

            content = '<div id="postlist">'

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "select wusers.wfirstname, topicpost.string2 from " \
                    "(topicpost left join wusers on topicpost.wuserid = wusers.wuserid) where topicpost.topicid = " + vtopicid

            cursor.execute(query)

            results = tuple(cursor.fetchall())

            query = "select count(*) from topicpost where topicpost.topicid = " + vtopicid

            cursor.execute(query)

            recordcount = cursor.fetchall()

            resultdict = pages.recordfilter(results)

            dbconnect.fdisconnect(connectparam)

            switch = "head"

            if results:
                for num in range(vmin, vmax - 1):
                    if str(num) in resultdict.keys():
                        vusername = resultdict[str(num)][0]
                        vValue = resultdict[str(num)][1]

                        if switch == "head":
                            content = content + '<div id="rowtopic" class="row" style="background-color:lavender;"><div class="col-md-2 ml-8"><li class="fas">&#xf007;</i>' + vusername.strip() + '</div><div class="col-md-9 ml-8">' + vValue.strip() + '</div></div>'
                            switch = "body"
                        else:
                            content = content + '<div id="rowtopic" class="row" style="background-color:lavenderblush;"><div class="col-md-2 ml-8"><li class="fas">&#xf007;</i>' + vusername.strip() + '</div><div class="col-md-9 ml-8">' + vValue.strip()  + '</div></div>'
                            switch = "head"

                content = content + "</div>"

                content += pages.getTextArea(vtopicid, vtopicname, vmin, vmax, int(recordcount[0][0]))

                return content,  200
            else:
                content = "No posts found for this topic..."
                content += pages.getTextArea(vtopicid, vtopicname, vmin, vmax, int(recordcount[0][0]))
                return content,  200
        except:
            return "Caught technical error",  200

    @app.route("/postcomnt/",methods=["post"])
    def postcomnt():
        try:
            content = {}

            content = dict(request.values)

            connectparam = dbconnect.fconnect()

            cursor = connectparam.cursor()

            query = "insert into topicpost (topicid,string2,wuserid) values( '" + content['topicid']  + "','" + \
                                                                                  content['comments']  + "','" + \
                                                                                  content['userid'] + "')"
            cursor.execute(query)

            connectparam.commit()

            dbconnect.fdisconnect(connectparam)

            return "<h2> Comments created successfully!! </h2>",  200
        except:
            return "Caught technical error",  200

if __name__ == "__main__":
    app.run()