from dbdb_based import connect

def main():
    # Open the existing database
    db = connect("mydb.db")

    try:
        print("foo ->", db["foo"])
        print("hello ->", db["hello"])
        print("number ->", db["number"])
    except KeyError as e:
        print("❌ Key not found:", e)

if __name__ == "__main__":
    main()
