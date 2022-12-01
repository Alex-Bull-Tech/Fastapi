"""add foreign-key to posts table

Revision ID: 47155ea80fc1
Revises: 40a3586843c7
Create Date: 2022-11-29 10:23:31.449919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47155ea80fc1'
down_revision = '40a3586843c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
    local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
