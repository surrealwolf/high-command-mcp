"""Data models for HellHub Collective API responses."""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationInfo(BaseModel):
    """Pagination information for list responses."""

    page: int
    pageSize: int = Field(..., alias="pageSize")
    total: int
    pageCount: int = Field(..., alias="pageCount")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper from HellHub."""

    data: Any  # Can be a single object or list
    error: Optional[str] = None
    pagination: Optional[PaginationInfo] = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class WarInfo(BaseModel):
    """War information."""

    id: int
    index: int
    startDate: datetime = Field(..., alias="startDate")
    endDate: datetime = Field(..., alias="endDate")
    time: datetime
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class PlanetInfo(BaseModel):
    """Planet information."""

    index: int
    name: str
    sector: str
    position: dict[str, float]
    biome: dict[str, Any] = {}
    hazards: list[dict[str, Any]] = []
    status: Optional[dict[str, Any]] = None

    class Config:
        """Pydantic config."""

        populate_by_name = True


class Statistics(BaseModel):
    """Global game statistics."""

    id: int
    missionsWon: int = Field(..., alias="missionsWon")
    missionsLost: int = Field(..., alias="missionsLost")
    missionTime: int = Field(..., alias="missionTime")
    bugKills: int = Field(..., alias="bugKills")
    automatonKills: int = Field(..., alias="automatonKills")
    illuminateKills: int = Field(..., alias="illuminateKills")
    bulletsFired: int = Field(..., alias="bulletsFired")
    bulletsHit: int = Field(..., alias="bulletsHit")
    timePlayed: int = Field(..., alias="timePlayed")
    deaths: int
    revives: int
    friendlyKills: int = Field(..., alias="friendlyKills")
    missionSuccessRate: int = Field(..., alias="missionSuccessRate")
    accuracy: int
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class CampaignInfo(BaseModel):
    """Campaign information."""

    id: int
    planet: int
    type: int
    count: int
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")

    class Config:
        """Pydantic config."""

        populate_by_name = True


class APIError(BaseModel):
    """API error response."""

    error: str
    message: Optional[str] = None
    status_code: int = Field(..., alias="statusCode")

    class Config:
        """Pydantic config."""

        populate_by_name = True
