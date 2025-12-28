from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

security = HTTPBearer()

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.credentials!= "Sx36EBvt2ZW330mXDy878QucWiPXu5SLpZXzBBBLbS3hFwUS1EeIgb768B6CjeHa":
        raise HTTPException(status_code=401, detail="Invalid credentials")

app = FastAPI(dependencies=[Depends(verify_auth)])

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["healthyfy-kitchen-db"]
diet_collection = db["diet-profile"]
recipes_collection = db["recipies"]
user_collection = db["user"]

class User(BaseModel):
    user_name: str
    user_email: str
    password: str

class Recipe(BaseModel):
    ingredients: list[str]
    instructions: list[str]
    serving_suggestions: str
    user: str

class DietProfile(BaseModel):
    weight: str
    height: str
    daily_activity: str
    goal:str


class SaveRecipes(BaseModel):
    user: str
    recipes:list[str]

#get calls
@app.get("/diet-profile")
async def get_diet_profile():
    diet_finder = diet_collection.find({})
    diets = []
    async for diet in diet_finder:
        diet["id"] = str(diet["_id"])
        del diet["_id"]
        diets.append(diet)
    return {"diet_profiles": diets}      
   
@app.get("/user")
async def get_user_details():
    user_finder = user_collection.find({})
    users = []
    async for user in user_finder:
        user["id"] = str(user["_id"])
        del user["_id"]
        users.append(user)
    return {"users": users}



@app.get("/recipes")
async def get_all_recipes():
    recipe_finder = recipes_collection.find({})
    recipes = []
    async for recipe in recipe_finder:
        recipe["id"] = str(recipe["_id"])
        del recipe["_id"]
        recipes.append(recipe)
    return {"recipes": recipes}

#post calls

@app.post("/user")
async def create_user(user: User):
    users= user.model_dump()
    result = await user_collection.insert_one(users)
    return {"user_id": str(result.inserted_id)}

@app.post("/recipe")
async def create_recipe(recipe: Recipe):
    recipe_data = recipe.model_dump()
    result = await recipes_collection.insert_one(recipe_data)
    return {"recipe_id": str(result.inserted_id)}

@app.post("/diet-profile")
async def create_diet_profile(diet_profile: DietProfile):
    diet_data = diet_profile.model_dump()
    result = await diet_collection.insert_one(diet_data)
    return {"diet_profile_id": str(result.inserted_id)}

@app.post("/save-recipes")
async def save_recipe(save_recipes: SaveRecipes):
    save_data = save_recipes.model_dump()
    result = await recipes_collection.insert_one(save_data)
    return {"saved_recipes_id": str(result.inserted_id)}