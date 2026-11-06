"""
Простий POC FastAPI для перевірки ланцюга MongoDB + Redis + ScyllaDB
(ендпоінти узгоджені з промптом у docs/index.html).
"""

from __future__ import annotations

import json
import os
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pymongo import MongoClient
import redis

HERE = os.path.dirname(os.path.abspath(__file__))

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB", "app_db")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
SCYLLA_HOSTS = os.environ.get("SCYLLA_HOSTS", "127.0.0.1").split(",")
CACHE_KEY = "cache:dashboard:analytics"
REDIS_HASH = "device:state"

app = FastAPI(title="Database Labs POC")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_mongo: MongoClient | None = None
_redis: redis.Redis | None = None
_scylla_session = None
_scylla_cluster = None


def mongo_db():
    global _mongo
    if _mongo is None:
        _mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    return _mongo[DB_NAME]


def rds() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    return _redis


def scylla():
    global _scylla_session, _scylla_cluster
    if _scylla_session is None:
        _scylla_cluster = Cluster(SCYLLA_HOSTS, connect_timeout=10)
        _scylla_session = _scylla_cluster.connect()
        _scylla_session.set_keyspace("smart_monitoring")
    return _scylla_session


def get_active_rule() -> dict[str, Any]:
    doc = mongo_db().rules.find_one(sort=[("_id", -1)])
    if not doc:
        raise HTTPException(500, "У MongoDB немає документа правил (запустіть seed_data.py)")
    doc.pop("_id", None)
    return doc


def float_from_hash(h: dict[str, str], key: str) -> float:
    try:
        return float(h.get(key, "0"))
    except (TypeError, ValueError):
        return 0.0


def eval_threshold(metric: str, op: str, threshold: float, h: dict[str, str]) -> bool:
    v = float_from_hash(h, metric)
    if op == ">":
        return v > threshold
    if op == "<":
        return v < threshold
    if op == ">=":
        return v >= threshold
    if op == "<=":
        return v <= threshold
    if op == "==":
        return abs(v - threshold) < 1e-9
    return False


class SensorIn(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit: str = ""
    specs: dict[str, Any] = {}


class RuleThreshold(BaseModel):
    threshold: float


@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))


@app.get("/api/mongo/config")
def mongo_config():
    db = mongo_db()
    sensors = list(db.sensors.find({}, {"_id": 0}))
    rule = db.rules.find_one(sort=[("_id", -1)])
    if rule:
        rule.pop("_id", None)
    return {"sensors": sensors, "rule": rule}


@app.post("/api/mongo/sensors")
def mongo_add_sensor(body: SensorIn):
    db = mongo_db()
    if db.sensors.find_one({"code": body.code}):
        raise HTTPException(400, f"Сенсор з кодом {body.code} вже є")
    doc = {
        "code": body.code,
        "name": body.name,
        "unit": body.unit,
        "ieee_address": "0xPOC" + body.code.upper()[:8].ljust(8, "0"),
        "vendor": "POC",
        "model": "LAB",
        "specs": body.specs or {"note": "custom"},
    }
    db.sensors.insert_one(doc)
    rds().hset(REDIS_HASH, body.code, "0.0")
    return {"ok": True, "sensor": {k: v for k, v in doc.items() if k != "_id"}}


@app.delete("/api/mongo/sensors/{code}")
def mongo_delete_sensor(code: str):
    res = mongo_db().sensors.delete_one({"code": code})
    if res.deleted_count == 0:
        raise HTTPException(404, "Не знайдено")
    rds().hdel(REDIS_HASH, code)
    return {"ok": True}


@app.put("/api/mongo/rules")
def mongo_update_rule(body: RuleThreshold):
    db = mongo_db()
    rule = db.rules.find_one(sort=[("_id", -1)])
    if not rule:
        raise HTTPException(500, "Немає правила в MongoDB")
    db.rules.update_one({"_id": rule["_id"]}, {"$set": {"threshold": body.threshold}})

    r = rds()
    h = r.hgetall(REDIS_HASH)
    rdoc = get_active_rule()
    metric = rdoc.get("metric", "temp")
    op = rdoc.get("operator", ">")
    thr = float(body.threshold)
    active = rdoc.get("active_state", "TRIP")
    normal = rdoc.get("normal_state", "NORMAL")
    new_status = active if eval_threshold(metric, op, thr, h) else normal
    r.hset(REDIS_HASH, "actuator_status", new_status)
    return {"ok": True, "threshold": thr, "actuator_status": new_status}


@app.get("/api/redis/state")
def redis_state():
    return rds().hgetall(REDIS_HASH)


@app.post("/api/redis/simulate-tick")
def simulate_tick():
    """Штучний новий вимір: оновлює Redis і пише рядок у ScyllaDB."""
    rule = get_active_rule()
    object_id = rule.get("object_id", "variant_01_smart_flat")
    metric = rule.get("metric", "temp")
    op = rule.get("operator", ">")
    thr = float(rule.get("threshold", 26.0))
    active = rule.get("active_state", "COOLING")
    normal = rule.get("normal_state", "NORMAL")

    r = rds()
    h = r.hgetall(REDIS_HASH)
    codes = [c["code"] for c in mongo_db().sensors.find({}, {"code": 1})]
    rng = random.Random()

    vals: dict[str, float] = {}
    for i, c in enumerate(codes[:3]):
        cur = float_from_hash(h, c)
        delta = rng.uniform(-1.2, 1.2)
        vals[c] = round(max(-50.0, cur + delta), 2)

    if len(codes) >= 3 and rng.random() < 0.12:
        vals[metric] = round(thr + rng.uniform(0.5, 2.0), 2)

    ts = datetime.now(timezone.utc).replace(microsecond=0)
    val_list = [vals.get(codes[i], 0.0) for i in range(3)] if len(codes) >= 3 else [0.0, 0.0, 0.0]

    trip = eval_threshold(metric, op, thr, {**h, **{k: str(v) for k, v in vals.items()}})
    status = active if trip else normal

    pipe = r.pipeline()
    for k, v in vals.items():
        pipe.hset(REDIS_HASH, k, str(v))
    pipe.hset(REDIS_HASH, "actuator_status", status)
    pipe.hset(REDIS_HASH, "linkquality", str(rng.randint(110, 250)))
    pipe.hset(REDIS_HASH, "battery_mv", str(rng.randint(2850, 3100)))
    pipe.execute()

    sess = scylla()
    sess.execute(
        """
        INSERT INTO sensor_history (object_id, ts, val1, val2, val3, alert_triggered)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (object_id, ts, val_list[0], val_list[1], val_list[2], 1 if trip else 0),
    )

    return {
        "ts": ts.isoformat(),
        "values": vals,
        "actuator_status": status,
        "alert_triggered": int(trip),
    }


@app.get("/api/analytics")
def analytics():
    r = rds()
    raw = r.get(CACHE_KEY)
    if raw:
        data = json.loads(raw)
        ttl = r.ttl(CACHE_KEY)
        return {"source": "REDIS_CACHE_HIT", "ttl": ttl, "data": data}

    rule = get_active_rule()
    object_id = rule.get("object_id", "variant_01_smart_flat")
    since = datetime.now(timezone.utc) - timedelta(hours=12)

    sess = scylla()
    rows = sess.execute(
        SimpleStatement(
            """
            SELECT ts, val1, val2, val3, alert_triggered
            FROM sensor_history
            WHERE object_id = %s AND ts >= %s
            """,
            fetch_size=5000,
        ),
        (object_id, since),
    )

    buckets: dict[int, dict[str, Any]] = {}
    for row in rows:
        if row.ts is None:
            continue
        ts = row.ts if row.ts.tzinfo else row.ts.replace(tzinfo=timezone.utc)
        hour_key = int(ts.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0).timestamp() // 3600)
        b = buckets.setdefault(hour_key, {"vals": [], "alerts": 0})
        if row.val1 is not None:
            b["vals"].append(float(row.val1))
        b["alerts"] += int(row.alert_triggered or 0)

    out_hours = sorted(buckets.keys())
    chart1 = []
    chart2 = []
    for hk in out_hours:
        vs = buckets[hk]["vals"]
        if not vs:
            continue
        hour_dt = datetime.fromtimestamp(hk * 3600, tz=timezone.utc)
        label = hour_dt.strftime("%H:00")
        chart1.append(
            {
                "hour": label,
                "min_val": min(vs),
                "avg_val": sum(vs) / len(vs),
                "max_val": max(vs),
            }
        )
        chart2.append({"hour": label, "alerts_count": buckets[hk]["alerts"]})

    payload = {"chart1": chart1, "chart2": chart2}
    r.setex(CACHE_KEY, 60, json.dumps(payload))
    return {"source": "SCYLLADB_AGGREGATED_MISS", "ttl": 60, "data": payload}


@app.post("/api/cache/clear")
def cache_clear():
    rds().delete(CACHE_KEY)
    return {"ok": True}


@app.on_event("shutdown")
def shutdown():
    global _mongo, _redis, _scylla_session, _scylla_cluster
    if _mongo:
        _mongo.close()
    if _scylla_cluster:
        _scylla_cluster.shutdown()
