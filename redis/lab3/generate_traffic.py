"""
Лабораторна робота №3, завдання 3.
Генерація випадкових подій вебтрафіку та запис їх у Redis Stream traffic:events.

Запуск:  python3 generate_traffic.py
"""

import random
import time

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

CITIES = ["kyiv", "lviv", "odessa", "kharkiv", "dnipro"]

# HTTP-статуси з вагами: успішних відповідей у реальному трафіку значно більше
STATUSES = [200, 301, 404, 500]
STATUS_WEIGHTS = [80, 8, 9, 3]

EVENTS_COUNT = 500

now_ms = int(time.time() * 1000)
hour_ms = 3600 * 1000

for i in range(EVENTS_COUNT):
    # час події: випадковий момент за останню добу
    event_time_ms = now_ms - random.randint(0, 24 * hour_ms)

    event = {
        "time": event_time_ms,
        "city": random.choice(CITIES),
        "bytes": random.randint(100, 5000),
        "status": random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0],
    }
    r.xadd("traffic:events", event)

print("Додано подій:", EVENTS_COUNT)
print("XLEN traffic:events =", r.xlen("traffic:events"))
