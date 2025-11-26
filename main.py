from fastapi import FastAPI
from routes import (
    figures_milo,
    figure_infos,
    figure_infos_modif_customproperties,
    get_categories,
    get_subcategories,
    select_subcategory,
    get_selected,
)

app = FastAPI(
    title="PILS Server API",
    description="API for Milo figures and characters",
    version="1.0.0"
)

# Inclure les routes
app.include_router(figures_milo.router)
app.include_router(figure_infos.router)
app.include_router(figure_infos_modif_customproperties.router)
app.include_router(get_categories.router)
app.include_router(get_subcategories.router)
app.include_router(select_subcategory.router)
app.include_router(get_selected.router)