from panda_patrol.backend.database.models import Base, engine

Base.metadata.create_all(bind=engine)
