from app import app,models, db
from forms import goal_form, strategy_form, project_form, task_form,DeleteRow_form,ldapA,LoginForm, Request, Which,Staff
import datetime
from sqlalchemy.orm.attributes import get_history
from werkzeug import secure_filename
import re, shutil, os, sys
from sqlalchemy.sql import func
from sqlalchemy import case
from sqlalchemy import and_
from app.models import Tasks, Projects, Goals, Strategies
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
from threading import Thread
import ldap
from flask import render_template, flash, redirect,Flask,Response,request,url_for, g,session,jsonify

@app.route('/restartajaxtest')
def restartajaxtest():
    computer = request.args.get('a')
    import pdb;pdb.set_trace()
    def runJob(computer):
        try:
            print computer
            # subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\restart\%s" % computer)
        except Exception,e:
            print 'there was an exception', e
    thr = Thread(target = runJob, args = [computer])
    thr.start()
    return jsonify(result=computer)

@app.route('/restartajax/<computer>')
def restartajax(computer):
    def sendEmail(you,html,text,subject):
        print you
        me = 'chet@acbhcs.org'
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ", ".join(you)
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo
        with open('//covenas/decisionsupport/meinzer/production/ps/secret/pw.txt','r') as pw:
            fillPW=pw.readline()
        s.login('alamedaDST@gmail.com', '%s' % fillPW) 
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, you, msg.as_string())
        s.quit()
    # def runJob(computer):
    #     try:
    #         subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\restart\%s" % computer)
    #     except Exception,e:
    #         print 'there was an exception', e
    # thr = Thread(target = runJob, args = [computer])
    # thr.start()
    def runJob(computer):
            err='error code 1'                 
            count=0
            while count < 3:
                out='Error'
                err='error'
                worked='Fail!  Please try again..................'
                try:
                    # log = open("//bhcsdbv02/emanio/bhcsdbv02psexec.log", 'w+') 
                    p=subprocess.Popen(r"""\\covenas\decisionsupport\meinzer\production\bat\restart\%s""" % computer,  stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
                    out, err = p.communicate()
                    if 'error code 0' not in err:
                        count+=1  
                    if 'error code 0' in err:
                        count=3                                          
                        out.replace('Offwall','')
                        err.replace('Offwall','')
                        if "error code 0." in err:
                            worked= "Yes, it worked...................."
                            sendEmail(['cmeinzer@acbhcs.org'],'restarting %s' % computer,'restarting %s' % computer,'restarting %s' % computer)
                except Exception,e:
                    print 'there was an exception', e
                return out,err,worked

    o,e,w=runJob(computer)
    print 'this is o ',o,'this is e ', e
    def runOpen(computer):
        try:
            subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\open\%s" % computer)
        except Exception,e:
            print 'there was an exception', e
    thr = Thread(target = runOpen, args = [computer])
    if w=="Yes, it worked....................":
        thr.start()
        shift=".......................try server at "+str((datetime.datetime.now()+datetime.timedelta(minutes=8)).strftime('%I:%M %p'))
    else:
        shift=''
    return jsonify(result=w +" results of "+computer+str(e)+shift )

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    # form=restart_form()
    restartFiles=os.listdir('//covenas/decisionsupport/meinzer/production/bat/restart/')
    return render_template("restart.html",restartFiles=restartFiles)



# login_manager = LoginManager()
# login_manager.init_app(app) 

# login_manager.session_protection = None
#login_managerlogin_view = 'login'

# class User(UserMixin):
#   def __init__(self, name, id, active=True):
#     self.name = name
#     self.id = id
#     self.active = active 

#   def is_authenticated(self):
#       return True

#   def is_active(self):
#     return self.active   

# USERS = {
# 1: User(u"Notch", 1),
# u'92bce19df203964b9dbbe7911f074e86': User(u"Chet", u'92bce19df203964b9dbbe7911f074e86'),
# 4: User(u"Stevex", 4),
# 3: User(u"Creeper", 3, False),
# u'seven': User(u'Bob',u'seven')
# } 
            # p=models.Projects(name=pform.project.data,projectleader=pform.projectleader.data)
            # db.session.add(p)
            # db.session.commit()

# @login_manager.user_loader
# def load_user(id):
#   # import pdb;pdb.set_trace()
#   x=models.User.query.filter_by(id=(id)).first() 
#   return x
# @login_manager.unauthorized_handler
# def unauthorized():
#     print 'unauthorized'
#     flash("You must be logged in.")
#     return redirect(url_for("login"))

# @login_manager.user_loader
# def user_loader(user_id):
#     """Given *user_id*, return the associated User object.

#     :param unicode user_id: user_id (email) user to retrieve
#     """
#     g.user=current_user
#     return models.User.query.get(user_id)



# @app.route("/logout")
# # @login_required
# def logout():
#     logout_user()
#     session.pop('logged_in', None)
#     flash("Logged Out.")
#     # import pdb;pdb.set_trace()
#     return redirect(url_for("login"))


# @app.route("/pickaform",methods=["GET","POST"])
# @login_required
# def pickaform():
#     form = Which()
#     if form.validate_on_submit():
#         # import pdb;pdb.set_trace()
#         print form.formtype.data
#         if form.formtype.data==u"Short":
#             WHICH=1
#         else:
#             WHICH=2
#         return redirect(url_for("requestform",WHICH=WHICH))
#     return render_template("start.html",email=g.user.email,name=g.user.name,form=form,)


# # @app.route("/requests",methods=["GET","POST"])
# # @login_required
# # def requests():
# #     requestlist=models.Request.query.all()
# #     return render_template("requests.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

# @app.route("/allrequest",methods=["GET","POST"])
# @login_required
# def allrequest():
#     requestlist= models.Request.query.all() 
#     # import pdb;pdb.set_trace()
#     return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)


# @app.route("/myrequest",methods=["GET","POST"])
# @login_required
# def myrequest():
#     requestlist= models.Request.query.filter_by(email=g.user.email).all() 
#     # import pdb;pdb.set_trace()
#     return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

# @app.route('/viewrequest/<id>/', methods=['GET', 'POST'])
# @login_required
# def view_request(id):
#     request_to_edit=models.Request.query.filter_by(id=int(id)).first() 
#     form=Request(obj=request_to_edit)
#     # form.populate_obj(request_to_edit)
#     # import pdb;pdb.set_trace()
#     if request.method == 'POST':
#         # import pdb;pdb.set_trace()
#         request_to_edit.note=form.note.data
#         db.session.commit()
#         return redirect(url_for('allrequest'))
#     # if delete_form.validate_on_submit():
#     #     db.session.delete(ptask)
#     #     db.session.commit()
#     #     return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
#     return render_template('view_request.html',request_to_edit=request_to_edit ,name=g.user.name,form=form)



# @app.route('/edit_request/<id>/', methods=['GET', 'POST'])
# @login_required
# def edit_request(id):
#     request_to_edit=models.Request.query.filter_by(id=int(id)).first() 
#     form=Request(obj=request_to_edit)
#     # form.populate_obj(request_to_edit)
#     # import pdb;pdb.set_trace()
#     if request.method == 'POST':
#         # import pdb;pdb.set_trace()
#         request_to_edit.note=form.note.data
#         db.session.commit()
#         return redirect(url_for('myrequest'))
#     # if delete_form.validate_on_submit():
#     #     db.session.delete(ptask)
#     #     db.session.commit()
#     #     return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
#     return render_template('edit_request.html',request_to_edit=request_to_edit ,name=g.user.name,form=form)



# @app.route("/followup",methods=["GET","POST"])
# @login_required
# def followup():
#     # import pdb;pdb.set_trace()
#     requestlist= models.Request.query.filter_by(email=g.user.email).all() 
#     return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

    
# @app.route("/requestform/<WHICH>",methods=["GET","POST"])
# @login_required
# def requestform(WHICH):
#     form = Request()
#     # import pdb;pdb.set_trace()
#     if form.validate_on_submit():
#       print 'submit'
#       # import pdb;pdb.set_trace()
#       p=models.Request(email=g.user.email,username=g.user.name,jobTitle=form.jobTitle.data,deadlinedate=form.deadlinedate.data,emanio=form.emanio.data,MHorSUD=form.MHorSUD.data,
#         keyQuestions=form.keyQuestions.data, problem=form.problem.data,specialFacts=form.specialFacts.data,requestedBy=form.requestedBy.data, priority=form.priority.data,
#         timeframe=form.timeframe.data,timeBreakdown=form.timeBreakdown.data,specialPop=form.specialPop.data,agency=form.agency.data,ru=form.ru.data,
#          specialInstructions=form.specialInstructions.data, typeOfService=form.typeOfService.data, timeframestart=form.timeframestart.data, timeframeend=form.timeframeend.data, 
#          longDescription=form.longDescription.data, requestDate=datetime.datetime.utcnow(),
#          audience=form.audience.data,  columnsRequired=form.columnsRequired.data, deadlinetime=form.deadlinetime.data, deadlineWhy=form.deadlineWhy.data)
#       db.session.add(p)
#       db.session.commit()
#       return redirect(url_for('followup'))
#     else:
#         flash('validation fail')
#     if WHICH=='1':
#         print 'short!!'
#         return render_template("short.html",email=g.user.email,name=g.user.name,form=form)
#     else:
#         return render_template("long.html",email=g.user.email,name=g.user.name,form=form)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         try:
#             l = ldap.initialize("ldap://10.129.18.101")
#             l.simple_bind_s("program\%s" % form.username.data,form.password.data)
#             print "Authentification Successful"
#             r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % form.username.data,['mail','objectGUID','displayName'])
#             email=r[0][1]['mail'][0]   
#             # print email
#             GUID=r[0][1]['objectGUID'][0]   
#             FullName=r[0][1]['displayName'][0] 
#             import uuid
#             guid = uuid.UUID(bytes=GUID)
#             # print form.remember_me.data
#             # g.user = current_user
#             if not models.User.query.filter_by(email=unicode(email)).first(): 
#               p=models.User(name=FullName,email=email)
#               db.session.add(p)
#               db.session.commit()            
#             login_user(user_loader(unicode(email)),remember=form.remember_me.data)
#             flash("Logged in successfully.")
#             g.email=email
#             session['logged_in'] = True
#             # import pdb;pdb.set_trace()
#             return redirect( url_for("pickaform"))
#         except Exception as e:
#             flash("Invalid Credentials.")
#             return render_template("login.html", form=form)
#     return render_template("login.html", form=form)
# USERS.get('\x92\xbc\xe1\x9d\xf2\x03\x96K\x9d\xbb\xe7\x91\x1f\x07N\x86')
# @app.route('/')
# def index():
#     user = {'nickname': 'Chet'}  # fake user
#     return render_template('index.html',
#                            title='Home',
#                            user=user)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html', 
#                            title='Sign In',
#                            form=form)

# from flask import request

@app.route('/navstart', methods=['GET','POST'])
def navstart():
    aform=ldapA()
    email=None
    AS=None
    if aform.validate_on_submit():
        import sys
        import ldap
        l = ldap.initialize("ldap://10.129.18.101")
        email=None
        try:
            l.simple_bind_s("program\%s" % aform.username.data,aform.password.data)
            print "Authentification Successful"
            r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % aform.username.data,['mail'])
            email=r[0][1]['mail']
            AS=1
            print email
        except:
            print 'Failed'
            AS=0
        print email
        # return render_template("navStart.html",aform=aform,email=email,AS=AS)
    return render_template("navStart.html",aform=aform,email=email,AS=AS)


@app.route('/sendemail', methods=['GET', 'POST'])
def sendEmailV4():
    # subject = ''
    recipient=', '.join(['cmeinzer@acbhcs.org'])
    body='html text'
    subject = 'subjectline'
    headers = ["From: " + 'chet@acbhcs.org',
               "Subject: " + 'subject',
               "To: " + 'cmeinzer@acbhcs.org',
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    session = smtplib.SMTP("allsmtp.acgov.org",25)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.sendmail('chet@acbhcs.org', ['cmeinzer@acbhcs.org'], headers + "\r\n\r\n" + body)
    session.quit()
    return "it worked"

app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    pform=project_form()
    tform=task_form()
    sform=strategy_form()
    gform=goal_form()
    P=models.Projects.query.all()
    if gform.validate_on_submit():
        u=models.Projects.query.get(1)
        p=models.Goals(goal=gform.goal.data,proj=u)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("baseindex.html",pform=pform,gform=gform,tform=tform,sform=sform,P=P)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@app.route('/start', methods=['GET','POST'])
def start():
    # from flask import request
    pform=project_form()
    P=models.Projects.query.all()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id)) 
    # import pdb;pdb.set_trace() 
    if request.method == 'POST':
        if pform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(pform)
            return redirect(url_for('start'))
        else:
            p=models.Projects(name=pform.project.data,projectleader=pform.projectleader.data)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('start'))
    return render_template("index_for_project.html",pform=pform,P=P,zipit=zip(P,q_sum))

@app.route('/ProjectTree/<name>', methods=['GET','POST'])
def project_outline(name):
    # name=request.args.get('name')
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    G=project.goals.all()
    gform=goal_form(request.values)
    delete_form=DeleteRow_form()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    Goals.id.label("goal_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id).filter(Projects.id == name) )
    if request.method == 'POST' and  gform.submit.data:
        if gform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(gform)
            return redirect(url_for('project_outline', name=name))
        else:
            p=models.Goals(goal=gform.goal.data,proj=project)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('project_outline', name=name))
    if request.method == 'POST' and  delete_form.submitd.data:
        pstratrow = delete_form.row_id.data
        pstrat=models.Goals.query.filter_by(id=pstratrow).first()
        db.session.delete(pstrat)
        db.session.commit()
        return redirect(url_for('project_outline',name=name))            
    # if request.method == 'POST' and  delete_form.submit.data:
    #     delete_row=
    return render_template("index_for_goal.html",project=project,G=G,gform=gform,P=P,zipit=zip(G,q_sum),delete_form=delete_form)

@app.route('/ProjectTree/<name>/<goal>', methods=['GET','POST'])
def strategy_outline(name,goal):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    S=pgoal.strategies.all()
    sform=strategy_form(request.values)
    delete_form=DeleteRow_form()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    Strategies.id.label("strategy_id"),
    Goals.id.label("goal_id"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id,Strategies.id).filter(Goals.id == goal) )
    if request.method == 'POST' and sform.submit.data:
        print sform.validate()
        if sform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(sform)
            return redirect(url_for('strategy_outline',name=name,goal=goal))
        else:
            p=models.Strategies(strategy=sform.strategy.data,goa=pgoal)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('strategy_outline',name=name,goal=goal))
    if request.method == 'POST' and  delete_form.submitd.data:
        pstratrow = delete_form.row_id.data
        pstrat=models.Strategies.query.filter_by(id=pstratrow).first()
        db.session.delete(pstrat)
        db.session.commit()
        return redirect(url_for('strategy_outline',name=name,goal=goal))
    return render_template("index_for_strategy.html",project=project,S=S,sform=sform,pgoal=pgoal,P=P,zipit=zip(S,q_sum),delete_form=delete_form)

@app.route('/strategysort/<goal>')
def strategy_sort(goal):
    P=models.Projects.query.all()
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    S=pgoal.strategies.all()
    project=models.Projects.query.filter_by(id=pgoal.project_id).first()
    return render_template("sort_strategy.html",q_sum=S,project=project,goal=pgoal,P=P)

@app.route('/order/<table>')
def order(table):
    sortedItems = request.args.listvalues()[0]
    o=1
    table = getattr(models, table)
    for item in sortedItems:
        grab = table.query.filter_by(id=item).first() 
        grab.order=o
        o+=1
    db.session.commit()
    return jsonify(result="New Order Saved!")

@app.route('/tasksort/<strategy>')
def task_sort(strategy):
    P=models.Projects.query.all()
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    T=pstrat.tasks.all()
    goal=models.Goals.query.filter_by(id=pstrat.goal_id).first()
    project=models.Projects.query.filter_by(id=goal.project_id).first()
    return render_template("sort_task.html",q_sum=T,project=project,goal=goal,strategy=strategy,P=P)

@app.route('/ProjectTree/<name>/<goal>/<strategy>', methods=['GET','POST'])
def task_outline(name,goal,strategy):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    # T=(pstrat.tasks.order_by(pstrat.tasks.Order)).all()
    T=pstrat.tasks.all()
    tform=task_form(request.values)
    if request.method == 'POST':
        if tform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(tform)
            return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
        else:
            if tform.complete.data == True:
                completeDate=datetime.datetime.utcnow()
                print completeDate
                p=models.Tasks(task=tform.task.data,strat=pstrat,note = tform.note.data,staff=tform.staff.data,deadline=tform.deadline.data,complete=tform.complete.data,created=datetime.datetime.utcnow(), completeDate=completeDate)
            else:
                p=models.Tasks(task=tform.task.data,strat=pstrat,note = tform.note.data,staff=tform.staff.data,deadline=tform.deadline.data,complete=tform.complete.data,created=datetime.datetime.utcnow())
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template("index_for_task.html",project=project,T=T,tform=tform,pstrat=pstrat,pgoal=pgoal,P=P)

@app.route('/outlineindex')
def outline_index():
    P=models.Projects.query.all()
    return render_template("index_for_outline.html",P=P)

@app.route('/outline/<name>' )
def outline(name):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    return render_template("index_outline_all.html",P=P,project=project)

@app.route('/edit/<name>/<goal>/<strategy>/<task>', methods=['GET', 'POST'])
def edit_task(name,goal,strategy,task):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    ptask=models.Tasks.query.filter_by(id=task).first()
    delete_form=DeleteRow_form()
    form = task_form(obj=ptask)
    form.populate_obj(ptask)
    form.deadline.data = ptask.deadline.strftime("%m/%d/%Y")
    tform=task_form(request.values)
    if request.method == 'POST' and form.validate_on_submit():
        #if it changed from True to false, set complete date to None
        # import pdb;pdb.set_trace()
        if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[False]:
            print 'changed from false to true'
            ptask.completeDate=datetime.datetime.utcnow()
        if get_history(ptask, 'complete')[0]==[False] and get_history(ptask, 'complete')[2]==[True]:
            print 'changed from true to false'
            ptask.completeDate=None
        else:
            if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[None]:
                ptask.complete=True
                ptask.completeDate=None
        db.session.commit()
        return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    if delete_form.validate_on_submit():
        db.session.delete(ptask)
        db.session.commit()
        return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template('edit_task.html', tform=tform,form=form,project=project,pgoal=pgoal,pstrat=pstrat,ptask=ptask,delete_form=delete_form,P=P)


@app.route('/graphs')
def graphs():
    P=models.Projects.query.all()
    return render_template("index_for_graphs.html", P=P)

@app.route('/graphs/stats')
def graphs_stats():
    P=models.Projects.query.all()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id))   
    return render_template("graph_stats.html", P=P,q_sum=q_sum,zipit=zip(P,q_sum))



from app import db
