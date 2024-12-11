"""change_employee_id_to_enroll_number_in_attendance_all

Revision ID: 87f6fc1db2bf
Revises: 05bf0c508adc
Create Date: 2024-12-11 11:11:50.354227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f6fc1db2bf'
down_revision: Union[str, None] = '05bf0c508adc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance_all', sa.Column('enroll_number', sa.String(length=50), nullable=False))
    op.alter_column('attendance_all', 'terminal_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('attendance_all', 'in_out_mode',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('attendance_all', 'verify_mode',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('attendance_all', 'work_code',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_attendance_all_enroll_number'), 'attendance_all', ['enroll_number'], unique=False)
    op.drop_constraint('attendance_all_employee_id_fkey', 'attendance_all', type_='foreignkey')
    op.drop_column('attendance_all', 'employee_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance_all', sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('attendance_all_employee_id_fkey', 'attendance_all', 'employees', ['employee_id'], ['id'])
    op.drop_index(op.f('ix_attendance_all_enroll_number'), table_name='attendance_all')
    op.alter_column('attendance_all', 'work_code',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('attendance_all', 'verify_mode',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('attendance_all', 'in_out_mode',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('attendance_all', 'terminal_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('attendance_all', 'enroll_number')
    # ### end Alembic commands ###