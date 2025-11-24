from fastapi import FastAPI
from routes import figures_milo, figure_infos

app = FastAPI(
    title="PILS Server API",
    description="API for Milo figures and characters",
    version="1.0.0"
)

# Inclure les routes
app.include_router(figures_milo.router)
app.include_router(figure_infos.router)
