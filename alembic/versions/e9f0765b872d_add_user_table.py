"""add user table

Revision ID: e9f0765b872d
Revises: 5f0e283ae3ee
Create Date: 2021-12-27 22:59:00.750653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import PrimaryKeyConstraint, UniqueConstraint


# revision identifiers, used by Alembic.
revision = 'e9f0765b872d'
down_revision = '5f0e283ae3ee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table("users")
