from fastapi import APIRouter

router = APIRouter(tags=["Book"])


@router.get("/books")
async def get_books():
    return [{"name": "Rick"}, {"author": "Morty"}]
#
#
# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}
#
#
# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}