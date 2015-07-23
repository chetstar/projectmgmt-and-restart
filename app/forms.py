from flask.ext.wtf import Form
from wtforms import validators
from wtforms import widgets
from wtforms import TextField, BooleanField, SubmitField, DateField,TextAreaField,SelectMultipleField,IntegerField,PasswordField,StringField,DateTimeField,FormField,RadioField,SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class Which(Form):
    formtype = RadioField('how ready are you', choices=[('Long','<h3>Standard data request form (Designed to guide you through your request)</h3><br>'),
        ('Short',"<h3>Data Partner's Advanced form (<strong>be prepared to list all of the columns in the data request</strong>)</h3><br>")],coerce=unicode)
    submit=SubmitField('Submit')

class LoginForm(Form):
    username = StringField('ACBHCS login', validators=[validators.DataRequired()])
    password = PasswordField('Password', [validators.Required()])
    remember_me = BooleanField('remember_me', default=False)
    submit=SubmitField('Submit')

# [validators.Required(),validators.Length(min=2, max=50)]
class Request(Form):
    # test= QuerySelectField(query_factory=Requests.with_entities(Requests.id)) 
    jobTitle= TextField('This will be the name we use to communicate about the request.',validators=[validators.Required(),validators.Length(min=2, max=50)])#,
    emanio = BooleanField('Yes, I have looked at Context.', default=False)
    MHorSUD= RadioField('Is this MHS or SUD Services related?', choices=[('MHS','MHS'),('SUD','SUD Services')],coerce=unicode)
    longDescription= TextAreaField('Describe what you want to investigate.',validators=[validators.Required(),validators.Length(min=2, max=120)])
    keyQuestions= TextAreaField('What are the questions you want answered?',validators=[validators.Required(),validators.Length(min=2, max=120)])
    problem= TextAreaField('If the data shows a problem, describe your intervention or what data you might you need for that intervention')
    audience= TextAreaField('With whom or in what forum do you plan to share this data?',)
    columnsRequired= TextAreaField('These are all the columns you will get in your report (chose <a href="//127.0.0.1:8080/long"> general form  </a>if you are unsure)<br> Be sure to include Agency/RUs needed, time frame, special population, etc.,' )
    agency= TextField('For what Agencies do you want this data?', ) 
    ru = TextField("Leave blank if you want all RU's for Agency specified above",  ) 
    deadlinetime = SelectField(u'What Hour?',coerce=int, choices=[(8,'8 am'), (9, '9 am'), (10, '10 am'),
        (11, '11 am'), (12, 'Noon'), (13, '1 pm'), (14, '2 pm'), (15, '3 pm'), (16, '4 pm'), (17, '5 pm')])
    deadlinedate= DateField( '',  format='%m/%d/%Y',)
    deadlineWhy = TextField('Why?')
    priority= RadioField('Priority', choices=[('1','1. Just Curious'),('2','2. Low Priority'),('3','3. Medium'),('4','4. Top Priority'),('5','5. Extremely Urgent')],coerce=unicode,validators=[validators.Required()])
    requestedBy= TextField("If this isn't your request, who is it for?") 
    # deliveryFormat= TextField('Format for Delivery', [validators.Required(),validators.Length(min=2, max=50)] ) 
    # start and end?
    timeframe= TextField('From what time frame do you want data? E.g., Most recent fiscal year? Most recent calendar year? Some other period?',  ) 
    timeframestart= DateField( '',  format='%m/%d/%Y',)
    timeframeend= DateField( '',  format='%m/%d/%Y',)
    timeBreakdown = TextField("If annual, specify Fiscal Year or Calendar.",  ) 
    specialPop= TextField('Are you interested in any demographics (age, ethnicity) or special populations (foster kids or disabled adults, and so on)?',  ) 
    typeOfService= TextField('Are there specific types of services you want? e.g. Crisis, Hospital, etc.', ) 
    specialInstructions= TextField('Any special instructions?',  ) 
    specialFacts= TextAreaField('Are there any facts or circumstances we should know to fulfill this request?') 
    note = TextAreaField('Note',)
    submit=SubmitField('Submit')

class Staff(Form):
    assinged= TextField('Staff Assigned?') 
    completeDate= DateTimeField( 'Date Completed',  format='%c')
    reviewed= TextField('Reviewed by?') 
    submit=SubmitField('Submit')


class project_form(Form):
    project = TextField('Project *', [validators.Required(),validators.Length(min=2, max=50)] ) 
    projectleader = TextField('Project Leader *(required)', [validators.Required(),validators.Length(min=4, max=35,message='not the right length')] ) 
    submit=SubmitField('Add Project')

class goal_form(Form):
    goal = TextAreaField('Goal', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    submit=SubmitField('Add Objective')

class strategy_form(Form):
    strategy = TextAreaField('Strategy', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    submit=SubmitField('Add Strategy')

class task_form(Form):
    task = TextAreaField('Task', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    staff = TextField('Staff Assigned')
    complete = BooleanField('Is the task Complete?')
    deadline =DateField( 'Deadline (mm/dd/yyyy)',  format='%m/%d/%Y',validators = [validators.Required()])
    note = TextAreaField('Note',)
    Order = IntegerField('Order')
    submit=SubmitField('Submit')

class DeleteRow_form(Form):
    row_id = IntegerField('')
    submitd = SubmitField('Delete')


class ldapA(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required()])
    submitd = SubmitField('Login')