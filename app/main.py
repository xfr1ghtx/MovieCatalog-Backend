from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import auth, user, movies, favorites, reviews

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="v1",
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/swagger.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
    root_path=settings.ROOT_PATH,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(movies.router)
app.include_router(favorites.router)
app.include_router(reviews.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to MovieCatalog.API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

