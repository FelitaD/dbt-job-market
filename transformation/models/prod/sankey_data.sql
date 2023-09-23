with raw as (select * from {{ source('raw_job_postings', 'raw_job_postings') }}),
stg_job_postings as (select * from {{ ref('stg_job_postings') }}),
jobs as (select * from {{ ref('jobs') }}),
scores as (select * from {{ ref('scores') }}),

rawc as ( select 1 as a, count(distinct(url)) as raw from raw ),
jobsc as ( select 1 as a, count(distinct(j.id)) as jobs from jobs j ),
relevantc as ( select 1 as a, count(distinct(j.id)) as relevant from jobs j join scores s on j.id = s.id where is_relevant = 1 ),
seniorc as ( select 1 as a, count(*) as senior from jobs j join scores s on j.id = s.id where is_relevant = 1 and seniority_score = -1 ),
juniorc as ( select 1 as a, count(*) as junior from jobs j join scores s on j.id = s.id where is_relevant = 1 and seniority_score = 3 ),
unspecifiedc as ( select 1 as a, count(*) as unspecified from jobs j join scores s on j.id = s.id where is_relevant = 1 and seniority_score = 1 ),
graduatec as ( select 1 as a, count(*) as graduate from jobs j join scores s on j.id = s.id where is_relevant = 1 and seniority_score = 0 )

select raw, jobs, relevant, senior, junior, graduate, unspecified
from rawc 
join jobsc using(a)
join relevantc using(a)
join seniorc using(a)
join juniorc using(a)
join graduatec using(a)
join unspecifiedc using(a)