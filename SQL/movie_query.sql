show databases;
use movies;
show tables;
select * from moviemeta limit 3;
select 
	COUNT(*) 
from moviemeta
where
	genres like '%Romance%'; #Romance, Comedy, 
    
-- adult ratio
select
	adult, count(*),round(count(*)/(select count(*) from moviemeta), 2) as 'ratio'
from moviemeta
group by adult;

-- budget
select 
	sum(budget)/count(*) as 'average' ,max(budget)
from moviemeta;



