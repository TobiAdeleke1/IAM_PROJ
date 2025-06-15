from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from tier_auth.models import User
import requests
import uuid


AUTH0_DOMAIN = settings.DOMAIN
API_IDENTIFIER = settings.API_IDENTIFIER
ALGORITHMS = ["RS256"]


class Auth0JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Fetch public keys from Auth0
            jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = requests.get(jwks_url).json()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = next(
                (key for key in jwks["keys"] if key["kid"] == unverified_header["kid"]),
                None
            )

            if not rsa_key:
                raise AuthenticationFailed("Unable to find RSA key.")

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

            # Sync with custom user model
            auth0_id = payload["sub"]
            email = payload.get("email", auth0_id)
            user = User.objects.filter(auth0_id=auth0_id).first()
            if not user:
                user = User.objects.create(
                      auth0_id=auth0_id,
                      # TODO : Update
                      stripe_customer_id=f"{str(uuid.uuid4())}_random",
                      defaults={"email": email, "username": email[:150]}
                )

            # token claims
            request.auth = payload
            return user, payload

        except Exception as err:
            raise AuthenticationFailed(f"JWT validation error: {str(err)}")
