from typing import List

from gino import Gino
from sqlalchemy import String, ForeignKey, Column, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from core import schema

db: Gino = Gino()


class RecipesIngredients(db.Model):
    __tablename__ = 'recipes_ingredients'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    ingredient = Column(Integer, ForeignKey('ingredients.id', ondelete="CASCADE"), nullable=False)


class ProductStringIdsMatching(db.Model):
    __tablename__ = 'product_string_ids_matching'
    id = Column(Integer, ForeignKey("products.id"), primary_key=True, nullable=False)
    string_id = Column('string_id', String, nullable=False)


class RecipesTags(db.Model):
    __tablename__ = 'recipes_tags'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('tags.id', ondelete="CASCADE"), nullable=False)
    tag = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)


class RecipesInstructions(db.Model):
    __tablename__ = 'recipes_instructions'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('instructions.id', ondelete="CASCADE"), nullable=False)
    instruction = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)


class RecipesImages(db.Model):
    __tablename__ = 'recipes_images'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('images.id', ondelete="CASCADE"), nullable=False)
    image = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)


class RecipesPlanning(db.Model):
    __tablename__ = 'recipes_planning'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('planning.id', ondelete="CASCADE"), nullable=False)
    planning = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)


class RecipesNutrition(db.Model):
    __tablename__ = 'recipes_nutrition'
    id = Column(Integer, primary_key=True, nullable=False)
    recipe = Column(Integer, ForeignKey('nutrition.id', ondelete="CASCADE"), nullable=False)
    nutrition = Column(Integer, ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)


class MatchedIngredientsProducts(db.Model):
    __tablename__ = 'matched_ingredients_products'
    id = Column(Integer, primary_key=True, nullable=False)
    product = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    ingredient = Column(Integer, ForeignKey('products.id'), nullable=False)


class UncheckedIngredientsProducts(db.Model):
    __tablename__ = 'unchecked_ingredients_products'
    id = Column(Integer, primary_key=True, nullable=False)
    product = Column(Integer, ForeignKey('products.id'), nullable=False)
    ingredient = Column(Integer, ForeignKey('ingredients.id'), nullable=False)


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    ingredients = relationship("Ingredients", secondary="RecipesIngredients", backref="recipes")
    tags = relationship("Tags", secondary="RecipesTags", backref="recipes")
    images = relationship("Image", secondary="RecipesImages", backref="recipes")
    planning = relationship("Planning", secondary="RecipesPlanning", backref="recipes")
    nutrition = relationship("Nutrition", secondary="RecipesNutrition",
                             backref=backref("nutrition", cascade="all, delete"))
    instructions = relationship("Instruction", secondary="RecipesInstructions", backref="recipes")

    def as_schema(self) -> schema.Recipe:
        return schema.Recipe(recipe_id=self.id, title=self.title)


class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    raw_string = Column(String)
    name = Column(String)
    quantity = Column(String)
    comment = Column(String)

    def as_schema(self) -> schema.Ingredient:
        return schema.Ingredient(ingredient_id=self.id, raw_string=self.raw_string, name=self.name,
                                 quantity=self.quantity, comment=self.comment)


class Tags(db.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False, unique=True)

    def as_schema(self) -> schema.Tag:
        return schema.Tag(tag_id=self.id, tag=self.tag)


class Images(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(String, unique=True)

    def as_schema(self) -> schema.Image:
        return schema.Image(image_id=self.id, image=self.image)


class Plan(db.Model):
    __tablename__ = "planning"
    id = Column(Integer, primary_key=True)
    prep_time = Column(String)
    cook_time = Column(String)
    total_time = Column(String)
    serves = Column(String)
    UniqueConstraint('prep_time', 'cook_time', 'total_time', 'serves')

    def as_schema(self) -> schema.Plan:
        return schema.Plan(planning_id=self.id, prep_time=self.prep_time, cook_time=self.cook_time,
                           total_time=self.total_time, serves=self.serves)


class Nutrition(db.Model):
    __tablename__ = "nutrition"
    id = Column(Integer, primary_key=True)
    energy = Column(String, nullable=True)
    fat = Column(String, nullable=True)
    saturated_fat = Column(String, nullable=True)
    carbohydrate = Column(String, nullable=True)
    sugars = Column(String, nullable=True)
    protein = Column(String, nullable=True)
    salt = Column(String, nullable=True)
    fibre = Column(String, nullable=True)
    UniqueConstraint('energy', 'fat', 'saturated_fat', 'carbohydrate',
                     'sugars', 'protein', 'salt', 'fibre')

    def as_schema(self) -> schema.Nutrition:
        return schema.Nutrition(nutrition_id=self.id, energy=self.energy, fat=self.fat,
                                saturated_fat=self.saturated_fat, carbohydrate=self.carbohydrate, sugars=self.sugars,
                                protein=self.protein,
                                salt=self.salt, fibre=self.fibre)


class Products(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(String)
    price = Column(String)
    image_url = Column(String)
    UniqueConstraint('name', 'size', 'image_url')

    def as_schema(self) -> schema.Product:
        return schema.Product(product_id=self.id, name=self.name, size=self.size, price=self.price,
                              image_url=self.image_url)


class Instructions(db.Model):
    __tablename__ = 'instructions'
    id = Column(Integer, primary_key=True)
    instruction = Column(String, nullable=False, unique=True)

    def as_schema(self) -> schema.Instruction:
        return schema.Instruction(instruction_id=self.id, instruction=self.instruction)
