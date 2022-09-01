"""is admin default to false

Revision ID: 335d86e340e2
Revises: 82bb04423245
Create Date: 2022-08-22 23:31:17.949014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335d86e340e2'
down_revision = '82bb04423245'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('nflteam', 'conference',
               existing_type=sa.VARCHAR(),
               server_default='',
               existing_nullable=False)
    op.alter_column('nflteam', 'division',
               existing_type=sa.VARCHAR(),
               server_default='',
               existing_nullable=False)
    op.alter_column('user', 'is_admin',
               existing_type=sa.BOOLEAN(),
               server_default='False',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_admin',
               existing_type=sa.BOOLEAN(),
               server_default=None,
               existing_nullable=True)
    op.alter_column('nflteam', 'division',
               existing_type=sa.VARCHAR(),
               server_default=None,
               existing_nullable=False)
    op.alter_column('nflteam', 'conference',
               existing_type=sa.VARCHAR(),
               server_default=None,
               existing_nullable=False)
    # ### end Alembic commands ###