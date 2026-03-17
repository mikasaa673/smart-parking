import mysql.connector
cfg = dict(host='localhost', user='root', password='root', database='smart_parking')
conn = mysql.connector.connect(**cfg)
c = conn.cursor()

# 1. Add 'expired' to ENUM for future-proofing
c.execute("ALTER TABLE reservations MODIFY COLUMN status ENUM('active','completed','cancelled','expired') DEFAULT 'active'")
print('ENUM updated: added expired')

# 2. Cancel all stuck reservations (created >15 min ago, slot unoccupied, still active)
c.execute("""
    UPDATE reservations r
    JOIN parking_slots p ON r.slot_id = p.slot_id
    SET r.status = 'cancelled'
    WHERE r.status = 'active'
      AND r.created_at <= NOW() - INTERVAL 15 MINUTE
      AND p.is_occupied = FALSE
""")
print(f'Cancelled {c.rowcount} stuck reservation(s)')

conn.commit()
conn.close()
print('DB migration complete!')
