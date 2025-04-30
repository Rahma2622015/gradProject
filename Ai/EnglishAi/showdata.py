from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///D:/gradProject/university_information.db"

engine = create_engine(DATABASE_URL, echo=False)

with engine.connect() as conn:
    tables_result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = [row[0] for row in tables_result]
    print("Tables in the database:")
    for table in tables:
        print(f"- {table}")

    for table in tables:
        print(f"\nContents of table '{table}':")
        try:
            result = conn.execute(text(f"SELECT * FROM {table};"))
            for row in result:
                print(row)
        except Exception as e:
            print(f"Error reading table {table}: {e}")
