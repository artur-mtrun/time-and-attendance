"""Add attendance_all table

Revision ID: e4bb0bf2b3e3
Revises: acdfe8be49ef
Create Date: 2024-12-11 07:21:28.892016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4bb0bf2b3e3'
down_revision: Union[str, None] = 'acdfe8be49ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###