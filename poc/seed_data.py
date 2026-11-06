#!/usr/bin/env python3
"""
Заповнює MongoDB, ScyllaDB та Redis тестовими даними для POC (варіант №1 як приклад).
Запуск: після `docker compose up -d` у каталозі poc — `python seed_data.py`
"""

from __future__ import annotations

import random
import time
from datetime import datetime, timedelta, timezone

from cassandra.cluster import Cluster
from pymongo import MongoClient
import redis

# Локальні дефолти (як у методичці)
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "app_db"
REDIS_URL = "redis://localhost:6379/0"
SCYLLA_HOSTS = ["127.0.0.1"]
OBJECT_ID = "variant_01_smart_flat"
REDIS_HASH = "device:state"


def seed_mongo(client: MongoClient) -> None:
    db = client[DB_NAME]
    db.sensors.delete_many({})
    db.rules.delete_many({})

    sensors = [
        {
            "code": "temp",
            "name": "Температура вітальня",
            "unit": "°C",
            "ieee_address": "0x00158d00045b2c91",
            "vendor": "Aqara",
            "model": "WSDCGQ11LM",
            "specs": {"value_min": -20, "value_max": 60, "accuracy": 0.3, "zone": "living_room"},
        },
        {
            "code": "humidity",
            "name": "Вологість",
            "unit": "%",
            "ieee_address": "0x00158d00045b2c92",
            "vendor": "Aqara",
            "model": "WSDCGQ11LM",
            "specs": {"value_min": 0, "value_max": 100, "accuracy": 3, "zone": "living_room"},
        },
        {
            "code": "lux",
            "name": "Освітленість",
            "unit": "Lux",
            "ieee_address": "0x00158d00045b2c93",
            "vendor": "Sonoff",
            "model": "SNZB-06P",
            "specs": {"value_min": 0, "value_max": 10000, "mount": "ceiling"},
        },
    ]
    db.sensors.insert_many(sensors)

    rule = {
        "object_name": "Розумна квартира",
        "object_id": OBJECT_ID,
        "metric": "temp",
        "operator": ">",
        "threshold": 26.0,
        "active_state": "COOLING",
        "normal_state": "NORMAL",
    }
    db.rules.insert_one(rule)
    print("MongoDB: колекції sensors та rules заповнені.")


def ensure_scylla_table(session) -> None:
    # Scylla 2026: SimpleStrategy несумісний з tablet replication — використовуємо NTS.
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS smart_monitoring
        WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 1}
        AND tablets = {'enabled': false};
        """
    )
    session.set_keyspace("smart_monitoring")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_history (
            object_id text,
            ts timestamp,
            val1 double,
            val2 double,
            val3 double,
            alert_triggered int,
            PRIMARY KEY (object_id, ts)
        ) WITH CLUSTERING ORDER BY (ts DESC);
        """
    )


def seed_scylla(session) -> None:
    ensure_scylla_table(session)
    session.execute("DELETE FROM sensor_history WHERE object_id = %s", (OBJECT_ID,))

    now = datetime.now(timezone.utc).replace(microsecond=0)
    start = now - timedelta(hours=12)
    threshold = 26.0

    insert = session.prepare(
        """
        INSERT INTO sensor_history (object_id, ts, val1, val2, val3, alert_triggered)
        VALUES (?, ?, ?, ?, ?, ?)
        """
    )

    rng = random.Random(42)
    for i in range(720):
        ts = start + timedelta(minutes=i)
        # val1 = temp (основна метрика для графіка №1)
        base = 22.0 + 4.0 * (i % 180) / 180.0
        noise = rng.uniform(-0.8, 0.8)
        temp = round(base + noise, 2)
        if rng.random() < 0.08:
            temp = round(threshold + rng.uniform(0.3, 3.0), 2)
        hum = round(40 + rng.uniform(-10, 15), 2)
        lux = round(100 + rng.uniform(0, 400), 2)
        alert = 1 if temp > threshold else 0
        session.execute(insert, (OBJECT_ID, ts, temp, hum, lux, alert))

    print("ScyllaDB: 720 рядків sensor_history додано.")


def seed_redis(r: redis.Redis) -> None:
    r.delete(REDIS_HASH)
    mapping = {
        "temp": "24.5",
        "humidity": "48.0",
        "lux": "220.0",
        "actuator_status": "NORMAL",
        "linkquality": "180",
        "battery_mv": "2990",
        "rssi_dbm": "-61",
    }
    r.hset(REDIS_HASH, mapping=mapping)
    print("Redis: hash device:state ініціалізовано.")


def main() -> None:
    print("Очікування сервісів (5 с)…")
    time.sleep(5)

    mc = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10000)
    mc.admin.command("ping")
    seed_mongo(mc)

    cluster = Cluster(SCYLLA_HOSTS, connect_timeout=30)
    session = cluster.connect()
    seed_scylla(session)
    cluster.shutdown()

    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
    seed_redis(r)

    print("Готово. Запустіть: uvicorn main:app --reload --port 8000")


if __name__ == "__main__":
    main()
