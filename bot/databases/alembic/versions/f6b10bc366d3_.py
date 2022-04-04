"""

Revision ID: f6b10bc366d3
Revises: 
Create Date: 2022-04-04 18:42:07.428640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6b10bc366d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food',
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('food_id')
    )
    op.create_index(op.f('ix_food_food_id'), 'food', ['food_id'], unique=False)
    op.create_table('user',
    sa.Column('scud_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('scud_id')
    )
    op.create_index(op.f('ix_user_scud_id'), 'user', ['scud_id'], unique=False)
    op.create_index(op.f('ix_user_telegram_id'), 'user', ['telegram_id'], unique=False)
    op.create_table('order',
    sa.Column('scud_id', sa.BigInteger(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['food.food_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['scud_id'], ['user.scud_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_index(op.f('ix_order_order_id'), 'order', ['order_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_order_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_user_telegram_id'), table_name='user')
    op.drop_index(op.f('ix_user_scud_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_food_food_id'), table_name='food')
    op.drop_table('food')
    # ### end Alembic commands ###