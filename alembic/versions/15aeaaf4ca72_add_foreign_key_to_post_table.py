"""add foreign key to post table

Revision ID: 15aeaaf4ca72
Revises: 876bf6d75eea
Create Date: 2024-04-03 17:13:35.950546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15aeaaf4ca72'
down_revision: Union[str, None] = '876bf6d75eea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey','posts')
    op.drop_column('posts', 'owner_id')
    pass
