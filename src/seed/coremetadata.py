from datetime import datetime
import os
from uuid import uuid4

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

url = 'postgresql://%s:%s@%s:%s/%s' % (
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'),
        os.getenv('POSTGRES_HOST'),
        os.getenv('POSTGRES_PORT'),
        os.getenv('POSTGRES_DB'),
    )

engine = create_engine(url)

metadata = MetaData(bind=engine)


customer = Table(
    'customer', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('first_name', String(50), nullable=False),
    Column('middle_name', String(50)),
    Column('last_name', String(50), nullable=False),
    Column('age', Integer, CheckConstraint(
        'age>0'), CheckConstraint('age<100')),
    Column('married', Boolean, default=False),
    Column('height', Float),
    Column('weight', Float),
    Column('last_updated', DateTime,
           default=datetime.now, onupdate=datetime.now),
    Column('created_at', DateTime, default=datetime.now)
)


address = Table(
    'address', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('customer_id', UUID(as_uuid=True), ForeignKey(
        "customer.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
    Column('street', String(50)),
    Column('city', String(50)),
    Column('country', String(50)),
    Column('last_updated', DateTime,
           default=datetime.now, onupdate=datetime.now),
    Column('created_at', DateTime, default=datetime.now)

)


audit = Table(
    'audit', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('table', String(50)),
    Column('item_id', UUID(as_uuid=True)),
    Column('operation', Enum("INSERT", "UPDATE",
                             "DELETE", name="operation_enum")),
    Column('time', Time)
)
