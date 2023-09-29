import pytest
import pandas as pd
import numpy as np
import datetime

from ingestion.octoparse.linkedin_etl import LinkedinETL


@pytest.fixture()
def etl():
    return LinkedinETL('linkedin_eu_remote')


@pytest.fixture()
def raw(etl):
    raw_cols = ['Title', 'url', 'company', 'location', 'status', 'date_posted', 'text']
    raw_data = {
        'Title': ['  Junior Software Engineer  ', 'Data Engineer SAP BW/4HANA', 'dummytitle'],
        'url': [' https://ro.linkedin.com/jobs/view/junior-software-engineer ',
                ' https://pt.linkedin.com/jobs/view/data-engineer-sap-bw-4hana-at-tui-3651416465 ', ''],
        'company': ['  University of Oradea  ', ' TUI ', ''],
        'location': ['  Romania  ', ' Lisbon, Lisbon, Portugal ', ''],
        'status': ['   Be an early applicant  ', '  Actively Hiring ', ''],
        'date_posted': ['   16 minutes ago  ', '       23 hours ago ', ' '],
        'text': [
            '  programming skills in Java, Python, C++, C#, and JavaScript.Proficiency in front-end technologies   ',
            ' ',
            '***This role is open to remote work from any location within Portugal or Spain***']
    }
    return pd.DataFrame(raw_data, columns=raw_cols)


@pytest.fixture()
def transformed_generic(etl):
    transformed_cols = ['title', 'url', 'company', 'location', 'status', 'date_posted', 'text']
    transformed_data = {
        'title': ['Junior Software Engineer'],
        'url': ['https://ro.linkedin.com/jobs/view/junior-software-engineer'],
        'company': ['University of Oradea'],
        'location': ['Romania'],
        'status': ['Be an early applicant'],
        'date_posted': ['16 minutes ago'],
        'text': ['programming skills in Java, Python, C++, C#, and JavaScript.Proficiency in front-end technologies']
    }
    return pd.DataFrame(transformed_data, columns=transformed_cols)


@pytest.fixture()
def transformed_generic_date(etl):
    transformed_cols = ['title', 'url', 'company', 'location', 'status', 'date_posted', 'text']

    transformed_data = {
        'title': ['dummy'] * 6,
        'url': ['dummy'] * 6,
        'company': ['dummy'] * 6,
        'location': ['dummy'] * 6,
        'status': ['dummy'] * 6,
        'date_posted': ['1 second ago', '16 minutes ago', '3 hours ago', '1 week ago', '3 jours', '1 day'],
        'text': ['dummy'] * 6
    }
    return pd.DataFrame(transformed_data, columns=transformed_cols)


@pytest.fixture()
def transformed_date(etl, transformed_generic_date):
    today = datetime.date.today()
    transformed_generic_date['created_at'] = [today, today, today, today - datetime.timedelta(weeks=1),
                                              today - datetime.timedelta(days=3), today - datetime.timedelta(days=1)]
    return transformed_generic_date

