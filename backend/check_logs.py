from database import SessionLocal
from models import QueryLog

db = SessionLocal()

logs = db.query(QueryLog).all()

for log in logs:

    print(
        log.id,
        log.query,
        log.answer_found,
        log.latency_ms
    )

db.close()