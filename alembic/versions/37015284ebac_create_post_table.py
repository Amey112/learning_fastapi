"""Create post table

Revision ID: 37015284ebac
Revises: 
Create Date: 2021-12-27 22:35:33.560196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37015284ebac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
