from dbdb_based import connect

def main():
    # Open or create database file
    db = connect("mydb.db")

    # Insert some values
    db["foo"] = "bar"
    db["hello"] = "world"
    db["number"] = "123"

    # Commit changes to disk
    db.commit()
    print("✅ Data committed to mydb.db")

    # Read values back
    print("foo ->", db["foo"])
    print("hello ->", db["hello"])
    print("number ->", db["number"])

if __name__ == "__main__":
    main()
