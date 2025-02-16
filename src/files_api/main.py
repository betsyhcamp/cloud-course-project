from textwrap import dedent

from fastapi import FastAPI
from fastapi.routing import APIRoute

from files_api.errors import handle_broad_exceptions
from files_api.routes import ROUTER
from files_api.settings import Settings


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}--{route.name}"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a FastAPI application."""
    settings = settings or Settings()

    app = FastAPI(
        title="Files API",
        summary="Store and retrieve files and file metadata.",
        version="v0",
        description=dedent(
            """
            ![Maintained by](https://img.shields.io/badge/Maintained_by-E_Camp-blue)
            
                
            [Project Github Repo](https://github.com/betsyhcamp/cloud-course-project)
            """
        ),
        docs_url="/",
        generate_unique_id_function=custom_generate_unique_id,
    )

    app.state.settings = settings
    app.include_router(ROUTER)

    app.middleware("http")(handle_broad_exceptions)

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
