from sqlalchemy import create_engine
import re

# engine = create_engine('mysql+pymysql://etl:fN9GwzhXrYtcrj@dev-reportingdb001.m.int1-dus.dg-ao.de/dwsta')
#engine = create_engine('mysql+pymysql://jdbc:firebirdsql://10.100.211.55:3050/D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB?lc_ctype=UTF8')

engine = create_engine('firebird+fdb://SYSDBA:Guiffez9@10.100.211.55:3050/D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB')


connection = engine.connect()

result = connection.execute("""
select
	CUSTOMER_ID,
	ADDRESS_TYPE_ID,
	HOUSENO
from
	CUSTOMER_ADDRESSES
""")

print(f"result is a {type(result)}")

print(f"this result has {result.keys()}")

for row in result:
    # print(f"got {row} {row[2]}")
    if row[2] != None:
        result = re.match(r"[^0-9]", row[2])
        if result != None:
            print(f"got {row}")

connection.close()