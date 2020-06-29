"""empty message

Revision ID: 373003768c93
Revises: 3e88df923a8a
Create Date: 2020-01-20 17:46:52.200249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373003768c93'
down_revision = '3e88df923a8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('status', sa.String(), server_default='Open', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'status')
    # ### end Alembic commands ###