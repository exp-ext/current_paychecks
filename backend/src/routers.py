from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

router = APIRouter(
    prefix="/docs",
)


@router.get('/swagger/', include_in_schema=False)
async def get_swagger_documentation():
    openapi_schema = get_openapi(
        title='API documentation',
        version='1.0.0',
        description='API documentation',
        routes=router.routes,
    )
    return get_swagger_ui_html(
        openapi_schema,
        title='API documentation',
        with_oauth=True
    )


@router.get('/redoc/', include_in_schema=False)
async def get_redoc_documentation():
    openapi_schema = get_openapi(
        title='API documentation',
        version='1.0.0',
        description='API documentation',
        routes=router.routes,
    )
    return get_redoc_html(openapi_schema, title='API documentation')
