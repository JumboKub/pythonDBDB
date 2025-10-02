from dbdb_based import connect

db = connect("mydb.db")
db["foo"] = "bar"
db.commit()

print("Value of foo:", db["foo"])
