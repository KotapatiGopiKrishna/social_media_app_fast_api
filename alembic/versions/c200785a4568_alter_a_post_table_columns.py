"""alter a Post table columns

Revision ID: c200785a4568
Revises: 9a52951ac5db
Create Date: 2024-04-03 16:39:34.163868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c200785a4568'
down_revision: Union[str, None] = '9a52951ac5db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
