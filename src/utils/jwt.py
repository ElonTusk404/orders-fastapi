from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from src.schemas.token import DecodedToken
from src.config import settings

security = HTTPBearer(scheme_name="BearerAuth", auto_error=True)

def get_current_user(required_scope: str = None):
    async def _get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> DecodedToken:
        token = credentials.credentials
        try:
            payload = jwt.decode(
                token, 
                settings.PUBLIC_KEY, 
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
            
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )

            user_scopes = payload.get("scopes", [])
            if required_scope and required_scope not in user_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )

            return DecodedToken(
                user_id=payload["user_id"],
                scopes=user_scopes
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

    return _get_current_user