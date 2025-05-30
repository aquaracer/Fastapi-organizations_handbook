from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from src.organizations_handbook.dependencies.organization_dependencies import get_organization_service, verify_api_key
from src.organizations_handbook.exceptions.organization_exceptions import OrganizationNotFound
from src.organizations_handbook.schemas.organization_schema import OrganizationSchema, OrganizationBuildingSchema
from src.organizations_handbook.services.organization_services import OrganizationService

router = APIRouter(prefix='/organization', tags=['organization'])


@router.get(
    "/get_organization/{organization_id}",
    response_model=OrganizationSchema,
    description="Вывод информации об организации по её идентификатору"
)
async def get_organization(
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
        organization_id: int,
):
    try:
        return await organization_service.get_organization(organization_id=organization_id)
    except OrganizationNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.detail
        )


@router.get(
    "/get_organization_by_name/{organization_name}",
    response_model=OrganizationSchema,
    description="Поиск организации по названию"
)
async def get_organization_by_name(
        organization_name: str,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
):
    try:
        return await organization_service.get_organization_by_name(organization_name=organization_name)
    except OrganizationNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.detail
        )


@router.get(
    "/list_organizations_by_building/{building_id}",
    response_model=list[OrganizationSchema],
    description="Список всех организаций, находящихся в конкретном здании"
)
async def list_organizations_by_building(
        building_id: int,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
):
    return await organization_service.list_organizations_by_building(building_id=building_id)


@router.get(
    "/list_organizations_by_location",
    response_model=OrganizationBuildingSchema,
    description="Список организаций и зданий, которые находятся в заданном радиусе относительно указанной точки на "
                "карте"
)
async def list_organizations_by_location(
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
        latitude: float = Query(..., description="Широта"),
        longitude: float = Query(..., description="Долгота"),
        radius: float = Query(1.0, description="Радиус в километрах"),
):
    return await organization_service.list_organizations_by_location(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )


@router.get(
    "/list_organizations_by_activity/{activity}",
    response_model=list[OrganizationSchema],
    description="Список всех организаций, которые относятся к указанному виду деятельности"
)
async def list_organizations_by_activity(
        activity: str,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
):
    return await organization_service.list_organizations_by_activity(activity=activity)


@router.get(
    "/search_organizations_by_activity/{activity}",
    response_model=list[OrganizationSchema],
    description="""искать организации по виду деятельности. Например, поиск по виду деятельности «Еда», 
                   которая находится на первом уровне дерева, и чтобы нашлись все организации, которые относятся к 
                   видам деятельности, лежащим внутри. Т.е. в результатах поиска должны отобразиться организации с 
                   видом деятельности Еда, Мясная продукция, Молочная продукция."""
)
async def search_organizations_by_activity(
        activity: str,
        organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
):
    return await organization_service.search_organizations_by_activity(activity=activity)
