from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    predictions = relationship("Prediction", back_populates="user")
    api_metrics = relationship("ApiMetrics", back_populates="user")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    request_id = Column(String(100), unique=True, nullable=False)
    prediction_type = Column(String(20), nullable=False)
    input_features = Column(JSONB, nullable=False)
    prediction_result = Column(JSONB, nullable=False)
    model_version = Column(String(50), nullable=False)
    confidence_score = Column(Float)
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="predictions")
    model_metadata = relationship("ModelMetadata", back_populates="predictions")


# ------------------------------------------------------------
#  ModelMetadata – minimal version‐tracking table for models
# ------------------------------------------------------------
class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_version = Column(String(50), unique=True, index=True, nullable=False)
    model_path    = Column(String(500), nullable=False)               # e.g. "models/model.ubj"
    is_active     = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Reverse relation for convenience (one-to-many)
    predictions = relationship("Prediction", back_populates="model_metadata")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ModelMetadata(version='{self.model_version}', active={self.is_active})>"


# ------------------------------------------------------------
#  ApiMetrics – coarse performance log of each API request
# ------------------------------------------------------------
class ApiMetrics(Base):
    __tablename__ = "api_metrics"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endpoint        = Column(String(100), nullable=False, index=True)
    method          = Column(String(10),  nullable=False)             # GET / POST …
    status_code     = Column(Integer,    nullable=False)
    response_time_ms= Column(Integer,    nullable=False)              # total latency

    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"),          index=True)
    model_version  = Column(String(50),    ForeignKey("model_metadata.model_version"))

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Simple back-refs
    user           = relationship("User", back_populates="api_metrics")
    model_metadata = relationship("ModelMetadata")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ApiMetrics({self.endpoint} {self.status_code} {self.response_time_ms}ms)>"
