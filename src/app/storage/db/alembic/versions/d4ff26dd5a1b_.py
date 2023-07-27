"""empty message

Revision ID: d4ff26dd5a1b
Revises:
Create Date: 2023-07-27 15:02:17.092185

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd4ff26dd5a1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'colors',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('hex_code', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('seo_keyword', sa.Text(), nullable=True),
        sa.Column('seo_product_id', sa.Text(), nullable=True),
        sa.Column('discern_product_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'sizes',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'product_colors',
        sa.Column(
            'id', sa.Integer(), nullable=False, comment='productId в терминологии ZARA'
        ),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('color_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rawDescription', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ['color_id'],
            ['colors.id'],
            name='product_colors_color_id_fkey',
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        sa.ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            name='product_colors_product_id_fkey',
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_product_colors_color_id'), 'product_colors', ['color_id'], unique=False
    )
    op.create_index(
        op.f('ix_product_colors_product_id'),
        'product_colors',
        ['product_id'],
        unique=False,
    )
    op.create_table(
        'product_colors_images',
        sa.Column('product_color_id', sa.Integer(), nullable=False),
        sa.Column('path', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ['product_color_id'],
            ['product_colors.id'],
            name='product_colors_images_product_id_fkey',
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        sa.UniqueConstraint(
            'product_color_id',
            'path',
            'name',
            name='product_colors_images_product_color_id_path_name_key',
        ),
    )
    op.create_index(
        op.f('ix_product_colors_images_product_color_id'),
        'product_colors_images',
        ['product_color_id'],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f('ix_product_colors_images_product_color_id'),
        table_name='product_colors_images',
    )
    op.drop_table('product_colors_images')
    op.drop_index(op.f('ix_product_colors_product_id'), table_name='product_colors')
    op.drop_index(op.f('ix_product_colors_color_id'), table_name='product_colors')
    op.drop_table('product_colors')
    op.drop_table('sizes')
    op.drop_table('products')
    op.drop_table('colors')
    # ### end Alembic commands ###
