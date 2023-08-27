select
    id,
    len(text) - len(cleaned_text) as diff_characters
from {{ ref('stg_texts' )}}
having not(diff_characters >= 0)