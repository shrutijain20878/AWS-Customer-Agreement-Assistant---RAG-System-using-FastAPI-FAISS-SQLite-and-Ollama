from database import SessionLocal
from models import QueryLog

db = SessionLocal()

logs = db.query(QueryLog).all()

for log in logs:

    print("-" * 50)

    print("ID:", log.id)
    print("Question:", log.query)
    print("Answer Found:", log.answer_found)
    print("Latency:", log.latency_ms)

db.close()