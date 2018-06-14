from flask import Flask, render_template, request, jsonify
import Movie_Recommender


app = Flask(__name__)

# @ signifies a decorator
@app.route('/')
def index():
    return render_template('home.html')
    #return 'Home Page'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile/<movieName>')
def profile(movieName):
    return render_template('profile.html', name=movieName)

# http://127.0.0.1:5000/recommender/The Godfather
@app.route('/recommender/<movieName>')
def recommender(movieName): # variable name need to be the same as < >
    result_overview = Movie_Recommender.recommendation_base_overview(str(movieName), 3)
    result_cast = Movie_Recommender.recommendation_base_crew(str(movieName), 3)
    return render_template('recommender.html', movie = movieName, result = [result_overview,result_cast])

@app.route('/EDA', methods=['GET','POST'])
def GenreTopN():
    if request.method == 'POST': # when the form is submitted
        genre = request.form['Genre']
        top = request.form['Top N']
        return render_template('EDAresult.html',genre=genre,top=top)
    else:
        return render_template('EDARequest_genre.html')

'''
#http://127.0.0.1:5000/EDA?genre=action&top=3
#query string begins after the question mark (?)
# and has two key-value pairs separated by an ampersand (&).
# For each pair, the key is followed by an equals sign (=) and then the value

def queryURL():
    genre = request.args.get('genre') #if key doesn't exist, returns None
    topN = request.args.get('top')
    return 'query result for top {} in genre {}'.format(topN, genre)
'''
if __name__ == '__main__':
    #app.run()
    app.run(debug=True) # debug = true will enable see changes just refresh web page
    
