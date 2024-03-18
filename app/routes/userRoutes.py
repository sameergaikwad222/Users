from fastapi import APIRouter, Response, status
from app.database.database import collection
from app.models.usersModel import Users
from app.schema.schemas import multiple_serializer, single_serializer
import datetime
from bson import ObjectId
import bcrypt


router = APIRouter()


# Get All Users


@router.get("/users")
async def get_users(response: Response, limit: int = 10, skip: int = 0):
    try:
        users = multiple_serializer(
            collection.find().limit(limit=limit).skip(skip=skip)
        )
        response.status_code = status.HTTP_200_OK
        return {"status": "success", "data": users}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print("Error while getting getting users from database", e)
        return {"status": "Failed", "data": None}


# Insert multiple users
@router.post("/users")
async def create_users(users: list[Users], response: Response):
    if len(users) <= 0:
        return {"status": "Failed", "data": None}

    # Converting list of objects into list of dictionaries
    userDicts = []

    for user in users:
        userDict = dict(user)
        locationDict = dict(userDict["location"])
        contactDict = dict(userDict["contact"])
        userDict["location"] = locationDict
        userDict["contact"] = contactDict
        userDict["createdAt"] = datetime.datetime.now()
        userDict["updatedAt"] = datetime.datetime.now()
        userDict["statusId"] = 1
        salt = bcrypt.gensalt(rounds=5)
        bpass = userDict["password"].encode("utf-8")
        bhash = bcrypt.hashpw(password=bpass, salt=salt)
        userDict["password"] = bhash.decode("utf-8")
        userDicts.append(userDict)

    try:
        result = collection.insert_many(userDicts)
        response.status_code = status.HTTP_201_CREATED
        return {"status": "success", "data": result.acknowledged}
    except Exception as e:
        print("Error while inserting data", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Failed", "data": None}


# Get Single User by Id
@router.get("/users/{id}")
async def get_user(id: str, response: Response):
    if id == "":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "failed", "data": None}

    try:
        user = collection.find_one({"_id": ObjectId(id)})
        response.status_code = status.HTTP_200_OK
        return {"status": "success", "data": single_serializer(user)}
    except Exception as e:
        print("Error while getting user", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Failed", "data": None}


# Update Single User
@router.patch("/users/{id}")
async def update_user(id: str, update_data: dict, response: Response):
    if id == "":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "failed", "data": None}

    payload = dict(update_data)
    if "location" in payload:
        payload["location"] = dict(payload["location"])

    if "contact" in payload:
        payload["contact"] = dict(payload["contact"])

    try:
        result = collection.update_one({"_id": ObjectId(id)}, update={"$set": payload})
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"status": "success", "data": result.acknowledged}
    except Exception as e:
        print("Error while getting user", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Failed", "data": None}


# Delete Single User
@router.delete("/users/{id}")
async def delete_user(id: str, response: Response):
    if id == "":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "failed", "data": None}
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"status": "success", "data": result.acknowledged}
    except Exception as e:
        print("Error while Deleting user", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "Failed", "data": None}
