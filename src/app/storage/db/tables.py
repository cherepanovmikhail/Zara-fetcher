from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
    UniqueConstraint,
)


meta = MetaData()

sizes_table = Table(
    'sizes',
    meta,
    Column("id", Integer(), primary_key=True, autoincrement=False),
    Column("name", Text()),
)

colors_table = Table(
    'colors',
    meta,
    Column("id", Integer(), primary_key=True, autoincrement=False),
    Column("name", Text()),
    Column("hex_code", Text()),
)

products_table = Table(
    'products',
    meta,
    Column("id", Integer(), primary_key=True, autoincrement=False),
    Column("name", Text()),
    Column("seo_keyword", Text()),
    Column("seo_product_id", Text()),
    Column("discern_product_id", Integer()),
)


product_colors_table = Table(
    'product_colors',
    meta,
    Column("id", Integer(), primary_key=True, comment="productId в терминологии ZARA"),
    Column(
        "product_id",
        ForeignKey(
            products_table.c.id,
            onupdate="CASCADE",
            ondelete="RESTRICT",
            name="product_colors_product_id_fkey",
        ),
        nullable=False,
        index=True,
    ),
    Column(
        "color_id",
        ForeignKey(
            colors_table.c.id,
            onupdate="CASCADE",
            ondelete="RESTRICT",
            name="product_colors_color_id_fkey",
        ),
        nullable=False,
        index=True,
    ),
    Column("price", Integer()),
    Column("description", Text()),
    Column("rawDescription", Text()),
)

product_colors_images_table = Table(
    'product_colors_images',
    meta,
    Column(
        "product_color_id",
        ForeignKey(
            product_colors_table.c.id,
            onupdate="CASCADE",
            ondelete="RESTRICT",
            name="product_colors_images_product_id_fkey",
        ),
        nullable=False,
        index=True,
    ),
    Column("path", Text()),
    Column("name", Text()),
    Column("width", Integer()),
    Column("height", Integer()),
    Column("timestamp", Text()),
    UniqueConstraint(
        "product_color_id",
        "path",
        "name",
        name="product_colors_images_product_color_id_path_name_key",
    ),
)

product_colors_sizes_table = Table(
    'product_colors_sizes',
    meta,
    Column("sku", Integer(), primary_key=True, autoincrement=False),
    Column(
        "product_color_id",
        ForeignKey(
            product_colors_table.c.id,
            onupdate="CASCADE",
            ondelete="RESTRICT",
            name="product_colors_sizes_product_id_fkey",
        ),
        nullable=False,
        index=True,
    ),
    Column(
        "size_id",
        ForeignKey(
            sizes_table.c.id,
            onupdate="CASCADE",
            ondelete="RESTRICT",
            name="product_colors_sizes_size_id_fkey",
        ),
        nullable=False,
        index=True,
    ),
    Column("availability", Text()),
    Column("price", Integer()),
    Column("demand", Text()),
)
