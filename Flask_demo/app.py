from flask import Flask, render_template

app = Flask(__name__)

# @ signifies a decorator
@app.route('/')
def index():
    return render_template('home.html')
    #return 'Home Page'

@app.route('/about')
def about():
    return render_template('about.html')

# http://127.0.0.1:5000/movieName/God Father
@app.route('/movieName/<movieName>')
def movieName(movieName): # variable name main the same as < >
    return 'Movie Name %s' % movieName

@app.route('/movieId/<int:movieId>')
def movieId(movieId):
    return '<h1>Movie ID %s<h1>' % movieId

@app.route('/profile/<movieName>') 
def profile(movieName):
    return render_template('profile.html', name=movieName)


if __name__ == '__main__':
    #app.run()
    app.run(debug=True) # debug = true will enable see changes just refresh web page
    
