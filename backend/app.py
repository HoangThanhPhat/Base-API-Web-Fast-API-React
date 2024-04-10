from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import(user_pydantic, user_pydanticIn, User)

# Email
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

# Import dotenv to load values
from dotenv import dotenv_values

# Load credentials from .env file
credentials = dotenv_values(".env")

# Adding cors headers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#-------------------------------------Adding CORS Url--------------------------------------------------
origins = [
    'http://localhost:3000'
    
]
# Add midlleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins     = origins,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

#---------------------------------------CRUD API------------------------------------------------------------
@app.get('/')
def index():
    return {"message": "Hello"}

@app.post('/user')
async def add_user(user_info: user_pydanticIn):
    user_obj = await User.create(**user_info.dict(exclude_unset = True))
    response = await user_pydantic.from_tortoise_orm(user_obj)
    return {"status": "ok", "data": response}

@app.get('/user')
async def get_all_users():
    response = await user_pydantic.from_queryset(User.all())
    return {"status": "ok", "data": response}

@app.get('/user/{User_ID}')
async def get_specific_user(User_ID: int):
    response = await user_pydantic.from_queryset_single(User.get(id = User_ID))
    return {"status": "ok", "data": response}

@app.put('/user/{User_ID}')
async def update_user(User_ID: int, update_info: user_pydanticIn):
    user                = await User.get(id = User_ID)
    update_info         = update_info.dict(exclude_unset = True)
    user.name           = update_info['name']
    user.password       = update_info['password']
    user.phone_number   = update_info['phone_number']
    user.email          = update_info['email']
    user.address        = update_info['address']
    await user.save()
    response            = await user_pydantic.from_tortoise_orm(user)
    return {"status": "ok", "data": response}

@app.delete('/user/{User_ID}')
async def delete_user(User_ID: int):
    user_obj = await User.get(id = User_ID)
    if user_obj:
        await user_obj.delete()
        return {"status": "ok"}
    return {"status": "User not exist!"}

#-----------------------------------------------Email function-----------------------------------------------
class EmailSchema(BaseModel):
    email: List[EmailStr]
    
class EmailContent(BaseModel):
    message: str
    subject: str


conf = ConnectionConfig(
    MAIL_USERNAME   = credentials['EMAIL'],
    MAIL_PASSWORD   = credentials['PASSWORD'],
    MAIL_FROM       = credentials["EMAIL"],
    MAIL_PORT       = 465,
    MAIL_SERVER     = "smtp.gmail.com",
    MAIL_STARTTLS   = False,
    MAIL_SSL_TLS    = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS  = True
)

@app.post("/email/{User_ID}")
async def send_email(User_ID: int, content: EmailContent):
    user_gui        = await User.get(id = User_ID)
    user_nhan       = await user_gui
    user_nhan_email = [user_nhan.email]
    
    html = f"""
    <h5>Công ty phatAI</h5> 
    <br>
    <p>{content.message}</p>
    <br>
    <h6>Chúc bạn một ngày tốt lành</h6>
    <h6>Công ty phatAI</h6>
    """


    message     = MessageSchema(
    subject     = content.subject,
    recipients  = user_nhan_email,
    body        = html,
    subtype     ="html")

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": "ok"}  

        


#------------------------------------------------ database----------------------------------------------
register_tortoise (
    app,
    db_url = "sqlite://database.sqlite3",
    modules= {"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)