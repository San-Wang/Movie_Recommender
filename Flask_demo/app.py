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

# http://127.0.0.1:5000/recommender/The Godfather
@app.route('/recommender/<movieName>')
def recommender(movieName): # variable name need to be the same as < >
    result_overview = Movie_Recommender.recommendation_base_overview(str(movieName), 3)
    result_cast = Movie_Recommender.recommendation_base_crew(str(movieName), 3)
    return render_template('recommender.html', movie = movieName, result = [result_overview,result_cast])


@app.route('/profile/<movieName>') 
def profile(movieName):
    return render_template('profile.html', name=movieName)


if __name__ == '__main__':
    #app.run()
    app.run(debug=True) # debug = true will enable see changes just refresh web page
    
