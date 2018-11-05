from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://etl:fN9GwzhXrYtcrj@dev-reportingdb001.m.int1-dus.dg-ao.de/dwsta')

connection = engine.connect()

result = connection.execute("SELECT * FROM dwsta.vdgh_customer limit 10;")

print(f"result is a {type(result)}")

print(f"this result has {result.keys()}")

for row in result:
    print(f"got {row}")

connection.close()