"""Tests for data models."""

from highcommand.models import CampaignInfo, PlanetInfo, Statistics, WarInfo


def test_war_info_model():
    """Test WarInfo model."""
    data = {
        "id": 1,
        "index": 801,
        "startDate": "2024-01-23T20:05:13.000Z",
        "endDate": "2028-02-08T20:04:55.000Z",
        "time": "1970-04-11T20:12:10.000Z",
        "createdAt": "2024-05-22T12:00:10.239Z",
        "updatedAt": "2024-05-22T12:00:10.239Z",
    }

    war_info = WarInfo(**data)
    assert war_info.id == 1
    assert war_info.index == 801


def test_campaign_info_model():
    """Test CampaignInfo model."""
    data = {
        "id": 1,
        "planet": 10,
        "type": 1,
        "count": 5,
        "createdAt": "2024-05-22T12:00:10.239Z",
        "updatedAt": "2024-05-22T12:00:10.239Z",
    }

    campaign = CampaignInfo(**data)
    assert campaign.id == 1
    assert campaign.planet == 10
    assert campaign.type == 1


def test_planet_info_model():
    """Test PlanetInfo model."""
    data = {
        "index": 0,
        "name": "Sicarus Prime",
        "sector": "Sector 1",
        "position": {"x": 100, "y": 200},
    }

    planet = PlanetInfo(**data)
    assert planet.index == 0
    assert planet.name == "Sicarus Prime"
    assert planet.position["x"] == 100


def test_statistics_model():
    """Test Statistics model."""
    data = {
        "id": 1,
        "missionsWon": 232299033,
        "missionsLost": 24922081,
        "missionTime": 528222382946,
        "bugKills": 38471552786,
        "automatonKills": 15595777961,
        "illuminateKills": 28,
        "bulletsFired": 303336002871,
        "bulletsHit": 336527984287,
        "timePlayed": 528222382946,
        "deaths": 1411862056,
        "revives": 2,
        "friendlyKills": 191683618,
        "missionSuccessRate": 90,
        "accuracy": 100,
        "createdAt": "2024-05-22T12:00:10.239Z",
        "updatedAt": "2024-05-22T12:00:10.239Z",
    }

    stats = Statistics(**data)
    assert stats.id == 1
    assert stats.missionsWon == 232299033
    assert stats.missionSuccessRate == 90
