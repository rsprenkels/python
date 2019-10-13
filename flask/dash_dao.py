from sqlalchemy import create_engine


def get_migrations():
    # connection_string = "firebird://SYSDBA:Guiffez9@10.100.211.55/3050:D:\\variobill\\production_dg\\data\\DG_VARIOBILL.FDB"
    # from internet engine = create_engine('firebird+fdb://sysdba:masterkey@localhost:3050/c:/fdbb/school.fdb')

    connection_string = 'firebird+fdb://SYSDBA:Guiffez9@10.100.211.55:3050/D:/variobill/production_dg/data/DG_VARIOBILL.FDB'

    engine = create_engine(connection_string)

    connection = engine.connect()

    select_statement = """
        select
           adr.City as city,
           cast (co.date_active as varchar(100)) as date_active,
           count(*) as migrated
        from
           customer cu
           join CONTRACTS co on cu.CUSTOMER_ID = co.CUSTOMER_ID
           join CUSTOMER_ADDRESSES adr on cu.CUSTOMER_ID = adr.CUSTOMER_ID and adr.ADDRESS_TYPE_ID = 10010
        where
           cu.CUSTOMER_ID > 200000000
           and datediff(day, co.date_active, current_date) <= 7 
        group by
           adr.CITY,
           co.date_active
        order by
            co.date_active desc     
    """
    result = connection.execute(select_statement)

    rows = []
    for row in result:
        rows.append (row)

    connection.close()

    return (result.keys(), rows)


def get_data():
    engine = create_engine(
        "mysql+pymysql://etl:fN9GwzhXrYtcrj@dev-reportingdb001.m.int1-dus.dg-ao.de/dwsta")
    connection = engine.connect()
    result = connection.execute("SELECT c.* FROM dwsta.vdgh_customer c limit 3;")

    rows = []
    for row in result:
        rows.append(row)

    connection.close()

    return (result.keys(), rows)
