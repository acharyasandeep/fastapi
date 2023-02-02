"""Add content column to post table

Revision ID: ebb80b9cade5
Revises: 933600eef208
Create Date: 2023-02-02 13:53:59.772429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebb80b9cade5'
down_revision = '933600eef208'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
