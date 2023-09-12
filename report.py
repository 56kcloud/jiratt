import argparse
import humanize
from datetime import datetime

from jira import JIRA
from os import environ
from datetime import date
from dateutil import parser
from tabulate import tabulate

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

jira = JIRA(
    options={
        'server': environ['JIRA_SERVER']
    },
    basic_auth=(
        environ['JIRA_EMAIL'],
        environ['JIRA_API_KEY']
    )
)


def str_to_date(s):
    return parser.parse(s).date()


def get_worklogs(project, username, date_from, date_to):
    df = date_from.strftime('%Y/%m/%d')
    dt = date_to.strftime('%Y/%m/%d')
    query = f'project="{project}" AND worklogAuthor="{username}" AND worklogDate>="{df}" AND worklogDate<="{dt}"'
    print(f'\nRUNNING QUERY')
    print(f'=============')
    print(f'{query}')
    issues = jira.search_issues(query, maxResults=0)
    results = []
    for issue in issues:
        worklogs = jira.worklogs(issue.key)
        for i in range(len(worklogs)):
            logged_at = str_to_date(worklogs[i].started)
            author = str(worklogs[i].author)
            if logged_at >= date_from and logged_at <= date_to and author == username:
                results.append({
                    'issue': issue.key,
                    'author': worklogs[i].author,
                    'started': worklogs[i].started,
                    'updated': worklogs[i].updated,
                    'timespent': worklogs[i].timeSpentSeconds
                })
    return results


def get_current_year():
    return 2023


def add_arguments(parser):
    """ Parse arguments passed to CLI
    """
    parser.add_argument('--username', required=True, type=str, help='JIRA user name.')
    parser.add_argument('--project', default='AWS', type=str, help='JIRA project name.')
    parser.add_argument('--date-from', required=True, type=str, help='Start date, eg. 2023/04/01')
    parser.add_argument('--date-to', required=True, type=str, help='End date, eg. 2023/04/30')
    return parser.parse_args()


def main(args):
    """ The main
    """
    date_from = str_to_date(args.date_from)
    date_to = str_to_date(args.date_to)
    worklogs = get_worklogs(args.project, args.username, date_from, date_to)
    timespent_total = sum([w['timespent'] for w in worklogs])

    for i in range(len(worklogs)):
        started = datetime.strptime(
            worklogs[i]['started'], DATE_TIME_FORMAT)
        worklogs[i]['started'] = started.strftime(
            "%m/%d/%Y, %H:%M:%S")
        worklogs[i]['timespent'] = humanize.precisedelta(
            worklogs[i]['timespent'], suppress=['days'])

    worklogs = sorted(worklogs, key=lambda x:x['started'])

    print('\nJIRA WORKLOGS')
    print('=============')
    print(f'username:', args.username)
    print(f'project:', args.project)
    print(f'period:', date_from.strftime('%Y/%m/%d'),
          '..', date_to.strftime('%Y/%m/%d'))
    print('\n', tabulate(worklogs, headers='keys'))

    print(
        f"\nTOTAL: {humanize.precisedelta(timespent_total, suppress=['days'])}\n")


if __name__ == "__main__":
    """ The real main
    """
    main(add_arguments(argparse.ArgumentParser()))
