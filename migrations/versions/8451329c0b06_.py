"""empty message

Revision ID: 8451329c0b06
Revises: ce2a3a74b829
Create Date: 2019-11-29 18:08:19.733747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8451329c0b06'
down_revision = 'ce2a3a74b829'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
