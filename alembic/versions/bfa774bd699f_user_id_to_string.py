"""user id to string

Revision ID: bfa774bd699f
Revises: 617ab5d31dbb
Create Date: 2022-08-22 22:54:54.490522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfa774bd699f'
down_revision = '617ab5d31dbb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adminmessage', sa.Column('user_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'adminmessage', 'user', ['user_id'], ['id'])
    op.add_column('playerteam', sa.Column('user_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'playerteam', 'user', ['user_id'], ['id'])
    op.add_column('usermessage', sa.Column('user_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'usermessage', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usermessage', type_='foreignkey')
    op.drop_column('usermessage', 'user_id')
    op.drop_constraint(None, 'playerteam', type_='foreignkey')
    op.drop_column('playerteam', 'user_id')
    op.drop_constraint(None, 'adminmessage', type_='foreignkey')
    op.drop_column('adminmessage', 'user_id')
    # ### end Alembic commands ###
