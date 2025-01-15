from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.users import UserSchema, is_existing_user, password_hash, save_user, handleLogin
from models.urls import UrlSchema, add_url, load_file, save_all_data

node = APIRouter();
templates = Jinja2Templates("templates");

@node.get('/', response_class=HTMLResponse)
async def index(request: Request, error: bool = False):
    isAuth = request.cookies.get('email');
    if isAuth:
        return RedirectResponse('/dashboard');

    return templates.TemplateResponse("login.html", {"request":request,'error':error})

@node.get('/register')
async def register_view(request: Request):
    isAuth = request.cookies.get('email');
    if isAuth:
        return RedirectResponse('/dashboard');
    return templates.TemplateResponse("register.html", {"request": request });

@node.post("/register")
async def create_user(request: Request,
    username: str = Form(...), 
    email: str = Form(...),
    password: str = Form(...) 
):    
    user = UserSchema(username=username, email=email, password=password)
    user.password = password_hash(user.password);

    isExisting = is_existing_user(user.email);
    if isExisting:
        return templates.TemplateResponse(
                        "register.html", 
                        {
                            "request":request,
                            'errorMsg':"Email is already existing"
                        }
                    );

    save_user(dict(user));          
    return templates.TemplateResponse(
        "login.html", 
        {"request":request, "successMsg":"Successfully Registration"
    })

@node.post("/login")
async def handle_login(
    request: Request,
    email: str = Form(...), 
    password: str = Form(...)
    ):
    
    formData = dict(email=email, password=password)
   
    isLogin = handleLogin(formData)
    if isLogin:
        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie("email", email)
        return response;
        
    return RedirectResponse("/?error=true", status_code=302)

@node.get('/dashboard')
async def dashboard(request: Request):

    email = request.cookies.get('email');
    if not email:
        return RedirectResponse('/');

    get_all_urls = load_file();
    get_all_urls = get_all_urls.get(email);
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request":request, "urls":get_all_urls}
    )

@node.post('/create_url')
async def create_url(request: Request,url: str = Form(...)):
    
    email = request.cookies.get('email');
    if not email:
        return RedirectResponse('/');

    add_url(url, email)
    return RedirectResponse(url="/dashboard", status_code=302)

@node.get('/url/delete/{short_id}')
async def delete_url(request: Request, short_id: str):

    email = request.cookies.get('email');
    if not email:
        return RedirectResponse('/');

    get_all_urls = load_file()
    user_urls = get_all_urls.get(email);
    updated_urls = [url for url in user_urls if url["short_id"] != short_id]

    get_all_urls[email] = updated_urls
    save_all_data(get_all_urls);
    print(get_all_urls)

    return RedirectResponse(url="/dashboard", status_code=302)

@node.get('/r/{short_id}')
async def redirect_url_by_short_id(request: Request,short_id: str):
    get_all_urls = load_file()
    if get_all_urls:
        for user_urls in get_all_urls.values():
            for url in user_urls:
                if url["short_id"] == short_id:
                    return RedirectResponse(url["url"])
    
    return RedirectResponse("/");

@node.get("/logout")
async def logout():
    response = RedirectResponse("/")
    response.delete_cookie("email")
    return response

