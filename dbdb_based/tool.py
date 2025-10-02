# defines a command-line tool for exploring a database from a terminal window.
# dbdb/tool.py
import sys
from . import connect

def usage():
    print("Usage:")
    print("  python -m dbdb.tool <dbname> get <key>")
    print("  python -m dbdb.tool <dbname> set <key> <value>")
    print("  python -m dbdb.tool <dbname> delete <key>")

def main(argv):
    if not (4 <= len(argv) <= 5):
        usage()
        return "BAD_ARGS"
    dbname, verb, key, value = (argv[1:] + [None])[:4]
    if verb not in {'get', 'set', 'delete'}:
        usage()
        return "BAD_VERB"
    db = connect(dbname)          # CONNECT
    try:
        if verb == 'get':
            sys.stdout.write(db[key])  # GET VALUE
        elif verb == 'set':
            db[key] = value
            db.commit()
        else:
            del db[key]
            db.commit()
    except KeyError:
        print("Key not found", file=sys.stderr)
        return "BAD_KEY"
    return "OK"