"""update data model

Revision ID: cf4a85b10dff
Revises: 192c04269296
Create Date: 2023-02-03 16:37:10.393020

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cf4a85b10dff"
down_revision = "192c04269296"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("data", "title", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("data", "title", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
