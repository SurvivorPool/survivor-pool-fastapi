"""Adding odds, part 1

Revision ID: 108ec4ac2d2c
Revises: 8f6840123d3c
Create Date: 2022-08-14 16:06:41.575867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '108ec4ac2d2c'
down_revision = '8f6840123d3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('odds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('details', sa.String(), nullable=True),
    sa.Column('over_under', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('game', sa.Column('odds_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'game', 'odds', ['odds_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'game', type_='foreignkey')
    op.drop_column('game', 'odds_id')
    op.drop_table('odds')
    # ### end Alembic commands ###