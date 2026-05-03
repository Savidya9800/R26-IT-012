from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT (Change in production!)
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Mock user database (Replace with actual DB later)
MOCK_USERS = {
    "student@university.edu": {
        "id": 1,
        "email": "student@university.edu",
        "full_name": "Medical Student",
        "role": "Student",
        "hashed_password": pwd_context.hash("password123")
    },
    "dr.thorne@hospital.org": {
        "id": 2,
        "email": "dr.thorne@hospital.org",
        "full_name": "Dr. Sarah Thorne",
        "role": "Clinician",
        "hashed_password": pwd_context.hash("password123")
    },
    "admin@hospital.org": {
        "id": 3,
        "email": "admin@hospital.org",
        "full_name": "Admin User",
        "role": "Admin",
        "hashed_password": pwd_context.hash("password123")
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """
    Login endpoint - accepts email and password, returns JWT token
    """
    user = MOCK_USERS.get(credentials.email)
    
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]},
        expires_delta=timedelta(hours=8)
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"]
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = None):
    """
    Get current user info from token (protected route)
    """
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = MOCK_USERS.get(email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"]
    )