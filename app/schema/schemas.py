def single_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": str(user["firstName"]),
        "lastName": str(user["lastName"]),
        "age": int(user["age"]),
        "contact": dict(
            {
                "email": user["contact"]["email"],
                "phoneNumber": user["contact"]["phoneNumber"],
            }
        ),
        "location": {
            "countryName": str(user["location"]["countryName"]),
            "countryCode": str(user["location"]["countryCode"]),
            "phoneCode": str(user["location"]["phoneCode"]),
            "area": str(user["location"]["area"]),
        },
        "password": str(user["password"]),
        "statusId": int(user["statusId"]),
        "createdAt": user["createdAt"],
        "updatedAt": user["updatedAt"],
    }


def multiple_serializer(users) -> list:
    return [single_serializer(user) for user in users]
