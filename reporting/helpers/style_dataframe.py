import pandas as pd


def create_color(type, decrease_step: float):
    good = tuple([24,101,98])
    bad = tuple([148,94,25])
    neutral = tuple([230,232,214])

    if type == 'good':
        return f'rgba{good + tuple([1 - decrease_step])}'
    if type == 'bad':
        return f'rgba{bad + tuple([1 - decrease_step])}'
    if type == 'neutral':
        return f'rgba{neutral + tuple([1 - decrease_step])}'


def highlight_row(s):
    score = s['total_score']
    if score == 6:
        return [f'background-color: {create_color("good", 0)}'] * len(s)
    elif score == 5:
        return [f'background-color: {create_color("good", 0.2)}'] * len(s)
    elif score == 4:
        return [f'background-color: {create_color("good", 0.4)}'] * len(s)
    elif score == 3:
        return [f'background-color: {create_color("good", 0.6)}'] * len(s)
    elif score == 2:
        return [f'background-color: {create_color("good", 0.8)}'] * len(s)
    elif score == 1:
        return [f'background-color: {create_color("neutral", 0.6)}'] * len(s)
    elif score == 0:
        return [f'background-color: {create_color("bad", 0.8)}'] * len(s)
    elif score == -1:
        return [f'background-color: {create_color("bad", 0.6)}'] * len(s)
    elif score == -2:
        return [f'background-color: {create_color("bad", 0.4)}'] * len(s)
    elif score == -3:
        return [f'background-color: {create_color("bad", 0.2)}'] * len(s)
    elif score == -4:
        return [f'background-color: {create_color("bad", 0)}'] * len(s)
    else:
        return [''] * len(s)


def highlight_quant_column(s):
    mean = s.median()
    return [f'background-color: {create_color("good", 0)}' if v > mean
            else f'background-color: {create_color("neutral", 0)}' if mean - 0.1 < v < mean + 0.1 or v == 0 or pd.isna(v)
            else f'background-color: {create_color("bad", 0)}' for v in s]


def highlight_english_text(s):
    pass



