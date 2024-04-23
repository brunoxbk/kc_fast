from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from keycloak import KeycloakOpenID

from typing import Annotated

app = FastAPI()

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://localhost:8080/realm/protocol/openid-connect/token",
    authorizationUrl="http://localhost:8080/realm/protocol/openid-connect/auth",
    refreshUrl="http://localhost:8080/realm/protocol/openid-connect/token",
)

keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="carship-client",
                                 realm_name="CarShip",
                                 client_secret_key="B2Lr0jdRV1Vk3eg9BZjd57oMwXZaMmqt")


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    try:
        print(access_token)
        print('aqui')
        userinfo = keycloak_openid.userinfo(access_token)
        print(userinfo)

        KEYCLOAK_PUBLIC_KEY = f"-----BEGIN PUBLIC KEY-----\n{keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"
        
        options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
        
        token_info = keycloak_openid.decode_token(access_token, key=KEYCLOAK_PUBLIC_KEY, options=options)

        print(token_info)

        return {"token_info": token_info, "user_info": user_info}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")


def has_role(role_name: str):
    async def check_role(
        token_data: Annotated[dict, Depends(valid_access_token)]
    ):
        roles = token_data["token_info"]["resource_access"]["account"]["roles"]
        print(roles)
        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


@app.get("/user-info")
def user_info():
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return {"userinfo": userinfo}


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