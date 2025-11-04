"""add nutrients jsonb column to food_items

Revision ID: 0001_add_nutrients
Revises:
Create Date: 2025-11-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_add_nutrients"
down_revision = "0000_initial"  # This revision depends on the initial migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        # Add JSONB column with default empty object
        op.add_column(
            "food_items",
            sa.Column(
                "nutrients",
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=True,
                server_default=sa.text("'{}'::jsonb"),
            ),
        )
        # Add GIN index for efficient querying of nutrient values
        op.execute("CREATE INDEX ix_food_items_nutrients ON food_items USING GIN (nutrients)")
    else:
        # Generic JSON column for other DBs (SQLite fallback)
        op.add_column("food_items", sa.Column("nutrients", sa.JSON(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        # Drop the GIN index first
        op.execute("DROP INDEX IF EXISTS ix_food_items_nutrients")
    # Then drop the nutrients column
    op.drop_column("food_items", "nutrients")
