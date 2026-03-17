"""Diagnostic: see what YOLO detects vs slot positions."""
import cv2, sys
sys.path.insert(0, '.')
from detection.vehicle_detection import VehicleDetector
import mysql.connector

cap = cv2.VideoCapture('parking_feed.mkv')
ret, frame = cap.read()
cap.release()

det = VehicleDetector()
detections = det.detect_vehicles(frame)
print(f"=== YOLO detected {len(detections)} vehicles ===")
for d in detections[:15]:
    print(f"  Box: ({d[0]},{d[1]}) -> ({d[2]},{d[3]})  conf={d[4]:.2f}  class={d[5]}")

conn = mysql.connector.connect(host='localhost', user='root', password='root', database='smart_parking')
cur = conn.cursor(dictionary=True)
cur.execute('SELECT slot_id, slot_label, x1, y1, x2, y2 FROM parking_slots')
slots = cur.fetchall()
conn.close()

print(f"\n=== Checking IoU for {len(slots)} slots ===")
results = det.check_slot_occupancy(detections, slots)
occupied_count = sum(1 for r in results.values() if r['is_occupied'])
print(f"Occupied: {occupied_count} / {len(slots)}")

for sid, r in results.items():
    if r['is_occupied']:
        print(f"  {r['slot_label']}: OCCUPIED (conf={r['confidence']:.2f})")

# Also check with lower threshold
print(f"\n=== With lower IoU threshold (0.05) ===")
for slot in slots:
    slot_box = (slot['x1'], slot['y1'], slot['x2'], slot['y2'])
    for d in detections:
        iou = det.compute_iou(slot_box, d[:4])
        if iou > 0.05:
            print(f"  {slot['slot_label']} overlaps detection({d[0]},{d[1]},{d[2]},{d[3]}): IoU={iou:.3f}")
