"""remove email fields

Revision ID: aa2d62345f5e
Revises: c1d7c8b48292
Create Date: 2021-08-24 23:30:42.605318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2d62345f5e'
down_revision = 'c1d7c8b48292'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(length=128), nullable=True))
    # ### end Alembic commands ###
