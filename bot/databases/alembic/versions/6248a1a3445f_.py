"""

Revision ID: 6248a1a3445f
Revises: f6b10bc366d3
Create Date: 2022-04-05 19:05:34.715074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6248a1a3445f'
down_revision = 'f6b10bc366d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'datetime')
    # ### end Alembic commands ###