"""First commit

Revision ID: ad466974c3b0
Revises: db7920e8e911
Create Date: 2022-08-03 19:03:12.076574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad466974c3b0'
down_revision = 'db7920e8e911'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addressbook',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('personal_info', sa.JSON(), nullable=True),
    sa.Column('created_on', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addressbook')
    # ### end Alembic commands ###
