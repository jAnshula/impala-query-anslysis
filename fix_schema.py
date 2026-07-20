import duckdb

con = duckdb.connect("profiles.db")

# Drop broken table if it exists
con.execute("DROP TABLE IF EXISTS profiles")
con.execute("DROP SEQUENCE IF EXISTS profiles_seq")

# Create sequence and table
con.execute("CREATE SEQUENCE profiles_seq START 1")
con.execute("""
    CREATE TABLE profiles (
        id INTEGER PRIMARY KEY DEFAULT nextval('profiles_seq'),
        raw_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

print("Recreated profiles table with auto-increment id using sequence.")


