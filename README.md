⏰ JIRA Time Tracker
===================

Tired of manually summarizing your JIRA worklogs?

Here is a Python script that automates this.

Installation
------------

Clone this repository:

	$ git clone https://github.com/56kcloud/jiratt.git

Create a Python virtual environment and install dependencies:

	$ python3.9 -m venv .venv
	$ source .venv/bin/activate
	$ pip install -r requirements.txt

Setup environment variables (using an envdir):

	$ cp -r env.example env
	$ echo "me@monkeycorp.com" > env/JIRA_EMAIL
	$ echo "secret-api-key" > env/JIRA_API_KEY
	$ echo "https://monkeycorp.atlassian.net" > env/JIRA_SERVER


Usage
-----

	$ envdir env python report.py --username "JIRA Username" --date-from 2023/07/01 --date-to 2023-07-31

Example
-------

	$ envdir env python report.py --username me@monkeycorp.com --date-from 2023/07/01 --date-to 2023-07-31

	RUNNING QUERY
	=============
	project="AWS" AND worklogAuthor="me@monkeycorp.com" AND worklogDate>="2023/07/01" AND worklogDate<="2023/07/31"

	JIRA WORKLOGS
	=============
	username: me@monkeycorp.com
	project: AWS
	period: 2023/07/01 .. 2023/07/31

	 issue    author            started                       updated                         timespent
	-------  ----------------  ----------------------------  ----------------------------  -----------
	AWS-456  me@monkeycorp.com  2023-07-29T01:55:01.135+0200  2023-07-31T10:55:34.989+0200       205200
	AWS-456  me@monkeycorp.com  2023-07-31T16:02:09.999+0200  2023-08-01T08:02:18.950+0200        57600
	AWS-455  me@monkeycorp.com  2023-07-31T02:44:55.231+0200  2023-07-31T10:44:59.660+0200        28800
	AWS-454  me@monkeycorp.com  2023-07-31T02:43:52.635+0200  2023-07-31T10:44:12.159+0200        28800
	AWS-322  me@monkeycorp.com  2023-07-03T09:00:00.000+0200  2023-07-31T10:41:16.611+0200        57600
	AWS-204  me@monkeycorp.com  2023-07-04T10:18:24.631+0200  2023-07-04T11:18:48.958+0200         3600
	AWS-108  me@monkeycorp.com  2023-07-30T18:41:49.415+0200  2023-07-31T10:42:17.272+0200        57600

	TOTAL: 122 hours
