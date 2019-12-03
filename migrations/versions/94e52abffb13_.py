"""empty message

Revision ID: 94e52abffb13
Revises: ea63b9e2e942
Create Date: 2019-12-03 14:28:49.164429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94e52abffb13'
down_revision = 'ea63b9e2e942'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('enddate', sa.DateTime(), nullable=True))
    op.add_column('projects', sa.Column('startdate', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'startdate')
    op.drop_column('projects', 'enddate')
    # ### end Alembic commands ###