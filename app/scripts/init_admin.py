import os
import uuid

from sqlmodel import Session, select

from app.api.employee.models import Employee
from app.auth.auth import pwd_context
from app.db_config import get_database_engine, DatabaseConfig
from logger_config import logger


def init_admin() -> None:
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        logger.info("Skipping admin creation: ADMIN_EMAIL or ADMIN_PASSWORD not set")
        return
    database_config = DatabaseConfig()
    engine = get_database_engine(database_config)
    with Session(engine) as session:
        existing = session.exec(select(Employee).where(Employee.email == admin_email)).first()
        if existing:
            logger.info("Admin user already exists.")
            return

        admin = Employee(
            employee_id=uuid.uuid4(),
            name="System Admin",
            email=admin_email,
            phone_number="+1234567890",
            address="System Address",
            is_admin=True,
            hashed_password=pwd_context.hash(admin_password),
        )
        session.add(admin)
        session.commit()
        logger.info("Admin user created successfully.")


if __name__ == "__main__":
    init_admin()
