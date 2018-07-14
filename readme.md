## Movie Recommender Project  
A  recommendation system using content-based & collaborative filtering methods.  

Current demo:  
<a href="https://imgflip.com/gif/2cuv3v"><img src="https://i.imgflip.com/2cuv3v.gif" width="500px" height="300px" title="movie recommender demo"/></a>  


## Overview  
A  recommendation system using content-based & collaborative filtering methods.   
Here is a workflow overview about my demo:  
![workflow](/output/workflow.png)  

**What it can do:**  
* recommend movies based on movie's **plot** or **cast**(director & main actors and actresses)  
* recommend movies based on **personal taste**  

[Data Source](https://www.kaggle.com/rounakbanik/the-movies-dataset/data)

**methods:**   
* content-based: NLTK, scikit-learn, TFIDF
* collaborative filtering: surprise, pyspark(final demo)

demo: flask(finished), mySQL(finished), Spark(final demo)


Home page:  
![home page](/output/HomePage.png)   

About page:  
![about](/output/about.png)  

Recommendation example:  

Request Page:  
![Request Page](/output/RecommendRequest.png)  
Recommendation Result Page:  
![RecommendResult1](/output/RecommendResult1.png)  
![RecommendResult2](/output/RecommendResult2.png)  

Best movie by genres:  
![ExploreRequest](/output/ExploreRequest.png)   
![ExploreResult](/output/ExploreResult.png)   




TODO list:   
* [x] Build local host demo website(flask)  
* [x] Connect mySQL with flask
* [x] Add Tableau EDA dashboard
* [ ] Display movie poster images in recommendation result
* [ ] Save similarity matrix to speed start  
* [ ] Using pyspark library to do collaborative filtering instead of surprise.SVD
* [ ] recommend movie based on poster style? Is it feasible?

File Structure:  
Movie_Recommendation:  
|-- data
|-- explore: playing script 
|-- Flask_demo
|	|-- app.py
|	|-- requirments.txt
|	|-- static: 
|	|-- templates: 
|-- Movie_Recommender.py: main engine
|-- Present: images used for blog
|-- readme.md
|-- reference.txt
|-- SQL: mySQL related






