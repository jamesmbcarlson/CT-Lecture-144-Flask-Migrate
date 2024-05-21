from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class CustomerAccount(Base):
    __tablename__ = "Customer_Accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))
    # One-to-One: CustomerAccount and Customer
    customer: Mapped['Customer'] = db.relationship(back_populates='customer_account')