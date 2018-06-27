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
def profile(movieName): # variable name need to be the same as < >
    return render_template('profile.html', name=movieName)

# http://127.0.0.1:5000/recommender/the Godfather
# @app.route('/recommender/<MovieName>')
@app.route('/recommender', methods=['GET','POST'])
def recommender():
    if request.method == 'POST':
        MovieName = request.form['Movie Name']
        top = int(request.form['Top N'])
        result_overview = Movie_Recommender.recommendation_base_overview(str(MovieName), top)
        poster_html = Movie_Recommender.display_posters(result_overview)
        result_cast = Movie_Recommender.recommendation_base_crew(str(MovieName), top)
        return render_template('RecommenderResult.html', MovieName = MovieName, top=top, result = [result_overview, result_cast,poster_html])
    else:
        return render_template('RecommenderRequest.html')

@app.route('/EDA', methods=['GET','POST'])
def GenreTopN():
    if request.method == 'POST': # when the form is submitted
        genre = request.form['Genre']
        top = request.form['Top N']
        min_count = request.form['Min Rate Count']
        result = Movie_Recommender.top_by_genre(genre,min_count,top)
        return render_template('EDAResult.html', genre=genre, top=top,min_count=min_count,result=result)
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
    
