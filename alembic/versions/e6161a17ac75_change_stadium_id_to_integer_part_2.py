"""Change stadium id to integer part 2

Revision ID: e6161a17ac75
Revises: 31dc477a9299
Create Date: 2022-08-13 16:01:21.174605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6161a17ac75'
down_revision = '31dc477a9299'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stadium', sa.Column('id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'stadium', ['id'])
    op.drop_column('stadium', 'espn_id')
    op.add_column('game', sa.Column('stadium_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'game', 'stadium', ['stadium_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stadium', sa.Column('espn_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'stadium', type_='unique')
    op.drop_column('stadium', 'id')
    op.drop_constraint(None, 'game', type_='foreignkey')
    op.drop_column('game', 'stadium_id')
    # ### end Alembic commands ###
