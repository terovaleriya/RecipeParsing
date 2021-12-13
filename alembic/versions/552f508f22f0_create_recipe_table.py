"""create recipe table

Revision ID: 552f508f22f0
Revises: 
Create Date: 2021-04-07 00:25:50.019385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, String, ForeignKey, UniqueConstraint

# revision identifiers, used by Alembic.
from sqlalchemy.orm import backref, relationship

revision = '552f508f22f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recipes', sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('title', String, nullable=False, unique=True))

    op.create_table('ingredients',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('raw_string', String, nullable=False, unique=True),
                    sa.Column('name', String), sa.Column('quantity', String),
                    sa.Column('comment', String))

    op.create_table('instructions',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('instruction', String, nullable=False, unique=True))

    op.create_table('products',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('name', String, nullable=False),
                    sa.Column('size', String),
                    sa.Column('price', String),
                    sa.Column('image_url', String),
                    UniqueConstraint('name', 'size', 'price', 'image_url'))

    op.create_table('tags',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('tag', String, nullable=False, unique=True))

    op.create_table('images',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('image', String, unique=True))

    op.create_table('planning',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('prep_time', String),
                    sa.Column('cook_time', String),
                    sa.Column('total_time', String),
                    sa.Column('serves', String), UniqueConstraint('prep_time', 'cook_time', 'total_time', 'serves'))

    op.create_table('nutrition',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('energy', String, nullable=True),
                    sa.Column('fat', String, nullable=True),
                    sa.Column('saturated_fat', String, nullable=True),
                    sa.Column('carbohydrate', String, nullable=True),
                    sa.Column('sugars', String, nullable=True),
                    sa.Column('protein', String, nullable=True),
                    sa.Column('salt', String, nullable=True),
                    sa.Column('fibre', String, nullable=True),
                    UniqueConstraint('energy', 'fat', 'saturated_fat', 'carbohydrate', 'sugars', 'protein', 'salt',
                                     'fibre'))

    op.create_table('recipes_instructions',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('instruction', INTEGER,
                              ForeignKey('instructions.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'instruction'))

    op.create_table('recipes_tags',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('tag', INTEGER, ForeignKey('tags.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'tag'))

    op.create_table('recipes_images',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('image', INTEGER, ForeignKey('images.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'image'))

    op.create_table('recipes_planning',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('planning', INTEGER, ForeignKey('planning.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'planning'))

    op.create_table('recipes_ingredients',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('ingredient', INTEGER, ForeignKey('ingredients.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'ingredient'))

    op.create_table('recipes_nutrition',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('nutrition', INTEGER, ForeignKey('nutrition.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('recipe', 'nutrition'))

    op.create_table('unchecked_ingredients_products',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('product', INTEGER, ForeignKey('products.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('ingredient', INTEGER, ForeignKey('ingredients.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('product', 'ingredient'))

    op.create_table('matched_ingredients_products',
                    sa.Column('id', INTEGER, primary_key=True),
                    sa.Column('product', INTEGER, ForeignKey('products.id', ondelete="CASCADE"), nullable=False),
                    sa.Column('ingredient', INTEGER, ForeignKey('ingredients.id', ondelete="CASCADE"), nullable=False),
                    UniqueConstraint('product', 'ingredient'))

    op.create_table('product_string_ids_matching',
                    sa.Column('id', INTEGER, ForeignKey("products.id"), nullable=False, primary_key=True),
                    sa.Column('string_id', String, nullable=False),
                    UniqueConstraint('id', 'string_id'))


def downgrade():
    op.drop_table('recipe')
