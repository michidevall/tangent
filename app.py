from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask (__name__)
# if ENV =='dev':
    # app.debug = True
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://wychojhczcvivp:69fdfc319c2ab408e3ed5ea77dd4281cf676a52151aa9ed7f2e57f590279766c@ec2-18-232-216-229.compute-1.amazonaws.com:5432/dd2m4v3ljrejpd'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE-URI'] = 'postgres://postgres://wychojhczcvivp:69fdfc319c2ab408e3ed5ea77dd4281cf676a52151aa9ed7f2e57f590279766c@ec2-18-232-216-229.compute-1.amazonaws.com:5432/dd2m4v3ljrejpd'

#     app.config['SQLALCHEMY_TRACK_MOSIFICATIONS'] = False
    
db = SQLAlchemy(app)

class Tangent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return self.title

db.create_all()
db.session.commit()


@app.route('/')
@app.route('/home')
@app.route('/tangent')
def Welcome():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = Tangent(title=post_title, content=post_content, posted_by=post_author)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Tangent.query.order_by(Tangent.posted_on).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = Tangent.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = Tangent.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.author =request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html', post=to_edit)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = Tangent(title=post_title,content=post_content, posted_by=post_author)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')



if __name__ == "__main__":
    app.run(debug=True)