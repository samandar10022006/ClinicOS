from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.hospital import Hospital
from app.models.bed import Bed
from app.models.doctor import Doctor
from app.models.user import User
from app.core.security import get_password_hash


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Hospital).count() == 0:
            hospital = Hospital(name="DMed Shifoxona", address="Toshkent", is_active=True)
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        else:
            hospital = db.query(Hospital).first()

        if db.query(Bed).count() == 0:
            beds = [
                Bed(room_number="101", ward="A", category="urgent", hospital_id=hospital.id),
                Bed(room_number="102", ward="A", category="urgent", hospital_id=hospital.id),
                Bed(room_number="103", ward="A", category="urgent", hospital_id=hospital.id),
                Bed(room_number="201", ward="B", category="chronic", hospital_id=hospital.id),
                Bed(room_number="202", ward="B", category="chronic", hospital_id=hospital.id),
                Bed(room_number="203", ward="B", category="chronic", hospital_id=hospital.id),
                Bed(room_number="301", ward="C", category="fast", hospital_id=hospital.id),
                Bed(room_number="302", ward="C", category="fast", hospital_id=hospital.id),
                Bed(room_number="303", ward="C", category="fast", hospital_id=hospital.id),
            ]
            db.add_all(beds)

        if db.query(Doctor).count() == 0:
            doctors = [
                Doctor(full_name="Dr. Alimov A.", specialty="Kardiolog", hospital_id=hospital.id),
                Doctor(full_name="Dr. Karimov B.", specialty="Terapevt", hospital_id=hospital.id),
                Doctor(full_name="Dr. Rahimov C.", specialty="Nevrolog", hospital_id=hospital.id),
                Doctor(full_name="Dr. Sultanov D.", specialty="Ortoped", hospital_id=hospital.id),
            ]
            db.add_all(doctors)

        if db.query(User).count() == 0:
            admin = User(
                username="admin",
                email="admin@dmed.uz",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrator",
                role="admin",
                hospital_id=hospital.id,
            )
            db.add(admin)

        db.commit()
    finally:
        db.close()
