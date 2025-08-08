from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from models import Base, User, SessionLocal, engine
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверяем существование пользователя
    db_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Создаем пользователя
    db_user = User(username=username, email=email, hashed_password=password)
    db.add(db_user)
    db.commit()

    # Перенаправляем на страницу входа
    return RedirectResponse(url="/login", status_code=303)

@app.post("/login/")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or password != db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Неправильный логин или пароль")
    
    return RedirectResponse(url="/welcome", status_code=303)

# Страницы
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/login")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("sansara.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("sanara.html", {"request": request})

@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})