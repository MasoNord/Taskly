
import sqlalchemy as sa

from taskly.domain.entities.auth_session import AuthSession
from taskly.infrastructure.postgresql.registry import mapper_registry

metadata = mapper_registry.metadata

session_table = sa.Table(
    "sessions",
    metadata,
    sa.Column("id", sa.String, primary_key=True),
    sa.Column("user_id", sa.ForeignKey("users.id"), onupdate="CASCADE"),
    sa.Column("ip_address", sa.String(500), nullable=True),
    sa.Column("user_agent", sa.String(500), nullable=True),
    sa.Column("expiration", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
)

mapper_registry.map_imperatively(
    AuthSession,
    session_table
)
