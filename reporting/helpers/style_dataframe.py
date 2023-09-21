import pandas as pd

def create_color(type, decrease_step):
    good = tuple([80, 200, 120])
    bad = tuple([137, 148, 153])
    neutral = tuple([138, 154, 91])

    if type == 'good':
        return f'rgba{good + tuple([0.9 - decrease_step])}'
    if type == 'bad':
        return f'rgba{bad + tuple([0.9 - decrease_step])}'
    if type == 'neutral':
        return f'rgba{neutral + tuple([0.9 - decrease_step])}'


def highlight_quant_column(s):
    mean = s.median()
    return [f'background-color: {create_color("good", 0)}' if v > mean
            else f'background-color: {create_color("neutral", 0)}' if mean - 0.1 < v < mean + 0.1 or v == 0 or pd.isna(v)
            else f'background-color: {create_color("bad", 0)}' for v in s]


def highlight_title(s):
    is_junior = r'junior'
    is_senior = r'senior|lead|confirmed|confirmé|expérimenté'
    is_graduate = r'apprenti|stagiaire|stage|intern|alternan'
    if s.str.contains(is_graduate, regex=True, case=False)['title']:
        return [f'background-color: {create_color("bad", 0)}']
    elif s.str.contains(is_senior, regex=True, case=False)['title']:
        return [f'background-color: {create_color("bad", 0)}']
    elif s.str.contains(is_junior, regex=True, case=False)['title']:
        return [f'background-color: {create_color("good", 0)}; color: white; font-weight: bold;']
    else:
        return [f'background-color: {create_color("good", 0)}']

def highlight_english_text(s):
    pass



