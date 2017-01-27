#!/usr/bin/python

"""
Test connection to database
"""

import os
import sys
import psycopg2

db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_port = os.environ['DB_PORT']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASS']
db_check_timeout = os.environ['DB_CHECK_TIMEOUT']

try:
    print 'Checking database connection on %s:%s with timeout of %ss' % (db_host, db_port, db_check_timeout)
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port,
        connect_timeout=db_check_timeout)
    cursor = conn.cursor()
    print 'SUCCESS: Connected to database'
except:
    # Get the most recent exception
    _, error, _ = sys.exc_info()
    sys.exit("ERROR: Database connection failed\n %s" % (error))
