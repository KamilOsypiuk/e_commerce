"""init

Revision ID: 192c04269296
Revises: 
Create Date: 2023-02-03 16:35:51.998846

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "192c04269296"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "data", sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("data", "title")
    # ### end Alembic commands ###
