"""add content column to posts table

Revision ID: 5f0e283ae3ee
Revises: 37015284ebac
Create Date: 2021-12-27 22:46:26.878641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0e283ae3ee'
down_revision = '37015284ebac'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
