"""init

Revision ID: f3886ec8e174
Revises: 
Create Date: 2023-10-22 10:11:03.288824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f3886ec8e174"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "role",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_role_id"), "role", ["id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "login_record",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_login_record_id"), "login_record", ["id"], unique=False)
    op.create_table(
        "user_role",
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("role_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_role")
    op.drop_index(op.f("ix_login_record_id"), table_name="login_record")
    op.drop_table("login_record")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_role_id"), table_name="role")
    op.drop_table("role")
    # ### end Alembic commands ###