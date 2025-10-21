"""MCP Server initialization."""

__version__ = "0.1.0"
__author__ = "Lee"
__email__ = "lee@fullmetal.dev"

from highcommand.api_client import HighCommandAPIClient
from highcommand.models import CampaignInfo, WarInfo

__all__ = [
    "CampaignInfo",
    "HighCommandAPIClient",
    "WarInfo",
]
