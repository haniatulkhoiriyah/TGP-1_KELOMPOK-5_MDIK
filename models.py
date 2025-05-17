from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Airnb(Base):
    __tablename__ = 'listings_albany'
    
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(255), nullable=True)
    host_id = Column("host_id", Integer, nullable=True)
    host_name = Column("host_name", String(100), nullable=True)
    neighbourhood_group = Column("neighbourhood_group", String(100), nullable=True)
    neighbourhood = Column("neighbourhood", String(100), nullable=True)
    latitude = Column("latitude", Float, nullable=True)
    longitude = Column("longitude", Float, nullable=True)
    room_type = Column("room_type", String(50), nullable=True)
    price = Column("price", Integer, nullable=True)
    minimum_nights = Column("minimum_nights", Integer, nullable=True)
    number_of_reviews = Column("number_of_reviews", Integer, nullable=True)
    last_review = Column("last_review", Date, nullable=True)  # Pastikan Date diimpor dengan benar
    reviews_per_month = Column("reviews_per_month", DECIMAL(4, 2), nullable=True)
    calculated_host_listings_count = Column("calculated_host_listings_count", Integer, nullable=True)
    availability_365 = Column("availability_365", Integer, nullable=True)
    number_of_reviews_ltm = Column("number_of_reviews_ltm", Integer, nullable=True)
    license = Column("license", String(255), nullable=True)
