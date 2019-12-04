"""empty message

Revision ID: 4982163548c9
Revises: 94e52abffb13
Create Date: 2019-12-04 09:53:45.746181

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4982163548c9'
down_revision = '94e52abffb13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), server_default='', nullable=True),
    sa.Column('startdate', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('enddate', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('projects', 'enddate',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'enddate',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_table('tasks')
    # ### end Alembic commands ###
