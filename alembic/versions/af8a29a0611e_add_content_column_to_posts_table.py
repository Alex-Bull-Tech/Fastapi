"""add content column to posts table

Revision ID: af8a29a0611e
Revises: c21278783289
Create Date: 2022-11-29 10:00:33.263471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af8a29a0611e'
down_revision = 'c21278783289'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content",sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
