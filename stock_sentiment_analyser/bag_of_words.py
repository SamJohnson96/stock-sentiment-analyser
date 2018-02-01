import sys
import logging
import pymysql

#rds settings
rds_host  = "stockbot.c0mj2r8tlwe3.eu-west-2.rds.amazonaws.com"
name = "admin"
password = "mypassword"
db_name = "stockbot"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def lambda_handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        cur.execute('insert into users (name) values("Joe")')
        conn.commit()
        cur.execute("SELECT * FROM articles AS r1 JOIN (SELECT CEIL(RAND() * (SELECT MAX(id) FROM articles)) AS id) AS r2 WHERE r1.id >= r2.id ORDER BY r1.id ASC LIMIT 500")
        for row in cur:
            item_count += 1
            logger.info(row)
            print(row)

    return "Added %d items from RDS MySQL table" %(item_count)
