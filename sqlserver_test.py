import pyodbc

connection = pyodbc.connect('DSN=<DSN>;UID=<USERNAME>@<HOST>;PWD=<PASSWORD>')

RANDOM_NUMBER_SQL = '''
select
round(((100 - 1 - 1) * rand() + 1), 0) as [random_number]
'''

cursor = connection.cursor()

for row in cursor.execute(RANDOM_NUMBER_SQL):
    print 'random_number = {random_number:.0f}'.format(random_number=row.random_number)