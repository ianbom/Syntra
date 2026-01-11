from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime

from app.database import Base
from app.enums import DocType, Sentiment


# -----------------------------------------------------
# USERS table (required for uploader relation)
# -----------------------------------------------------
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Kolom lain sesuai kebutuhan kamu


# -----------------------------------------------------
# DOCUMENTS
# -----------------------------------------------------
class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=True)
    creator = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    publisher = Column(String, nullable=True)
    contributor = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)

    type = Column(Enum(DocType), nullable=False)
    format = Column(String, nullable=True)
    identifier = Column(String, nullable=True)
    source = Column(String, nullable=True)
    language = Column(String(50), nullable=True)

    relation = Column(Text, nullable=True)
    coverage = Column(String, nullable=True)
    rights = Column(String, nullable=True)

    doi = Column(String(150), nullable=True)
    abstract = Column(Text, nullable=True)
    citation_count = Column(Integer, nullable=True)
    sentiment = Column(Enum(Sentiment), default=Sentiment.NEUTRAL)

    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_path = Column(String, nullable=True)
    url = Column(String, nullable=True)

    is_private = Column(Boolean, default=False)
    is_metadata_complete = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    uploader = relationship("Users")

    # One-to-many
    document_chunks = relationship("DocumentChunks", back_populates="document")

    # Many-to-many (via mapping tables)
    document_creators = relationship("DocumentCreators", back_populates="document")
    document_contributors = relationship("DocumentContributors", back_populates="document")
    document_subjects = relationship("DocumentSubjects", back_populates="document")
    document_relations = relationship("DocumentRelations", back_populates="document")

    # Back relation ("related_docs")
    document_relations_related = relationship(
        "DocumentRelations",
        back_populates="related_document",
        foreign_keys="DocumentRelations.related_document_id"
    )


# -----------------------------------------------------
# DOCUMENT CHUNKS
# -----------------------------------------------------
class DocumentChunks(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)

    # vector(768)
    embedding = Column(Vector(768), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document = relationship("Documents", back_populates="document_chunks")



class DocumentCreators(Base):
    __tablename__ = "document_creators"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    name = Column(String)

    document = relationship("Documents", back_populates="document_creators")


class DocumentContributors(Base):
    __tablename__ = "document_contributors"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    name = Column(String)

    document = relationship("Documents", back_populates="document_contributors")


class DocumentKeywords(Base):
    __tablename__ = "document_keywords"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    keyword = Column(String)

    document = relationship("Documents", back_populates="document_keywords")


class DocumentSubjects(Base):
    __tablename__ = "document_subjects"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    subject = Column(String)

    document = relationship("Documents", back_populates="document_subjects")


class DocumentRelations(Base):
    __tablename__ = "document_relations"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    related_document_id = Column(Integer, ForeignKey("documents.id"))
    relation_type = Column(String)

    document = relationship("Documents", foreign_keys=[document_id], back_populates="document_relations")
    related_document = relationship("Documents", foreign_keys=[related_document_id], back_populates="document_relations_related")
