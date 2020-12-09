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
    print(res.name)
    print(res.id)

if argv == "test_register":
    from utils.database_functions import Authentication

    authentication = Authentication()
    res = authentication.register(
        name="Jhon Doe", email="jhondoe@example.com", password="jhonDoe")
    print(res.name)
    print(res.id)

if argv == "test_email":
    from utils.driver_functions import send_mail

    send_mail(
        email_to="abrijwasi1@gmail.com",
        subject="Test Email",
        message='<h1>This is a test email</h1>')

if argv == "get_all_data":
    db = Database()
    print("Gathering data...\n")
    users, user_verifications, user_profile = db.get_all_data()
    print(users)
    print(user_verifications)
    print(user_profile)
