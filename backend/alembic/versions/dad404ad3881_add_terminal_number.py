"""add_terminal_number

Revision ID: dad404ad3881
Revises: 8b47e87960b7
Create Date: 2024-12-06 11:14:42.659531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dad404ad3881'
down_revision: Union[str, None] = '8b47e87960b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Dodaj kolumnę bez constraint'ów
    op.add_column('terminals', sa.Column('number', sa.Integer(), nullable=True))
    
    # Dodaj tymczasowe numery dla istniejących rekordów
    op.execute("UPDATE terminals SET number = id WHERE number IS NULL")
    
    # Dodaj constraint'y
    op.alter_column('terminals', 'number',
               existing_type=sa.Integer(),
               nullable=False)
    op.create_unique_constraint('uq_terminals_number', 'terminals', ['number'])


def downgrade() -> None:
    op.drop_constraint('uq_terminals_number', 'terminals', type_='unique')
    op.drop_column('terminals', 'number')
