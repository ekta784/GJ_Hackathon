from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cameras = relationship("Camera", back_populates="department")

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    cameras = relationship("Camera", back_populates="vendor")

class Camera(Base):
    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String)
    latitude = Column(Float, default=23.0225)
    longitude = Column(Float, default=72.5714)
    status = Column(String, default="ONLINE")
    fps = Column(Integer, default=5)
    resolution = Column(String, default="1920x1080")
    geom_source = Column(String, default="simulated")
    codec = Column(String, default="H.264")
    district = Column(String, default="Ahmedabad")
    
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=True)
    
    department = relationship("Department", back_populates="cameras")
    vendor = relationship("Vendor", back_populates="cameras")
    sightings = relationship("Sighting", back_populates="camera")

class Watchlist(Base):
    __tablename__ = 'watchlist'
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, index=True)
    reason = Column(Text)
    severity = Column(String, default="CRITICAL")
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

class Sighting(Base):
    __tablename__ = 'sightings'
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, index=True)
    confidence_score = Column(Float)
    plate_det_conf = Column(Float, default=0.95)
    ocr_char_conf = Column(Float, default=0.92)
    format_validity = Column(Float, default=1.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    snapshot_sha256 = Column(String)
    
    camera_id = Column(Integer, ForeignKey('cameras.id'))
    camera = relationship("Camera", back_populates="sightings")

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    sighting_id = Column(Integer, ForeignKey('sightings.id'))
    watchlist_id = Column(Integer, ForeignKey('watchlist.id'), nullable=True)
    alert_type = Column(String, default="watchlist_hit")
    alert_level = Column(String, default="CONFIRMED")
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    sighting = relationship("Sighting")
    watchlist = relationship("Watchlist")

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
