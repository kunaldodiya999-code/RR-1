import sqlite3


def connect():
    return sqlite3.connect("rr_monitor.db", check_same_thread=False)


def init_db():

    conn = connect()
    cur = conn.cursor()

    # ---------------- SETTINGS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        trade_mode TEXT,
        capital REAL,
        parts INTEGER,
        trail_on TEXT,
        trail_trigger REAL,
        trail_move REAL,
        breakeven_trigger REAL
    )
    """)

    # ---------------- TRADES TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT,
        symbol TEXT,
        side TEXT,
        qty INTEGER,
        entry REAL,
        sl REAL,
        target REAL,
        rr REAL,
        status TEXT,
        pnl REAL,
        entry_time TEXT,
        exit_time TEXT
    )
    """)

    # ---------------- AUTO MIGRATIONS ----------------
    migrations = [
        ("ALTER TABLE settings ADD COLUMN live_master TEXT DEFAULT 'OFF'"),
    ]

    for sql in migrations:
        try:
            cur.execute(sql)
        except:
            pass

    # ---------------- DEFAULT SETTINGS ----------------
    cur.execute("SELECT COUNT(*) FROM settings")
    count = cur.fetchone()[0]

    if count == 0:

        cur.execute("""
        INSERT INTO settings
        (
            id,
            trade_mode,
            capital,
            parts,
            trail_on,
            trail_trigger,
            trail_move,
            breakeven_trigger,
            live_master
        )
        VALUES
        (
            1,
            'PAPER',
            100000,
            10,
            'ON',
            1,
            0.5,
            2,
            'OFF'
        )
        """)

    else:
        try:
            cur.execute("""
            UPDATE settings
            SET live_master='OFF'
            WHERE live_master IS NULL
            """)
        except:
            pass

    conn.commit()
    conn.close()
