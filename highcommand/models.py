"""Data models for HellHub Collective API responses."""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationInfo(BaseModel):
    """Pagination information for list responses."""

    model_config = ConfigDict(populate_by_name=True)

    page: int
    pageSize: int = Field(..., alias="pageSize")
    total: int
    pageCount: int = Field(..., alias="pageCount")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper from HellHub."""

    model_config = ConfigDict(populate_by_name=True)

    data: Any  # Can be a single object or list
    error: Optional[str] = None
    pagination: Optional[PaginationInfo] = None


class WarInfo(BaseModel):
    """War information."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    index: int
    startDate: datetime = Field(..., alias="startDate")
    endDate: datetime = Field(..., alias="endDate")
    time: datetime
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")


class PlanetInfo(BaseModel):
    """Planet information."""

    model_config = ConfigDict(populate_by_name=True)

    index: int
    name: str
    sector: str
    position: dict[str, float]
    biome: dict[str, Any] = {}
    hazards: list[dict[str, Any]] = []
    status: Optional[dict[str, Any]] = None


class Statistics(BaseModel):
    """Global game statistics."""

    model_config = ConfigDict(populate_by_name=True)

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


class CampaignInfo(BaseModel):
    """Campaign information."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    planet: int
    type: int
    count: int
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")


class APIError(BaseModel):
    """API error response."""

    model_config = ConfigDict(populate_by_name=True)

    error: str
    message: Optional[str] = None
    status_code: int = Field(..., alias="statusCode")
