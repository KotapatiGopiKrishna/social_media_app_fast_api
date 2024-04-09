"""Create a Post table

Revision ID: 9a52951ac5db
Revises: 
Create Date: 2024-04-03 16:15:35.279479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a52951ac5db'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable = False, primary_key= True),
                    sa.Column('title', sa.String(), nullable= False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
