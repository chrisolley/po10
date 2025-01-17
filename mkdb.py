import psycopg2
import os


def ProcessData(SQLConn, schema, table):

    # Open a cursor
    SQLCursor = SQLConn.cursor()

    # Check existence
    print('Checking existence')
    SQLCursor.execute(f"select exists(select * from information_schema.tables where table_name='{table}');")

    print('Dropping')
    if SQLCursor.fetchone()[0]:  # if existence == true, drop table
        print('Found Table')
        SQLCursor.execute(f"drop table {schema}.{table};")  # drop table
        print('Dropped table')
        SQLConn.commit()

    # create table
    print('Creating Table')
    SQLCursor.execute(
        f"create table {schema}.{table}(sex varchar(3), event varchar(10), ranking varchar(10), time interval,\
        name varchar(40), club varchar(40), date date);")

    # copy data to table from csv
    # SQLCursor.execute(f"copy {schema}.{table} from {os.path.abspath('data_test.csv')}CSV;")
    print('Copying data')
    SQLCursor.execute("""COPY %s.%s FROM '%s'CSV;""" % (schema, table, os.path.abspath('data.csv')))
    SQLConn.commit()


connection = psycopg2.connect("dbname='po10db' user='' host='localhost' password=''")
ProcessData(connection, 'public', 'po10')