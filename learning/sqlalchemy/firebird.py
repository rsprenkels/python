import logging
import time

from sqlalchemy import create_engine
import re

# need to have FDB python firebird driver installed: https://pypi.org/project/fdb/
# and some libraries: sudo apt-get install firebird3.0-common firebird3.0-utils firebird-dev firebird3.0-doc

# engine = create_engine('mysql+pymysql://etl:fN9GwzhXrYtcrj@dev-reportingdb001.m.int1-dus.dg-ao.de/dwsta')
#engine = create_engine('mysql+pymysql://jdbc:firebirdsql://10.100.211.55:3050/D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB?lc_ctype=UTF8')

engine = create_engine('firebird+fdb://SYSDBA:Guiffez9@10.100.211.55:3050/D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB')

query = """
SELECT
	T.*,
	-- lots of work is available, but throughput in the last minute less than <threshhold>
	CASE WHEN T.num_old_notcompleted_orders >= 1 AND T.num_recently_finished < 5  
		THEN 1
		ELSE 0
	END AS Document_service_is_down
FROM (
	SELECT (
			SELECT
				count(*) AS num_old_notcompleted_orders
			FROM
				DOCUMENT_ORDERS
			WHERE 
				TS_WORK_FINISHED IS NULL -- order not completed
				AND TS_ORDER_CREATED > dateadd( -10 DAY TO CAST('Now' AS DATE)) -- orders created in last 10 days
				AND datediff(SECOND, TS_ORDER_CREATED, CAST('NOW' AS timestamp)) >= 60 -- orders older than 60 seconds
		), (	
			SELECT
				count(*) AS num_recently_finished
			FROM
				DOCUMENT_ORDERS
			WHERE 
				TS_WORK_FINISHED IS NOT NULL -- order completed
				AND TS_ORDER_CREATED > dateadd( -10 DAY TO CAST('Now' AS DATE)) -- orders created in last 10 days
				AND datediff(SECOND, TS_WORK_FINISHED, CAST('NOW' AS timestamp)) < 30 -- finished within the last 30 seconds
		)
	FROM
		RDB$DATABASE rd
) T	
"""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger('queue_moni')

log.info("Starting ...")

while True:
    connection = engine.connect()
    result = connection.execute(query)

    for row in result:
        res = {}
        for k, v in zip(result.keys(), row):
            res[k] = v
        log.info(res)
    connection.close()
    time.sleep(5)

connection.close()