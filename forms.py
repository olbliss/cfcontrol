from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateTimeField, validators #, SelectMultipleField , PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired #, Email, EqualTo, ValidationError
from datetime import datetime, timedelta
from wtforms.fields.html5 import DateField, TimeField


status_options = [('ongoing', 'ongoing'), ('completed', 'completed')]
priority_options = [('moderate', 'moderate'),('high', 'high'),('low','low')]
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description',[validators.Required()],render_kw={"placeholder": "Recommendation: include a short description now, and expand once the inital post is created - via the 'Edit' option"})
    date_posted  = DateField('Date',format='%Y-%m-%d', default=datetime.now())#+ timedelta(hours=1))
    time_posted  = TimeField('Time',format='%H:%M',default=datetime.now())# + timedelta(hours=1))
    date_closed  = DateField('Date',format='%Y-%m-%d')
    time_closed  = TimeField('Time',format='%H:%M')
    status = SelectField('Status',choices = status_options)
    priority = SelectField('Priority',choices = priority_options)
    assigned_to = StringField('Assigned To')
    reported_by = StringField('Reported By')
    submit = SubmitField('Save')

class BuggyForm(FlaskForm):
    BName = StringField('Name of Buggy', validators=[DataRequired()])
    BRider = StringField('Name of Rider',render_kw={"placeholder": "Leave Blank if Buggy is Available"})
    lastmodified  = DateTimeField('Date and Time', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Save')

class SearchForm(FlaskForm):
    searchstring = StringField('Search value', validators=[DataRequired()])
    email = StringField('Email',render_kw={"placeholder": "Type email if want an email report, otherwise leave blank"})
    submit = SubmitField('Search')

# Tiny MCE
class TinyPostForm(FlaskForm):
    heading = StringField('Title', validators=[InputRequired(), Length(max=100)])
    post = TextAreaField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')