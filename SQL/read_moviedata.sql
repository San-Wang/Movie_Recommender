DROP TABLE IF EXISTS moviemeta;
CREATE TABLE moviemeta (
  `adult` ENUM('TRUE','FALSE'),  # adult enum('true', 'false')
  `belongs_to_collection` text,
  `budget` bigint(20) DEFAULT NULL,
  `genres` text,
  `homepage` text,
  `id` int,
  `imdb_id` varchar(9),
  `original_language` char(2),
  `original_title` text,
  `overview` text,
  `popularity` float,
  `poster_path` text,
  `production_companies` text,
  `production_countries` text,
  `release_date` text,
  `revenue` int,
  `runtime` int DEFAULT NULL,
  `spoken_languages` text,
  `status` text,
  `tagline` text,
  `title` text,
  `video` ENUM('TRUE','FALSE'),
  `vote_average` double,
  `vote_count` int
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOAD DATA LOCAL INFILE '/Users/San/SelfLearning/RecommendationSystem/Movie_Recommendation/data/movies_metadata.csv' INTO TABLE moviemeta
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES;