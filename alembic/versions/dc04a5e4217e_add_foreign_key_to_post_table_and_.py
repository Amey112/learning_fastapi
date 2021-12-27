"""add foreign key to post table and create pusblished key

Revision ID: dc04a5e4217e
Revises: e9f0765b872d
Create Date: 2021-12-27 23:20:26.058772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc04a5e4217e'
down_revision = 'e9f0765b872d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),
                  server_default='TRUE', nullable=False)
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'))
    )
    op.add_column(
        'posts',
        sa.Column("owner_id", sa.Integer(),
                  nullable=False)
    )
    op.create_foreign_key('posts_users_fk', source_table="posts",
                          referent_table="users", local_cols=[
                              "owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_column(
        'posts',
        'published'
    )
    op.drop_column('posts', 'created_at')
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column('posts', "owner_id")
    pass
