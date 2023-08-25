with jobs as (
  select * from {{ ref("int_job_postings") }}
),

sentences as (
    select 
        *,
        split(regexp_replace(text, '[!.?)]+\\s', 'xxx'), 'xxx') as sentence_text_list
    from jobs
)

select * from sentences