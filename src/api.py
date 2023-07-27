import uvicorn
from app.api.handlers.catalog import router as catalog_router
from app.api.handlers.healthcheck import router as heath_router
from app.api.settings import ApiSettings
from dependencies import lifespan
from fastapi import FastAPI


api_settings = ApiSettings()


app = FastAPI(
    version=api_settings.version,
    lifespan=lifespan,
)

app.include_router(heath_router)
app.include_router(catalog_router)


if __name__ == "__main__":

    uvicorn.run(
        "api:app",
        host=str(api_settings.host),
        port=api_settings.port,
        root_path=api_settings.root_path,
    )
