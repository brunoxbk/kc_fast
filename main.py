from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from typing import Annotated
from pydantic import BaseModel

from models import Person, User
from database import engine, Base, get_db
from repositories import UserRepository, PersonRepository
from schemas import InitialPersonCreate, InitialPersonRetrieve


Base.metadata.create_all(bind=engine)


app = FastAPI()


# {'sub': '10373295-3342-4ea0-bfa7-a39a3b750f3c',
#  'email_verified': True, 'name': 'teste teste',
#  'preferred_username': 'teste',
#  'given_name': 'teste', 'family_name': 'teste','email': 'teste@gmail.com'}


# {'exp': 1713963449, 'iat': 1713963149, 'jti': '687e9d22-c510-4bf8-a709-7c77d96a8d18', 
#  'iss': 'http://localhost:8080/realms/CarShip', 'aud': 'account', 'sub': '10373295-3342-4ea0-bfa7-a39a3b750f3c',
#  'typ': 'Bearer', 'azp': 'carship-client', 'session_state': 'df093aa2-fc52-4fda-9f61-e823d555239a',
#  'acr': '1', 'realm_access': {'roles': ['offline_access', 'uma_authorization', 'default-roles-carship']}, 
#  'resource_access': {'account': {'roles': ['manage-account', 'manage-account-links', 'view-profile']}},
#    'scope': 'openid profile email', 'sid': 'df093aa2-fc52-4fda-9f61-e823d555239a', 
#    'email_verified': True, 'name': 'teste teste', 'preferred_username': 'teste', 
#    'given_name': 'teste', 'family_name': 'teste', 'email': 'teste@gmail.com'}

class User(BaseModel):
    uuid: str
    username: str
    email: str | None = None
    email_verified: bool
    full_name: str | None = None
    disabled: bool | None = None


oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://localhost:8080/realm/protocol/openid-connect/token",
    authorizationUrl="http://localhost:8080/realm/protocol/openid-connect/auth",
    refreshUrl="http://localhost:8080/realm/protocol/openid-connect/token",
)

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="carship-client",
    realm_name="CarShip",
    client_secret_key="B2Lr0jdRV1Vk3eg9BZjd57oMwXZaMmqt")


def decode_token(token):
    KEYCLOAK_PUBLIC_KEY = f"-----BEGIN PUBLIC KEY-----\n{keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"

    options = {
        "verify_signature": True,
        "verify_aud": False,
        "verify_exp": True
    }

    token_info = keycloak_openid.decode_token(
        token,
        key=KEYCLOAK_PUBLIC_KEY,
        options=options
    )
    return User(
        uuid=token_info['sid'],
        username=token_info['name'], 
        email=token_info['email'],
        email_verified=token_info['email_verified'],
        full_name=token_info['name']
    )

async def get_current_user(token: Annotated[str, Depends(oauth_2_scheme)]):
    user = decode_token(token)
    return user


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    try:
        
        user_info = keycloak_openid.userinfo(access_token)

        KEYCLOAK_PUBLIC_KEY = f"-----BEGIN PUBLIC KEY-----\n{keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"
        
        options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_exp": True
        }
        
        token_info = keycloak_openid.decode_token(
            access_token,
            key=KEYCLOAK_PUBLIC_KEY,
            options=options
        )

        return {"token_info": token_info, "user_info": user_info}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")


def has_role(role_name: str):
    async def check_role(
        token_info: Annotated[dict, Depends(valid_access_token)]
    ):
        roles = token_info["resource_access"]["account"]["roles"]
        print(roles)
        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


@app.get("/user-info")
def user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {"name": current_user.full_name, "email": current_user.email}


@app.get("/public")
def get_public():
    return {"message": "Ce endpoint est public"}


@app.post("/token")
def get_token():
    token = keycloak_openid.token("teste", "teste123")
    return {"token": token}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "Ce endpoint est privé"}


@app.get("/admin", dependencies=[Depends(has_role("admin"))])
def get_private():
    return {"message": "Admin only"}