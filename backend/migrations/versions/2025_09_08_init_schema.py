"""init schema

Revision ID: 20250908_init
Revises: 
Create Date: 2025-09-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision = "20250908_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # organisations
    op.create_table(
        "organisations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )

    # users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.Enum("admin", "analyst", name="role"), nullable=False),
        sa.Column("organisation_id", sa.Integer(), sa.ForeignKey("organisations.id"), nullable=False),
    )

    # tenants
    op.create_table(
        "tenants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("organisation_id", sa.Integer(), sa.ForeignKey("organisations.id"), nullable=False),
    )

    # invoices
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("invoice_no", sa.String(), nullable=False, unique=True),
        sa.Column("amount_due", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("organisation_id", sa.Integer(), sa.ForeignKey("organisations.id"), nullable=False),
    )

    # bank_transactions
    op.create_table(
        "bank_transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value_date", sa.Date(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("batch_id", sa.String(), nullable=False, index=True),
        sa.Column("external_id", sa.String(), nullable=False, unique=True),
        sa.Column("organisation_id", sa.Integer(), sa.ForeignKey("organisations.id"), nullable=False),
    )

    # matches
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("bank_txn_id", sa.Integer(), sa.ForeignKey("bank_transactions.id"), nullable=False),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("matched_by", sa.String(), nullable=True),
        sa.Column("accepted", sa.Boolean(), default=None),
        sa.Column("reviewed_by", sa.String(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("organisation_id", sa.Integer(), sa.ForeignKey("organisations.id"), nullable=False),
    )


def downgrade():
    op.drop_table("matches")
    op.drop_table("bank_transactions")
    op.drop_table("invoices")
    op.drop_table("tenants")
    op.drop_table("users")
    op.drop_table("organisations")
    op.execute("DROP TYPE role")
