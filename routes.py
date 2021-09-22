from flask import render_template, url_for, flash, redirect, request, send_from_directory
from flask_app import app, db
from flask_app.forms import PostForm, BuggyForm, SearchForm, TinyPostForm  #, BackupForm
from flask_app.models import Post, Buggies #, Backup
import pandas as pd
from sqlalchemy import create_engine
import smtplib
from email.message import EmailMessage
import datetime
import subprocess
import mysql.connector
import os

@app.route('/home')
@app.route('/h')
@app.route('/')
def home():
    # posts = Post.query.order_by(Post.priority.desc(),Post.date_posted.desc()).all()
    posts = Post.query.order_by(Post.priority.asc(),Post.date_posted.asc()).all()
    buggies = Buggies.query.all()
    return render_template('home.html', posts=posts, buggies=buggies)


@app.route('/all')
def all():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    buggies = Buggies.query.all()
    return render_template('all.html', posts=posts, buggies=buggies)




'''
Universal Search
'''
@app.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm()
	if request.method == "POST":
		search_term = form.searchstring.data
		email = form.email.data

		''' mysql.connector method:'''
		# mydb = mysql.connector.connect(host="olbliss.mysql.pythonanywhere-services.com",user="olbliss",passwd="creationfest")
		# mycursor = mydb.cursor()
		# mycursor.execute("USE olbliss$CF")
		# mycursor = mydb.cursor()

		# mycursor.execute('''SELECT *
          #                   FROM post
          #                   WHERE title like '%'''+search_term+'''%'
          #                   OR description like '%'''+search_term+'''%'
          #                   OR priority like '%'''+search_term+'''%'
          #                   OR date_posted like '%'''+search_term+'''%'
          #                   OR time_posted like '%'''+search_term+'''%'
          #                   OR date_closed like '%'''+search_term+'''%'
          #                   OR time_closed like '%'''+search_term+'''%'
          #                   OR status like '%'''+search_term+'''%'
          #                   OR assigned_to like '%'''+search_term+'''%'
          #                   OR reported_by like '%'''+search_term+'''%'
          #                   ;''')
		# post =  mycursor.fetchall()

		'''flask-sqlalchemy method:'''
		search_term = "%{}%".format(search_term)
		post2 = Post.query.filter(
			Post.title.like(search_term) |
			Post.description.like(search_term) |
			Post.priority.like(search_term) |
			Post.date_posted.like(search_term) |
			Post.time_posted.like(search_term) |
			Post.date_closed.like(search_term) |
			Post.time_closed.like(search_term) |
			Post.status.like(search_term) |
			Post.assigned_to.like(search_term) |
			Post.reported_by.like(search_term)).all()

		with open(os.getcwd()+'/cfcontrolapp/flask_app/search_report/search_output.html', 'w') as f:
			f.write('''
			<!DOCTYPE html>
			<html>
			  <head>
			    <meta charset="UTF-8">
			    <title>Search Result</title>
			    <!-- CSS Styling -->
			    <!--Link direct from CF:-->
			    <link rel="stylesheet" href="https://creationfest.org.uk/wp-content/themes/creation-fest/style.css" type="text/css" media="screen">
			    <link rel="stylesheet" href="{{ url_for('static', filename='additional.css') }}" type="text/css" media="screen">
			    <style>table,tr,td {
			         border:1px solid black;
			        } </style>
			  </head>
			  <body>''')
			f.write('<h1>Search Report</h1><hr>')
			f.write('<h2> Report: "'+search_term[1:-1]+'"</h2><hr>')
			f.write('<table>')
			for p in post2:
				f.write('<tr><td colspan="8"><h3>')
				f.write(p.title)
				f.write('</h3></td></tr>')
				f.write('<tr>')
				f.write('<td> <b>Date Posted:</b> '+str(p.date_posted)+'</td>')
				f.write('<td> <b>Time Posted:</b> '+str(p.time_posted)+'</td>')
				f.write('<td> <b>Date Closed:</b> '+str(p.date_closed)+'</td>')
				f.write('<td> <b>Time Closed:</b> '+str(p.time_closed)+'</td>')
				f.write('<td> <b>Status:</b> '+p.status+'</td>')
				f.write('<td> <b>Priority:</b> '+p.priority+'</td>')
				f.write('<td> <b>Assigned To:</b> '+p.assigned_to+'</td>')
				f.write('<td> <b>Reported By:</b> '+p.reported_by+'</td>')
				f.write('</tr>')
				f.write('<tr><td colspan="8">')
				f.write(p.description)
				f.write('</td></tr>')
				f.write('<tr><td colspan="8"></td></tr>')
			f.write('''
			  </table>
			  </body>
			  </html>''')

		# highlight the search term within the text:
		with open(os.getcwd()+'/cfcontrolapp/flask_app/search_report/search_output.html', 'r') as file :
			filedata = file.read()
		filedata = filedata.replace(search_term[1:-1], '<b><mark>'+search_term[1:-1]+'</mark></b>')
		with open(os.getcwd()+'/cfcontrolapp/flask_app/search_report/search_output.html', 'w') as file:
			file.write(filedata)

		if email == '':
			pass
		else:
			msg = EmailMessage()
			msg['Subject'] = 'CF Search Report'
			msg['From'] = 'oliver@blissfam.co.uk'
			msg['To'] = email
			msg.set_content('Please find your search report attached:')

			file = os.getcwd()+'/cfcontrolapp/flask_app/search_report/search_output.html'
			with open(file,'rb') as f:
				file_data = f.read()
				file_name = file
				msg.add_attachment(file_data, maintype='application', subtype = 'octet-stream', filename=file_name)

			with smtplib.SMTP_SSL('mail.blissfam.co.uk',465) as smtp:
				smtp.login('oliver@blissfam.co.uk','W14499884pardon1%')
				smtp.send_message(msg)
				smtp.quit()


		return render_template('search.html', post=post, post2=post2, form=form, email=email)
		# return redirect(url_for('search_result',result_search=post))
	else:
		# request.method == 'GET':
		return render_template('search.html',form=form)
        # return render_template('search.html', buggies=buggies)

# @app.route('/search_result/<string:result_search>')
# def search_result(result_search):
#     data = result_search
#     return render_template('search_res.html',data=data)


'''
Backup
'''
@app.route('/backup',methods=['GET', 'POST'])
def backup():
    if request.method == "POST":
        db_connection_str = 'mysql+pymysql://olbliss:creationfest@olbliss.mysql.pythonanywhere-services.com/olbliss$CF'
        db_connection = create_engine(db_connection_str)
        df = pd.read_sql('SELECT * FROM post', con=db_connection)
        html = df.to_html('database.html',index=False)


        msg = EmailMessage()
        timestamp = ('{:%Y%m%d_%H%M}'.format(datetime.datetime.now()))
        msg['Subject'] = timestamp + ' Database Backup'
        msg['From'] = 'oliver@blissfam.co.uk'

        backup.Backup_Email =  request.form["backupemail"]
        msg['To'] = backup.Backup_Email

        msg.set_content('''Please find database backups attached \n \n Timestamp: ''' + timestamp + '''
        \n \n
        To restore the content of the .sql file: \n
        Start a mysql terminal and type: \n
        source [filename].sql;
        '''
        )

        ''' Create .sql and .txt files (using subprocess): '''
        name1 = "mysqldump -u olbliss -h olbliss.mysql.pythonanywhere-services.com 'olbliss$CF' > database_backup.sql"
        subprocess.Popen(name1, shell=True)


        files = ['database.html']
        files.append("database_backup.sql")

        for file in files:
            with open(file,'rb') as f:
                file_data = f.read()
                file_name = file
            msg.add_attachment(file_data, maintype='application', subtype = 'octet-stream', filename=file_name)

        with smtplib.SMTP_SSL('mail.blissfam.co.uk',465) as smtp:
            smtp.login('oliver@blissfam.co.uk','W14499884pardon1%')
            smtp.send_message(msg)
            smtp.quit()
        flash('Backup to email successful!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('backup.html', title='Backup')




'''
POSTS
'''
@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    description=form.description.data,
                    status=form.status.data,
                    priority=form.priority.data,
                    date_posted=form.date_posted.data,
                    time_posted=form.time_posted.data,
                    assigned_to=form.assigned_to.data,
                    reported_by=form.reported_by.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form,
                legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm(request.form)
	if form.validate_on_submit():
		form.populate_obj(post)
		if post.status == 'completed':
			post.date_closed = datetime.datetime.utcnow()+ datetime.timedelta(hours=1) #(BST)
			post.time_closed = datetime.datetime.utcnow()+ datetime.timedelta(hours=1) #(BST)
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.description.data = post.description
		form.date_posted.data = post.date_posted
		form.time_posted.data = post.time_posted
		form.status.data = post.status
		form.priority.data = post.priority
		form.assigned_to.data = post.assigned_to
		form.reported_by.data = post.reported_by
	return render_template('create_post.html', title='Update Post',form=form, legend ='Update Post',post=post)


@app.route("/post/<int:post_id>/markcomplete", methods=['GET', 'POST'])
def mark_complete(post_id):
    post = Post.query.get_or_404(post_id)
    post.status = "completed"
    import datetime
    post.date_closed = datetime.datetime.utcnow() #+ datetime.timedelta(hours=1) #(BST)
    post.time_closed = datetime.datetime.utcnow() #+ datetime.timedelta(hours=1) #(BST)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'danger')
    return redirect(url_for('home'))




'''
BUGGIES
'''
@app.route("/buggy", methods=['GET', 'POST'])
def new_buggy():
    form = BuggyForm()
    if form.validate_on_submit():
        buggy = Buggies(BName=form.BName.data,
                    BRider=form.BRider.data)
        db.session.add(buggy)
        db.session.commit()
        flash('Buggy created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_buggy.html', title='New Buggy', form=form,
                legend='New Buggy')

@app.route("/buggy/list")
def buggy_list():
    buggies = Buggies.query.all()
    return render_template('buggy.html', buggies=buggies)

@app.route("/buggy/<int:buggy_id>")
def buggy(buggy_id):
    buggy = Buggies.query.get_or_404(buggy_id)
    return render_template('buggy.html', buggy=buggy)

@app.route("/buggy/<int:buggy_id>/update", methods=['GET', 'POST'])
def update_buggy(buggy_id):
    buggy = Buggies.query.get_or_404(buggy_id)
    form = BuggyForm()
    if form.validate_on_submit():
        buggy.BName = form.BName.data
        buggy.BRider = form.BRider.data
        db.session.commit()
        flash('Your buggy has been updated!', 'success')
        return redirect(url_for('home', buggy_id=buggy.id))
    elif request.method == 'GET':
        form.BName.data = buggy.BName
        form.BRider.data = buggy.BRider
    return render_template('create_buggy.html', title='New Buggy',
            form=form, legend ='Update Buggy',buggy=buggy)

@app.route("/buggy/<int:buggy_id>/delete", methods=['GET', 'POST'])
def delete_buggy(buggy_id):
    buggy = Buggies.query.get_or_404(buggy_id)
    db.session.delete(buggy)
    db.session.commit()
    flash('Your buggy has been deleted', 'danger')
    return redirect(url_for('home'))



'''
Delete all (reset)
'''
# Delete all posts, not linked anywhere, will have to enter manually
@app.route('/delete',methods=['GET', 'POST'])
@app.route('/remove',methods=['GET', 'POST'])
@app.route('/deleteall',methods=['GET', 'POST'])
def deleteall():
    if request.method == "POST":
        delete_option =  request.form["deleteall"]
        if delete_option == "DELETE" or delete_option == "delete" or delete_option == "Delete":
            # Drop Table (if exists):
            try: Post.__table__.drop(db.engine)
            except: pass
            # Recreate Table:
            Post.__table__.create(db.engine)
            flash('All Posts have been deleted', 'danger')
            return redirect(url_for('home'))
        flash('The word DELETE was not entered correctly, no posts were deleted', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('delete_all.html', title='Delete All')




@app.route('/wysiwyg',methods=['GET', 'POST'])
@app.route('/WYSIWYG',methods=['GET', 'POST'])
def wsi():
    form = PostForm()
    if request.method == "POST":
        # print(request.form.get('editordata'))
        # return 'Posted Data'
        post = Post(title=request.form.get('title'),
                    description=request.form.get('editordata'),
                    status='ongoing',
                    priority = 'low',
                    assigned_to = 'test',
                    reported_by = 'test',
                    )

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('wsi2.html', title='New Post', form=form,
                legend='New Post')






@app.route('/ntest',methods=['GET', 'POST'])
def ntest():
    form = PostForm()
    if request.method == "POST":
        post = Post(title=request.form.get('title'),
                    description = 'test',
                    # description=request.form.get('editordata'),
                    status='ongoing',
                    priority = 'low',
                    assigned_to = 'test',
                    reported_by = 'test',
                    )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('ntest'))
    else:
        posts = Post.query.order_by(Post.priority.asc(),Post.date_posted.asc()).all()
        buggies = Buggies.query.all()
        return render_template('ntest.html', posts=posts, buggies=buggies)


@app.route('/eventplan')
@app.route('/eventplans')
@app.route('/evntplan')
def eventplan():
    return send_from_directory('static', 'Event Plan.pdf')

@app.route('/programme')
@app.route('/program')
@app.route('/programmme')
@app.route('/programe')
def programme():
    return send_from_directory('static', 'Programme.pdf')

@app.route('/map')
@app.route('/sitemap')
def map():
    return send_from_directory('static','sitemap.jpeg')






