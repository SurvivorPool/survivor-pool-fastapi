"""user id to string

Revision ID: a5e3b73c6486
Revises: e65a3e7facc6
Create Date: 2022-08-22 22:52:36.983013

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5e3b73c6486'
down_revision = 'e65a3e7facc6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('adminmessage_user_id_fkey', 'adminmessage', type_='foreignkey')
    op.drop_column('adminmessage', 'user_id')
    op.drop_constraint('playerteam_user_id_fkey', 'playerteam', type_='foreignkey')
    op.drop_column('playerteam', 'user_id')
    op.drop_column('user', 'provider')
    op.alter_column('usermessage', 'type_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_constraint('usermessage_user_id_fkey', 'usermessage', type_='foreignkey')
    op.drop_column('usermessage', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usermessage', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('usermessage_user_id_fkey', 'usermessage', 'user', ['user_id'], ['id'])
    op.alter_column('usermessage', 'type_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.add_column('user', sa.Column('provider', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('playerteam', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('playerteam_user_id_fkey', 'playerteam', 'user', ['user_id'], ['id'])
    op.add_column('adminmessage', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('adminmessage_user_id_fkey', 'adminmessage', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
