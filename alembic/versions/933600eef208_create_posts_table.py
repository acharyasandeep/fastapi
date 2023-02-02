"""create posts table

Revision ID: 933600eef208
Revises: 
Create Date: 2023-02-02 13:44:52.517435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '933600eef208'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_table("posts")
    
