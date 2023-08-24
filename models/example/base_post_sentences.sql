with posts as (
  select * from {{ ref("posts") }}
),

sentences as (
    select 
        *,
        replace(selftext,'"', '') as self_text,
        split(regexp_replace(self_text, '[!.?)]+\\s', 'xxx'), 'xxx') as sentence_text_list
    from posts
),

flatten as (
    select 
        id as post_id,
        author,
        url,
        title,
        s.value :: text as sentence_text,
        {{ dbt_utils.surrogate_key(['post_id', 'index', 'sentence_text']) }} as sentence_id
    from sentences,
        lateral flatten(input => sentence_text_list) as s
)

select * from flatten