from sqlalchemy import create_engine
import re

dwh = create_engine('mysql+pymysql://etl:fN9GwzhXrYtcrj@dev-reportingdb001.m.int1-dus.dg-ao.de/stage')
dwh_connection = dwh.connect()

plm = create_engine('mysql+pymysql://plm_prod:plm_prod@mysql003.int1-dus.dg-ao.de:3306/plm')
plm_connection = plm.connect()

# engine = create_engine('firebird+fdb://SYSDBA:Guiffez9@10.100.211.55:3050/D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB')



dwh_projects = dwh_connection.execute(""" select * from plm_project """).fetchall()

plm_projects = plm_connection.execute(""" select * from project """).fetchall()


# print(f"result is a {type(dwh_result)}")

# print(f"this result has {dwh_result.keys()}")

print(f"dwh has {len(dwh_projects)} projects")
print(f"plm has {len(plm_projects)} projects")

# for row in dwh_projects:
    # print(f"got {row} {row[2]}")

dwh_connection.close()
