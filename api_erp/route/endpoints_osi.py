from fastapi import APIRouter

router_osi = APIRouter(prefix="/osi", tags=["OSI"])

@router_osi.get("/")
async def get_osi_info():
    """
    Endpoint to retrieve OSI model information.
    """
    osi_info = {
        "model": "OSI Model",
        "layers": [
            {"name": "Physical", "number": 1},
            {"name": "Data Link", "number": 2},
            {"name": "Network", "number": 3},
            {"name": "Transport", "number": 4},
            {"name": "Session", "number": 5},
            {"name": "Presentation", "number": 6},
            {"name": "Application", "number": 7}
        ]
    }
    return osi_info