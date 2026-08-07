from uuid import uuid7

import sqlalchemy as sa
from taskly.domain.entities.user import User
from taskly.infrastructure.postgresql.registry import mapper_registry

metadata = mapper_registry.metadata

user_table = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.UUID(as_uuid=True), default=uuid7, primary_key=True),
    sa.Column("first_name", sa.String(255), nullable=False),
    sa.Column("last_name", sa.String(255), nullable=False),
    sa.Column("patronymic", sa.String(255), nullable=True),
    sa.Column("username", sa.String(250), nullable=True, unique=True, index=True),
    sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
)

mapper_registry.map_imperatively(
    User,
    user_table
)
