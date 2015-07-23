from app import app
from flask import Flask, render_template, request, flash,redirect,url_for,jsonify
from forms import goal_form, strategy_form, project_form, task_form,upload_form,push_form
import models 
import datetime
from sqlalchemy.orm.attributes import get_history
from werkzeug import secure_filename
import re, shutil, os, sys
from sqlalchemy.sql import func
from sqlalchemy import case
from sqlalchemy import and_
from app.models import Tasks, Projects, Goals, Strategies
from app import db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
from threading import Thread




@app.route('/_order')
def order():
    sortedItems = request.args.get('result')
    print sortedItems
    return jsonify(result=sortedItems)

@app.route('/test')
def test():
    P=models.Goals.query.all()
    return render_template("test.html",q_sum=P)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/testjs')
def testjs():
    return render_template('testjs.html')


@app.route('/argonautwho/<DB>', methods=['GET', 'POST'])
def argonautwho(DB):
    form=push_form(pushfile=DB)
    if form.validate_on_submit():
        def startEmail(DB, whox,whatFile):  
            list=[]
            list.append('cmeinzer@acbhcs.org')
            if 'LO' in whox.upper():
             list.append('LHall2@acbhcs.org')
            if 'GAB' in whox.upper():
             list.append('GOrozco@acbhcs.org')
            if 'GAR' in whox.upper():
             list.append('GSpicer@acbhcs.org')
            if 'KE' in whox.upper():
             list.append('KCoelho@acbhcs.org')
            if 'KI' in whox.upper():
             list.append('KRassette@acbhcs.org')
            if 'JO' in whox.upper():
             list.append('JEngstrom@acbhcs.org')
            if 'JA' in whox.upper():
             list.append('jbiblin@acbhcs.org')
            for item in list:
             print item
            who= list    
            if socket.gethostname() =='WinSPSSV4':
                sender='chet@acbhcs.org'
                recipient=', '.join(who)
                text=''
                html = """\
                <html>
                  <head>Processing your request!<br></head>
                    </html> <br> %s
                """ % whatFile
                body=html
                subject = 'Processing your request to run %s! ' % DB
                headers = ["From: " + sender,
                           "Subject: " + subject,
                           "To: " + recipient,
                           "MIME-Version: 1.0",
                           "Content-Type: text/html"]
                headers = "\r\n".join(headers)
                session = smtplib.SMTP("allsmtp.acgov.org",25)
                session.ehlo()
                session.starttls()
                session.ehlo
                session.sendmail(sender, who, headers + "\r\n\r\n" + body)
                session.quit()
            else:  
                subjectline='Processing your request to run %s! ' % DB
                SendEmailFrom='chet@acbhcs.org'
                SendEmailTo=who
                text=''
                html = """\
                <html>
                  <head>Running your request!</head>
                          <br><br> %s
                
                </html> 
                """ % whatFile 
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subjectline
                msg['From'] = SendEmailFrom
                msg['To'] = ", ".join(SendEmailTo)
                # Record the MIME types of both parts - text/plain and text/html.
                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')
                # Attach parts into message container.
                # According to RFC 2046, the last part of a multipart message, in this case
                # the HTML message, is best and preferred.
                msg.attach(part1)
                msg.attach(part2)
                # SMTP_SERVER = 'smtp.gmail.com'
                # SMTP_PORT = 587
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
                s.sendmail(SendEmailFrom, SendEmailTo, msg.as_string())
                s.quit()
        DevProdBoth= "".join(form.where.data)
        insertList=[]
        DB = os.path.splitext(DB)[0]
        print DB     
        if 'F' in DevProdBoth.upper() or DevProdBoth.upper()=='':
            insertList.append('//covenas/decisionsupport/meinzer/Production/dashboarddatasets/%s.sps' % DB)
        if 'D' in DevProdBoth.upper():
            insertList.append("//covenas/decisionsupport/meinzer/Production/push/%spush.sps" % DB)
        if 'P' in DevProdBoth.upper():
            insertList.append("//covenas/decisionsupport/meinzer/Production/pushproduction/%spushP.sps" % DB)
        # who=raw_input('\n\n\n\n\n\n\n\n\n\n\n----------who should be emailed?\n')
        who=form.who.data
        where='server'   
        if 'L' in where.upper():
            Serverx=0
            print '*******Local job selected'
        elif "S" in where.upper():
            Serverx=1
        else:
            Serverx=0
            print 'Defaulting to local'
        liststring=insertList[0:]
        AddInsert="""begin program.
when='fly'  
Files=%s
end program.
insert file='//covenas/decisionsupport/meinzer/production/ps/errorTestPickles.sps'.""" % (liststring)
        p=re.compile('\n',re.M)
        splitsyntax=p.split(AddInsert)
        if Serverx==1:
            batstring=r""""C:\Program Files\IBM\SPSS\Statistics\22\stats.exe"  "\\covenas\decisionsupport\Meinzer\production\spj\%s.spj" -production -server inet:bhcsstat1:3022 -user program\meinzerc -password %%mypassword%%""" % DB
        else:
            batstring=r""""C:\Program Files\IBM\SPSS\Statistics\%s\stats.exe" -production "\\covenas\decisionsupport\Meinzer\Production\SPJ\%s.spj" """ % ('22',DB)
        spjstring=r"""<?xml version="1.0" encoding="UTF-8"?><job print="false" syntaxErrorHandling="continue" syntaxFormat="interactive" unicode="false" xmlns="http://www.ibm.com/software/analytics/spss/xml/production" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ibm.com/software/analytics/spss/xml/production http://www.ibm.com/software/analytics/spss/xml/production/production-1.3.xsd"><output outputFormat="viewer" outputPath="\\covenas\decisionsupport\Meinzer\Production\Output\production made\%s.spv"/><syntax syntaxPath="\\covenas\decisionsupport\temp\%s.sps"/></job>""" % (DB,DB)
        SPJloc="//covenas/decisionsupport/Meinzer/Production/SPJ/%s.spj" % DB
        BATloc="//covenas/decisionsupport/Meinzer/Production/bat/temp/%s.bat" % DB
        with open(SPJloc,'w') as spj:
            spj.write(spjstring)
        with open(BATloc,'w') as bat:
            bat.write(batstring)   
        with open('//covenas/decisionsupport/temp/%s.sps' % DB,'w+') as gen:
            for item in splitsyntax:
                item=item.replace(', ',',\n')
                gen.write(item+'\n')
        def runJob(DB,who,liststring):
            try:
                startEmail(DB, who,liststring)
                subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\temp\%s.bat" % DB)
                stars='*'*10
                for i in stars:
                    print i
                print '\nPushing your file!!!!\n'
                print DB
                with open('//covenas/decisionsupport/temp/errorresult.txt','r') as ER:
                    error=ER.readline()
            except Exception,e:
                print 'there was an exception'
                error='\nThere was an error in your file\n'+str(e)
            print error
            subprocess.call(r'c:\python%s\python \\covenas\decisionsupport\meinzer\production\ps\finishAlert2.py "%s" %s ' % (str(sys.version_info[0])+str(sys.version_info[1]),error,who))
        thr = Thread(target = runJob, args = [DB,who,liststring])
        thr.start()
        # try:
        #     startEmail(DB, who,liststring)
        #     subprocess.call(r"\\covenas\decisionsupport\meinzer\production\bat\temp\%s.bat" % DB)
        #     stars='*'*10
        #     for i in stars:
        #         print i
        #     print '\nPushing your file!!!!\n'
        #     print DB
        #     with open('//covenas/decisionsupport/temp/errorresult.txt','r') as ER:
        #         error=ER.readline()
        # except Exception,e:
        #     print 'there was an exception'
        #     error='\nThere was an error in your file\n'+str(e)
        # print error
        # subprocess.call(r'c:\python%s\python \\covenas\decisionsupport\meinzer\production\ps\finishAlert2.py "%s" %s ' % (str(sys.version_info[0])+str(sys.version_info[1]),error,who))
        stageFiles=os.listdir('//covenas/decisionsupport/DashboardDataSets/staging/')
        prodFiles=os.listdir('//covenas/decisionsupport/meinzer/production/DashboardDataSets/')
        return render_template("argonaut.html",stageFiles=stageFiles,prodFiles=prodFiles)
    return render_template("argonautwho.html",form=form,file=DB)

@app.route('/stageupdate/<file>', methods=['GET', 'POST'])
def stageupdate(file):
    stageFolder = '//covenas/decisionsupport/DashboardDataSets/staging/'
    dashProdFolder ='//covenas/decisionsupport/meinzer/production/DashboardDataSets/'
    dashDevFolder = '//covenas/decisionsupport/DashboardDataSets/'
    prodFolder = dashProdFolder
    devFolder = dashDevFolder
    stagefile='//covenas/decisionsupport/DashboardDataSets/staging/'+file
    def makeRemoteSyntax(spssTable,SQLtable):
        Syntax=r"""get file =  '%s.sav'.
compute DBcreateDate=$time.
formats dbcreatedate (datetime23).
SAVE TRANSLATE OUTFILE='//bhcsdbv03/emanio/%s.csv'
  /TYPE=CSV
  /ENCODING='Locale'  /MAP   /REPLACE  /FIELDNAMES  /CELLS=VALUES.
n of cases 1.

SAVE TRANSLATE /TYPE=ODBC
/Connect ='DSN=DashboardDatadev;UID=;APP=SPSS For'+
' Windows;WSID=HPMXL9360ZDD;DATABASE=DashboardDatadev;Trusted_Connection=Yes'
/table= '%s' /MAP/REPLACE.


         """ % (spssTable,SQLtable,SQLtable)
        return Syntax
    def makeSQLPushbase(SQLtable):
        SQLPushbase=r"""
import re
import pypyodbc as pyodbc
from datetime import datetime
import csv
import logging
import time

logging.basicConfig(filename='//bhcsdbv03/emanio/bhcsdbv03.log',level=logging.DEBUG)
logging.debug('Start push %s at '+ str(datetime.now()))
benchmarkstart=datetime.now()

for i in range(120):
    with open('//bhcsdbv03/emanio/busy.txt','r+') as busy:
        isit=busy.readline()
        if isit =='':
            break
        else:
            time.sleep(60)
            logging.debug('sleeping 1 min')
            if i == 119:
                break

with open('//bhcsdbv03/emanio/busy.txt','w') as busy:
    busy.write('busy')

def sendTOSQL(csvLocation,sqlTableName):
    x=-1
    with open (csvLocation, 'r') as f:
                cnxn = pyodbc.connect('DSN=dashboarddatadev')
                cursor = cnxn.cursor()            
                reader = csv.reader(f)
                list=[]
                cursor = cnxn.cursor()
                cursor.execute('select * from %%s' %% sqlTableName)
                for i in cursor.description:
                    if i[1].__name__=='datetime':
                        list.append(1)
                    else: 
                        list.append(0)
                cnxn2 = pyodbc.connect('DSN=dashboarddatadev')
                cursor = cnxn2.cursor()            
                reader = csv.reader(f)
                columns = next(reader) 
                print columns
                for data in reader:
                    #this line takes out first row since 
                    if x != -1:
                        changeNulls=zip(data,list)
                        y=0
                        for item in changeNulls:
                            if item[1]==1 and item[0]==' ':
                                data[y]=None
                            y=y+1
                        query = 'insert into {0}({1}) values ({2})'
                        query = query.format(sqlTableName,','.join(columns), ','.join('?' * len(columns)))
                        itemchange=re.compile(re.escape('case,'),re.IGNORECASE)
                        query=itemchange.sub('"case",',query)
                        itemchange=re.compile(re.escape('full,'),re.IGNORECASE)
                        query=itemchange.sub('"full",',query)
                        cursor.execute(query, data)
                        if x %% 1000000==0:
                            if len(str(x)) > 7:
                                xstar=str(x)[0:2]
                            else:
                                xstar=str(x)[0]
                            if xstar=='0':
                                logging.debug(r'processing and counting rows to a million' )
                            else:
                                logging.debug(r'%%s,000,000 rows processed and counting' %% (xstar))
                    x=x+1
                cursor.commit() 


"""     % (SQLtable)             
        return SQLPushbase    
    try:
        with open(stagefile, "r") as f: 
            c=f.readlines() 
        with open(stagefile, 'w') as ts:
            for item in c:
                print item
                itemchange=re.compile(re.escape('k:/'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/decisionsupport/',item)
                itemchange=re.compile(re.escape('k:\\'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/decisionsupport/',itemswitch)
                itemchange=re.compile(re.escape('i:/'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/spssdata/',itemswitch)
                itemchange=re.compile(re.escape('i:\\'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/spssdata/',itemswitch)
                itemchange=re.compile(re.escape('k:'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/decisionsupport/',itemswitch)
                itemchange=re.compile(re.escape('i:'),re.IGNORECASE)
                itemswitch=itemchange.sub('//covenas/spssdata/',itemswitch)
                #print itemswitch
                ts.write(itemswitch) 
    except Exception,e:
        print e
    afilenodev=re.sub('_dev','',file, flags=re.I)
    print 'moving ', afilenodev
    src=stagefile
    dst=prodFolder+'%s' % (afilenodev)
    shutil.move(src,dst)
    src=prodFolder+'%s' % (afilenodev)
    afileWdev=re.sub('\.',r'_Dev.',afilenodev)
    dst=devFolder+'%s' % (afileWdev)
    shutil.copyfile(src,dst)
    primaryFolder='//covenas/decisionsupport/meinzer/production/DashboardDatasets/'
    stageFiles=os.listdir('//covenas/decisionsupport/DashboardDataSets/staging/')
    prodFiles=os.listdir(primaryFolder)
    DB=os.path.splitext(afilenodev)[0]
    list=[]
    list2=[]
    listpypush=[]
    fileDB=primaryFolder+"%s.sps" % DB
    fileDev="//covenas/decisionsupport/meinzer/production/push/%spush.sps" % DB
    fileProduction="//covenas/decisionsupport/meinzer/%s.sps" % DB
    print fileDB
    # import pdb;pdb.set_trace()
    with open(fileDB, "rb") as f: 
            code=f.read()
            if 'PUSHBREAK' in code.upper():
                results=re.split('pushbreak\\.',code,flags=re.M)
                for i in results:
                    if 'SKIPROW' in i.upper() or 'REMOTEPUSH'in i.upper() or 'REMOTE PUSH'in i.upper():
                        skipRow=1
                    elif 'ASIS' in i.upper():
                        skipRow=2
                    else:
                        skipRow=0
                    if skipRow==2:
                                m=re.search('(?<=asis\.).*',i,flags=re.DOTALL)
                                Syntax=m.group(0)
                                xx=m.group(0)
                                xx=xx.replace('*','')
                                listeCommands=xx.split('\r\n')
                                for item in listeCommands:
                                    item=item.replace('\n','')
                                Syntax='\n'.join(listeCommands)
                                print Syntax
                                print i
                                list.append(Syntax)
                                list.append('\n\n')
                    if 'SQLTABLE' in i.upper():
                        if 'OLD PUSH' in i.upper() or 'DO NOT PUSH' in i.upper():
                            print 'the file ', fileDB, '\ndid not convert\n',  i.replace('\r\n',' ')
                        else:  
                            m = re.search('(?<=SQLTABLE)\s*\=\s*\S+',i,flags=re.I)
                            print  m.group(0)         
                            SQLtable=m.group(0).replace('=','').replace(',','').replace("'","") 
                            SQLtable=SQLtable.strip( ).strip('.') 
                            SQLtable=os.path.splitext(SQLtable)[0] 
                            SQLtable=SQLtable.strip( )                                                       
                            m = re.search('(?<=SPSSTABLE)\s*\=\s*\S+[\s\S]*',i,flags=re.I)
                            spssTable=m.group(0).replace('=','').replace(',','').replace('"','').replace("'","")
                            insensitive=re.compile(re.escape('.sav'),re.I)
                            spssTable=insensitive.sub('',spssTable)
                            spssTable=spssTable.rstrip('.')
                            spssTable=spssTable.strip("'")
                            spssTable=spssTable.strip('"')
                            spssTable=spssTable.strip( )
                            spssTable=os.path.splitext(spssTable)[0]
                            spssTable=spssTable.strip( )                            
                            Syntax=r"""get file =  '%s.sav'.
                            compute DBcreateDate=$time.
                            formats dbcreatedate (datetime23).
                            SAVE TRANSLATE /TYPE=ODBC
                            /Connect ='DSN=DashboardDatadev;UID=;APP=SPSS For'+
                            ' Windows;WSID=HPMXL9360ZDD;DATABASE=DashboardDatadev;Trusted_Connection=Yes'
                            /table= '%s' /MAP/REPLACE.

                            """ % (spssTable,SQLtable)
                            if skipRow==1:
                                hostcmd=r"""host command=['c:\python27\python "//bhcsdbv03/emanio/Aremote%s.py"'].""" % DB
                                Syntax=makeRemoteSyntax(spssTable,SQLtable)
                                SQLPushbase=makeSQLPushbase(SQLtable)
                                line0=r"""benchmarkend=datetime.now()"""
                                line1=r"""FinishText = benchmarkend.strftime("%m-%d-%y %H:%M")"""
                                line2=r"""StartText = benchmarkstart.strftime("%m-%d-%y %H:%M")"""
                                line3=r"Runtimex = str(benchmarkend-benchmarkstart)[0:7]"
                                line5=r'with open("//bhcsdbv03/emanio/Error Log.txt", "r+") as myfile:'
                                line6=r"    old=myfile.read()"
                                line7=r"    myfile.seek(0)"
                                line8=r'    myfile.write("""%s ' % DB+"bhcsdbv03"
                                line9=r"    Start             Finish           Runtime Hrs:Min:Sec"
                                line10=r'    %s    %s   %s """  % (StartText,FinishText,Runtimex)+"\n\n"+ old)'
                                line11=r"with open('//bhcsdbv03/emanio/busy.txt','w') as busy:"
                                line12=r"   busy.write('')"
                                SQLPush=r"""
try:
sendTOSQL('//bhcsdbv03/emanio/%s.csv','%s')                                 
except:
logging.exception('Got exception on main handler %s')
raise

logging.debug('Finished push %s at '+ str(datetime.now()))
    """  % (SQLtable,SQLtable,SQLtable,SQLtable)       
                                listpypush.append(SQLPush)
                                listpypush.append('\n')
                            else:
                                print 'do not skip row!'
                            print Syntax
                            list.append(Syntax)
                            list.append('\n')
                #import pdb; pdb.set_trace();
                try:
                  if listpypush:
                    with open(r"//bhcsdbv03/emanio/Aremote%s.py" % DB, 'w+') as callpy:
                        callpy.write(r"""import subprocess
from datetime import datetime
import logging
logging.basicConfig(filename='//bhcsdbv03/emanio/bhcsdbv03.log',level=logging.DEBUG)
logging.debug('Start chain %s at '+ str(datetime.now()))   
try:       
log = open("//bhcsdbv03/emanio/bhcsdbv03psexec.log", 'w+')                  
c=subprocess.Popen(r"//bhcsdbv03/emanio/Bremote%s.bat", stdout=log, stderr=log, shell=True)
#stdout, stderr = p.communicate()
#print stderr
print 'it worked'
except:
logging.exception('Got exception on main handler chain %s')
raise

print 'it worked'""" % (DB, DB, DB))       
                    with open(r"//bhcsdbv02/emanio/Aremote%s.py" % DB, 'w+') as callpy:
                        callpy.write(r"""import subprocess
from datetime import datetime
import logging
logging.basicConfig(filename='//bhcsdbv02/emanio/bhcsdbv02.log',level=logging.DEBUG)
logging.debug('Start chain %s at '+ str(datetime.now()))   
try:                         
log = open("//bhcsdbv02/emanio/bhcsdbv02psexec.log", 'w+')               
c=subprocess.Popen(r"//bhcsdbv02/emanio/Bremote%s.bat", stdout=log, stderr=log, shell=True)
#stdout, stderr = p.communicate()
#print stderr
print 'it worked'
except:
logging.exception('Got exception on main handler chain %s')
raise

print 'it worked'""" % (DB, DB, DB))               
                    with open(r"//bhcsdbv03/emanio/Bremote%s.bat" % DB, 'w+') as hostfile:
                        hostfile.write(r"""psexec \\bhcsdbv03 -c -f -i \\bhcsdbv03\emanio\CopenPyFile%s.bat -u meinzerc -p %%mypassword%%""" % DB)
                    with open(r"//bhcsdbv02/emanio/Bremote%s.bat" % DB, 'w+') as hostfile:
                        hostfile.write(r"""psexec \\bhcsdbv02 -c -f -i \\bhcsdbv02\emanio\CopenPyFile%s.bat -u meinzerc -p %%mypassword%%""" % DB)                        
                    # with open(r"//bhcsdbv02/emanio/Aremote%s.bat" % DB, 'w+') as hostfile:
                    #     hostfile.write(r"""psexec \\bhcsdbv02 -c -f \\bhcsdbv02\emanio\CopenPyFile%s.bat""" % DB)                        
                    with open(r"\\bhcsdbv03\emanio\CopenPyFile%s.bat" % DB, 'w+') as batToPy:
                        batToPy.write(r"""c:\python27\python \\bhcsdbv03\emanio\DsendToSQL%s.py""" % DB)   
                    with open(r"\\bhcsdbv02\emanio\CopenPyFile%s.bat" % DB, 'w+') as batToPy:
                        batToPy.write(r"""c:\python27\python \\bhcsdbv02\emanio\DsendToSQL%s.py""" % DB)                            
                    with open(r"//bhcsdbv03/emanio/DsendToSQL%s.py" % DB,'w+') as test:
                        test.write(SQLPushbase)
                        for item in listpypush:
                            test.write(item)   
                        test.write(line0+'\n')
                        test.write(line1+'\n')
                        test.write(line2+'\n')
                        test.write(line3+'\n')
                        test.write(line5+'\n')
                        test.write(line6+'\n')
                        test.write(line7+'\n')
                        test.write(line8+'\n')
                        test.write(line9+'\n')
                        test.write(line10+'\n\n')
                        test.write(line11+'\n')
                        test.write(line12)
                        #need end benchmark 
                    with open(r"//bhcsdbv03/emanio/DsendToSQL%s.py" % DB,'r') as devcopy:    
                        code=devcopy.readlines()
                        with open(r"//bhcsdbv02/emanio/DsendToSQL%s.py" % DB,'w') as productioncopy:
                            for line in code:
                                itemchange=re.compile(re.escape('dashboarddatadev'),re.IGNORECASE)
                                line=itemchange.sub('DashboardData',line)
                                itemchange=re.compile(re.escape('bhcsdbv03'),re.IGNORECASE)
                                line=itemchange.sub('bhcsdbv02',line) 
                                productioncopy.write(line)  
                except:
                    print 'no listpy'   
                #import pdb;pdb.set_trace();                             
                with open(fileProduction,'w') as test:
                    for item in list:
                        test.write(item)
                    try:
                        test.write(hostcmd)
                    except:
                        print 'no host cmd'
                with open(fileProduction,'r') as makelist:
                    for itemx in makelist:
                        itemx=itemx.lstrip('*')
                        if 'REPLACE.' in itemx.upper():
                            list2.append(itemx+'\n')
                        else:
                            list2.append(itemx)
                with open(fileDev,'w') as makesyntax:
                    for item2 in list2:
                          item3=item2.lstrip()
                          item3=item3.replace('\r\n','\n')
                          item3=item3.lstrip('*')
                          item3=item3.lstrip(' ')
                          makesyntax.write(item3)
            else:
                print 'no push found in', fileDB
                print 'these files were updated in push'
    DBname=DB+'push'
    DBname2=DBname+"P"
    fileDev="//covenas/decisionsupport/meinzer/production/push/%s.sps" % DBname
    fileProduction="//covenas/decisionsupport/meinzer/production/pushproduction/%s.sps" % DBname2
    print fileDev, fileProduction+'\n'
    try:
        with open(fileDev,"r") as checkforDashFile:
            DashCheck=checkforDashFile.read()
            if 'DASHBOARD' in DashCheck.upper():
                with open(fileDev, "r") as f: 
                    c=f.readlines()   
                with open(fileProduction, 'w') as ts:
                    for item in c:
                        itemchange=re.compile(re.escape('dashboarddatadev'),re.IGNORECASE)
                        itemswitch=itemchange.sub('DashboardData',item)
                        itemchange=re.compile(re.escape('bhcsdbv03'),re.IGNORECASE)
                        itemswitch=itemchange.sub('bhcsdbv02',itemswitch)                        
                        ts.write(itemswitch)
    except:
        print '\n   ********Hey    No push file, was that expect?'
    return redirect(url_for('argonaut',
                                stageFiles=stageFiles,prodFiles=prodFiles))


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
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/send_me_a_file')
def send_me_index():
    P=models.Projects.query.all()
    uform=upload_form()
    return render_template("upload_file.html",form=uform,P=P)


# Route that will process the file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    P=models.Projects.query.all()
    flash('Thank you for uploading %s. ' % filename)
    uform=upload_form()
    return render_template("upload_another_file.html",form=uform,P=P)


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
    pform=project_form()
    P=models.Projects.query.all()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id))  
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
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    Goals.id.label("goal_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id).filter(Projects.id == name) )
    if request.method == 'POST':
        if gform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(gform)
            return redirect(url_for('project_outline', name=name))
        else:
            p=models.Goals(goal=gform.goal.data,proj=project)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('project_outline', name=name))
    return render_template("index_for_goal.html",project=project,G=G,gform=gform,P=P,zipit=zip(G,q_sum))

@app.route('/ProjectTree/<name>/<goal>', methods=['GET','POST'])
def strategy_outline(name,goal):
    # name=request.args.get('name')
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    S=pgoal.strategies.all()
    sform=strategy_form(request.values)
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    Strategies.id.label("strategy_id"),
    Goals.id.label("goal_id"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id,Strategies.id).filter(Goals.id == goal) )
    if request.method == 'POST':
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
    return render_template("index_for_strategy.html",project=project,S=S,sform=sform,pgoal=pgoal,P=P,zipit=zip(S,q_sum))

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
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    ptask=models.Tasks.query.filter_by(id=task).first()
    form = task_form(obj=ptask)
    form.populate_obj(ptask)
    form.deadline.data = ptask.deadline.strftime("%m/%d/%Y")
    tform=task_form(request.values)
    if request.method == 'POST' and form.validate_on_submit():
        #if it changed from True to false, set complete date to None
        if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[False]:
            print 'changed from false to true'
            ptask.completeDate=datetime.datetime.utcnow()
        if get_history(ptask, 'complete')[0]==[False] and get_history(ptask, 'complete')[2]==[True]:
            print 'changed from true to false'
            ptask.completeDate=None
        # task=tform.task.data
        # strat=pstrat
        # note = tform.note.data
        # staff=tform.staff.data
        # deadline=tform.deadline.data
        # complete=tform.complete.data
        # created=datetime.datetime.utcnow()
        db.session.commit()
        return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template('edit_task.html', tform=tform,form=form,project=project,pgoal=pgoal,pstrat=pstrat,ptask=ptask)


@app.route('/graphs')
def graphs():
    P=models.Projects.query.all()
    return render_template("index_for_graphs.html", P=P)

@app.route('/graphs/stats')
def graphs_stats():
    P=models.Projects.query.all()
    # for p in P:  
    #     y=0     
    #     x=0
    #     total=0
    #     project=models.Projects.query.filter_by(name=p.name).first() 
    #     G=project.goals.all()
    #     for g in G:
    #         pgoal=models.Goals.query.filter_by(goal=g.goal).first() 
    #         S=pgoal.strategies.all()
    #         for s in S:
    #             pstrat=models.Strategies.query.filter_by(strategy=s.strategy).first() 
    #             T=pstrat.tasks.all()
    #             for t in T:
    #                 if t.completeDate != None and t.deadline != None:
    #                     deadlineDiff= (t.deadline - t.completeDate) > datetime.timedelta(days=0)
    #                     print deadlineDiff, ' this is the deadlineDiff variable for ',t.task
    #                     if deadlineDiff==True:
    #                         y+=1
    #                         print y,' this is task y....'
    #                 total+=1
    #                 if t.complete==True:
    #                     x+=1
    #     y=float(y*1.00)
    #     x=float(x*1.00)
    #     total=float(total*1.00)
    #     if x == 0 or total ==0:
    #         p.percent=0
    #         db.session.commit()
    #     else:
    #         p.percent=float(x/total*100.0)
    #         db.session.commit()   
    #     if y == 0 or x ==0:
    #         p.percentDeadline=0
    #         db.session.commit()
    #     else:
    #         p.percentDeadline=float(y/x*100.0)
    #         db.session.commit()  
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id))   
    return render_template("graph_stats.html", P=P,q_sum=q_sum,zipit=zip(P,q_sum))



from app import db
