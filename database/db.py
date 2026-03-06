from sqlalchemy import create_engine, text
from config import NEON_DATABASE_URL

engine = create_engine(NEON_DATABASE_URL)

def create_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS patient_monitoring (
                id SERIAL PRIMARY KEY,
                heart_rate INT,
                spo2 INT,
                temperature FLOAT,
                bp_systolic INT,
                severity VARCHAR(10),
                reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

# create the table when the module is imported so both the
# consumer and the dashboard can rely on it existing without
# needing to remember to call create_table().
create_table()


def insert_data(vitals, severity, reason):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO patient_monitoring
            (heart_rate, spo2, temperature, bp_systolic, severity, reason)
            VALUES (:hr, :spo2, :temp, :bp, :sev, :reason)
        """), {
            "hr": vitals["heart_rate"],
            "spo2": vitals["spo2"],
            "temp": vitals["temperature"],
            "bp": vitals["bp_systolic"],
            "sev": severity,
            "reason": reason
        })
        conn.commit()

def fetch_data():
    # make sure the table exists before querying (defensive in case
    # create_table wasn't called elsewhere)
    create_table()

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM patient_monitoring
            ORDER BY timestamp DESC
            LIMIT 50
        """))
        return result.fetchall()