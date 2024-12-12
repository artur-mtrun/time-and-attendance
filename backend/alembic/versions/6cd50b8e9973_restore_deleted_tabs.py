"""restore deleted tabs

Revision ID: 6cd50b8e9973
Revises: 97708ad25227
Create Date: 2024-12-12 11:09:00.094174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd50b8e9973'
down_revision: Union[str, None] = '97708ad25227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enroll_number', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('card_number', sa.String(length=50), nullable=True),
    sa.Column('privileges', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_enroll_number'), 'employees', ['enroll_number'], unique=True)
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_table('attendance_all',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enroll_number', sa.String(length=50), nullable=False),
    sa.Column('terminal_number', sa.Integer(), nullable=False),
    sa.Column('event_timestamp', sa.DateTime(), nullable=False),
    sa.Column('in_out_mode', sa.Integer(), nullable=True),
    sa.Column('verify_mode', sa.Integer(), nullable=True),
    sa.Column('work_code', sa.Integer(), nullable=True),
    sa.Column('is_sync', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['terminal_number'], ['terminals.number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_all_enroll_number'), 'attendance_all', ['enroll_number'], unique=False)
    op.create_index(op.f('ix_attendance_all_id'), 'attendance_all', ['id'], unique=False)
    op.create_table('attendance_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enroll_number', sa.String(), nullable=True),
    sa.Column('terminal_number', sa.Integer(), nullable=True),
    sa.Column('event_timestamp', sa.DateTime(), nullable=False),
    sa.Column('in_out_mode', sa.Integer(), nullable=False),
    sa.Column('verify_mode', sa.Integer(), nullable=False),
    sa.Column('work_code', sa.Integer(), nullable=False),
    sa.Column('is_sync', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['enroll_number'], ['employees.enroll_number'], ),
    sa.ForeignKeyConstraint(['terminal_number'], ['terminals.number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_logs_id'), 'attendance_logs', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_attendance_logs_id'), table_name='attendance_logs')
    op.drop_table('attendance_logs')
    op.drop_index(op.f('ix_attendance_all_id'), table_name='attendance_all')
    op.drop_index(op.f('ix_attendance_all_enroll_number'), table_name='attendance_all')
    op.drop_table('attendance_all')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_index(op.f('ix_employees_enroll_number'), table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###
