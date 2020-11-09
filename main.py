from app.default_app import app
from utils.database_functions import Database, BASE_DIR
import sys
import os


if len(sys.argv) < 2:
    # Run app
    app()

    # Treminate
    exit()


# IF arguments are passed
argv = sys.argv[1]

if argv == "migrate":
    db = Database()
    print("Migrating database")
    db.migrate_db()
    print("Migrations successfully applied")


if argv == "dropdb":
    print("Deleting database...")
    if os.name == "nt":
        os.system("rm sqlite3.db")
    else:
        os.system("rm -rf sqlite3.db")

    print("Deleted database")


if argv == "test_authenticate":
    from utils.database_functions import Authentication

    authentication = Authentication()

    res = authentication.authenticate(
        email="jhondoe@example.com", password="jhonDoe")
    print(res)

if argv == "test_register":
    from utils.database_functions import Authentication

    authentication = Authentication()
    res = authentication.register(
        name="Jhon Doe", email="jhondoe@example.com", password="jhonDoe")
    print(res)


if argv == "get_all_data":
    db = Database()
    print(db.get_all_data())
