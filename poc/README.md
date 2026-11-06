# POC лабораторної (базова перевірка)

Цей каталог **не змінює** `docs/index.html` — це окремий мінімальний стенд для перевірки, що завдання з методички реалізовне.

## Що всередині

- `docker-compose.yml` — MongoDB, Redis, ScyllaDB (порти як у описі).
- `seed_data.py` — створює колекції, таблицю `sensor_history`, 720 рядків за 12 год, початковий Redis hash.
- `main.py` — FastAPI з ендпоінтами у стилі промпту з методички (`/api/mongo/...`, `/api/redis/...`, `/api/analytics`).
- `static/index.html` — примітивна сторінка з кнопками виклику API.
- `Discution.md` — питання та неузгодженості в формулюваннях (для обговорення з викладачем).

## Запуск

```bash
cd poc
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d
# зачекати, поки Scylla підніметься (1–2 хв), потім:
python seed_data.py
uvicorn main:app --reload --port 8000
```

Відкрити в браузері: http://127.0.0.1:8000

## Примітки

- **Docker / RAM:** якщо Scylla в логах пише `insufficient physical memory` (типово при ліміті ~500 МБ на контейнер), у `docker-compose.yml` для POC зменшено `--memory` (наприклад 384M) і ліміт контейнера. На повноцінній машині можна повернути 1G, як у методичці.
- **Scylla 2026 + keyspace:** у `seed_data.py` keyspace створюється з `NetworkTopologyStrategy` і `tablets = {'enabled': false}` — інакше типовий для Cassandra `SimpleStrategy` на поточній Scylla дає помилку `SimpleStrategy doesn't support tablet replication`.
- ScyllaDB на слабкому ноуті стартує повільно; якщо `seed_data.py` падає по таймауту — повторити через хвилину.
- Повноцінні графіки Chart.js у цьому POC не обов’язкові — для швидкої валідації достатньо JSON з `/api/analytics`.
