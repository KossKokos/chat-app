from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
    UniqueConstraint,
    func,
    CheckConstraint,
    Numeric,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = "tbl_users" 

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    confirmed = Column(Boolean, default=False)  # email confirmed
    refresh_token = Column(String(255), nullable=True)
    contacts = relationship(
        "User",
        secondary="tbl_contacts",
        primaryjoin="User.user_id == tbl_contacts.c.user_id",
        secondaryjoin="User.user_id == tbl_contacts.c.contact_id",
        backref="contacted_by",
    ) # this creates a list of contacts for specific user

    blacklisted_token = relationship(
        "BlacklistedToken", uselist=False, back_populates="user"
    )

    # refresh_token = Column(String(255), nullable=True)
    # banned = Column(Boolean, default=False)
    # role = Column(String(20), nullable=False, default="user")
    # license_plate = Column(
    #     "license_plate", ForeignKey("cars_table.license_plate"), unique=True
    # )
    # tariff_id = Column("tariff_id", ForeignKey("tariffs_table.id"))
    # blacklisted_token = relationship(
    #     "BlacklistedToken", uselist=False, back_populates="user"
    # )
    # cars = relationship("Car", uselist=True, back_populates="user")
    # tariff = relationship("Tariff", back_populates="user")

    # __table_args__ = (
    #     CheckConstraint(role.in_(["admin", "user"]), name="check_valid_role"),
    # )


class Contacts(Base):
    __tablename__ = "tbl_contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False) # user who requested contact
    contact_id = Column(Integer, ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False) # user who have to accept
    is_confirmed = Column(Boolean, default=False, nullable=False)  # Mutual confirmation flag

    # Ensures no duplicate contacts & prevents self-contact
    __table_args__ = (UniqueConstraint("user_id", "contact_id"),)


class Profile(Base):
    __tablename__ = "tbl_profiles"

    profile_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False) 
    phone_number = Column(String(20), nullable=True)
    biography = Column(Text, nullable=True)
    img_url = Column(Text, nullable=True)


class Posts(Base):
    __tablename__ = "tbl_posts"

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False) 
    description = Column(Text, nullable=True)
    img_url = Column(Text, nullable=False)
    posted_at = Column("posted_at", DateTime, default=func.now())


class Chat(Base):
    __tablename__ = "tbl_chats"

    chat_id = Column(Integer, primary_key=True)
    user_1_id = Column("user_1_id", ForeignKey("tbl_users.user_id"), nullable=False)
    user_2_id = Column("user_2_id", ForeignKey("tbl_users.user_id"), nullable=False)
    chat_started = Column("chat_started", DateTime, default=func.now())


class Message(Base):
    __tablename__ = "tbl_messages"

    message_id = Column(Integer, primary_key=True)
    chat_id = Column("chat_id", ForeignKey("tbl_chats.chat_id"))
    sender_id = Column("sender_id", ForeignKey("tbl_users.user_id"))
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    sent_at = Column("sent_at", DateTime, default=func.now())


class BanList(Base):
    __tablename__ = "tbl_banlist"

    ban_id = Column(Integer, primary_key=True)
    user_id = Column("user_id", ForeignKey("tbl_users.user_id"))
    banned_at = Column("banned_at", DateTime, default=func.now())


class BlacklistedToken(Base):
    __tablename__ = "tbl_blacklisted_tokens"

    id = Column(Integer, primary_key=True)
    blacklisted_token = Column(String(255), nullable=True)
    user_id = Column(
        "user_id", ForeignKey("tbl_users.user_id", ondelete="CASCADE"), unique=True
    )
    user = relationship("User", back_populates="blacklisted_token")