import snowflake.connector
from datetime import datetime

from config.definitions import PROJECT_PATH, SNOWFLAKE_ACCOUNT, SNOWFLAKE_ROLE, SNOWFLAKE_USER, SNOWSQL_PWD, WAREHOUSE

conn = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWSQL_PWD,
    database='ANALYTICS',
    schema='MARTS',
    role=SNOWFLAKE_ROLE,
    warehouse=WAREHOUSE
)
cur = conn.cursor()


def fetch_companies():
    try:
        # We want to scrape companies from new listings that aren't present in the companies table
        cur.execute(
            "SELECT DISTINCT(company) "
            "FROM jobs_technos_agg j"
            "JOIN companies c"
            "ON j.company = c.name "
            "WHERE j.company NOT IN ("
            "   SELECT name FROM companies"
            ");"
        )
        data = cur.fetchall()
    except snowflake.connector.errors.ProgrammingError as e:
        # default error message
        print(e)
        # customer error message
        print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
    finally:
        cur.close()
        return [t[0] for t in data]


def generate_urls(companies):
    formatted_companies = [company.split('|')[0] for company in companies]
    formatted_companies = [company.replace(' ', '%20') for company in formatted_companies]
    base_url = 'https://www.glassdoor.com/Search/results.htm?keyword={}'
    return [base_url.format(company) for company in formatted_companies]


def save_to_file(urls):
    now = datetime.now().strftime('%Y-%m-%d')
    path = PROJECT_PATH / 'ingestion' / 'octoparse' / 'data' / 'glassdoor' / f'companies_{now}.txt'
    file = open(path, 'w+')
    for url in urls:
        file.write(url + "\n")


if __name__ == '__main__':
    companies = fetch_companies()
    urls = generate_urls(companies)
    save_to_file(urls)
