from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from model import Base, User, Summary, Feedback

DB_NAME = 'sqlite:///database.db'
engine = create_engine(DB_NAME, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

def register_user(username, email, password):
    session = SessionLocal()
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    try:
        session.add(user)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def authenticate_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password, password):
        return user.id
    return None

def save_summary(user_id, original_text, summary):
    session = SessionLocal()
    summary_obj = Summary(user_id=user_id, original_text=original_text, summary=summary)
    session.add(summary_obj)
    session.commit()
    session.close()

def get_summaries(user_id):
    session = SessionLocal()
    summaries = session.query(Summary).filter_by(user_id=user_id).order_by(Summary.created_at.desc()).all()
    result = [(s.id, s.original_text, s.summary, s.created_at) for s in summaries]
    session.close()
    return result

def save_feedback(user_id, feedback):
    session = SessionLocal()
    feedback_obj = Feedback(user_id=user_id, feedback=feedback)
    session.add(feedback_obj)
    session.commit()
    session.close()

def get_db_connection():
    """Return a new SQLAlchemy session."""
    return SessionLocal()
