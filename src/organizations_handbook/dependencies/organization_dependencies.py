from starlette import status
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.config.project_config import Settings
from src.organizations_handbook.repositories.organization_repository import OrganizationRepository
from src.organizations_handbook.services.organization_services import OrganizationService


async def get_organization_repository(db_session: AsyncSession = Depends(get_db_session)) -> OrganizationRepository:
    return OrganizationRepository(db_session=db_session)


async def get_organization_service(
        organization_repository: OrganizationRepository = Depends(get_organization_repository),
) -> OrganizationService:
    return OrganizationService(organization_repository=organization_repository)


header_scheme = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key_header: str = Depends(header_scheme)):
    settings = Settings()
    if api_key_header == settings.API_KEY:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
