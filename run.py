from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(

    SECRET_KEY = '12345678',
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost/my_first_database',
    SQLALCHEMY_TRACK_MODIFICATION = False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_flask():

    return 'Hello flask'


@app.route('/new/')
def query_strings(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)

    return '<h1> the greeting is : {0} </h1>'.format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name= 'mina'):
    return '<h1> hello there! : {0} </h1>'.format(name)

# STRINGS
@app.route('/text/<string:name>')
def working_with_string(name):
    return '<h1> here is a string:' + name + '</h1>'

# TEMPLATES
@app.route('/watch')
def movies_2018():
    movie_list = ['autopsy of jane doe'
                  'neon demon',
                  'kong: skull island',
                  'john wich 2',
                  'spiderman - homecoming']
    return render_template('movies.html', movies = movie_list,
                            name = 'Harry')

# TEMPLATES
@app.route('/tables')
def movies_plus():
    movie_dict= {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'kong: skull island': 2.00,
                  'john wich 2': 1.50,
                  'spiderman - homecoming': 02.52}

    return render_template('table_data.html', movies = movie_dict,
                            name = 'Sally')

@app.route('/filters')
def filter_data():
    movie_dict= {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'kong: skull island': 2.00,
                  'john wich 2': 1.50,
                  'spiderman - homecoming': 02.52}

    return render_template('filter_data.html', movies = movie_dict,
                            name = None, film = 'a christmas carol')

@app.route('/macros')
def jinjia_macros():
    movie_dict= {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'kong: skull island': 2.00,
                  'john wich 2': 1.50,
                  'spiderman - homecoming': 02.52}

    return render_template('using_macros.html', movies = movie_dict)

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), primary_key = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Pulisher is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500), nullable = False, index = True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique = True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default = datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        # automatically assign primary key
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = self.num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

if __name__ =='__main__':
    db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5000)
