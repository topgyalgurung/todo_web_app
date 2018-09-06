#!/usr/bin/python

from flask import Flask, flash, redirect, render_template, request, session, abort
import sqlite3

from flask import g

app = Flask(__name__)

app.database="database.db"

def connect_db():
	return sqlite3.connect(app.database)

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/login')
def login():
	return render_template("todo.html")
		
@app.route('/logout')
def logout():
	flash('Logged out')
	return render_template("index.html")	
	
@app.route("/newuser")
def newuser():
	#return render_template("newuser.html")
	return render_template('newuser.html')

# to do list
@app.route('/todo')
#def todo():
		#return render_template('todo.html')
def item():
	g.db = connect_db()
	if request.method == 'POST':
		if 'new' in request.form:
			addList = request.form['new']
			cur = g.db.execute("SELECT rowid FROM posts WHERE List = ?", (addList,))
			data = cur.fetchone()
			if data is None:
				# Insert new item
				cur = g.db.execute('INSERT into posts (List,Note) VALUES (?,?)', (addList,'Not Done'))
				g.db.commit()
			cur = g.db.execute('select * from posts')
			posts = [dict(List=row[0],Note=row[1]) for row in cur.fetchall()]
			g.db.close()
			return render_template('todo.html',posts=posts)
		elif 'delete' in request.form:
			deleteList = request.form['delete']
			# Delete item 
			cur = g.db.execute('DELETE FROM posts WHERE List = ?', (deleteList,))
			g.db.commit()
			cur = g.db.execute('select * from posts')
			posts = [dict(List=row[0],Note=row[1]) for row in cur.fetchall()]
			g.db.close()
			return render_template('todo.html',posts=posts)
		elif 'mark' in request.form:
				markItem = request.form['mark']
				''' Mark item '''
				cur = g.db.execute('UPDATE posts SET Status = ? WHERE Item = ?', ('Done', markItem))
				g.db.commit()
				cur = g.db.execute('select * from posts')
				posts = [dict(Item=row[0],Status=row[1]) for row in cur.fetchall()]
				g.db.close()
				return render_template('item.html',posts=posts)
	else:
		cur = g.db.execute('select * from posts')
		posts = [dict(List=row[0],Note=row[1]) for row in cur.fetchall()]
		g.db.close()
		return render_template('todo.html',posts=posts)
			


'''create account '''
@app.route('/create', methods=['GET','POST'])
def create():		
	return render_template("newuser.html")
	
@app.route('/register')
def register():
	#return redirect(url_for('index'))
	flash('Now log in')
	return render_template("home.html")



	
if __name__=='__main__':
	app.run(debug=True)