"""Major project restructure

Revision ID: a512cc540642
Revises: 
Create Date: 2022-08-07 18:27:41.031836

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a512cc540642'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaguetype',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('messagetype',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nflteam',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=False),
    sa.Column('city_state', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('nickname', sa.String(), nullable=False),
    sa.Column('conference', sa.String(), nullable=False),
    sa.Column('division', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('stadium',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('roof_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.Column('receive_notifications', sa.Boolean(), nullable=True),
    sa.Column('wins', sa.Integer(), nullable=True),
    sa.Column('provider', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('adminmessage',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('show', sa.Boolean(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('home_team_name', sa.String(), nullable=False),
    sa.Column('home_team_score', sa.Integer(), nullable=True),
    sa.Column('away_team_name', sa.String(), nullable=False),
    sa.Column('away_team_score', sa.Integer(), nullable=True),
    sa.Column('day_of_week', sa.String(), nullable=True),
    sa.Column('game_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('quarter', sa.String(), nullable=True),
    sa.Column('quarter_time', sa.String(), nullable=True),
    sa.Column('week', sa.Integer(), nullable=True),
    sa.Column('stadium_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['away_team_name'], ['nflteam.nickname'], ),
    sa.ForeignKeyConstraint(['home_team_name'], ['nflteam.nickname'], ),
    sa.ForeignKeyConstraint(['stadium_id'], ['stadium.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('league',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('start_week', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('type_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['leaguetype.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usermessage',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('type_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('read', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('read_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['messagetype.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playerteam',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('league_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('streak', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['league_id'], ['league.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pick',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('player_team_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('game_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('week_num', sa.Integer(), nullable=False),
    sa.Column('nfl_team_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['nfl_team_name'], ['nflteam.nickname'], ),
    sa.ForeignKeyConstraint(['player_team_id'], ['playerteam.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pick')
    op.drop_table('playerteam')
    op.drop_table('usermessage')
    op.drop_table('league')
    op.drop_table('game')
    op.drop_table('adminmessage')
    op.drop_table('user')
    op.drop_table('stadium.py')
    op.drop_table('nflteam')
    op.drop_table('messagetype')
    op.drop_table('leaguetype')
    # ### end Alembic commands ###
