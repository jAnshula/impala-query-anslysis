import duckdb

con = duckdb.connect("profiles.db")

# Rename old table if it exists
try:
    con.execute("ALTER TABLE profiles RENAME TO profiles_old")
    print("Renamed old profiles table to profiles_old")
except Exception:
    print("No existing profiles table to rename.")

# Create new schema with raw_text column
con.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY,
        raw_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
print("Created new profiles table with raw_text column.")

# Copy over old data if available
try:
    con.execute("""
        INSERT INTO profiles (raw_text, created_at)
        SELECT '' AS raw_text, created_at FROM profiles_old
    """)
    print("Migrated old rows into new schema (raw_text left empty).")
except Exception:
    print("No old rows to migrate.")



