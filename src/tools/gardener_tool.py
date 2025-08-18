from typing import Annotated, List, Optional, TypedDict
from semantic_kernel.functions import kernel_function

class PlantModel(TypedDict):
   id: int
   name: str
   species: str
   last_watered: str  # ISO format date
   last_fertilized: str  # ISO format date
   health_status: str  # "Good", "Needs attention", "Critical"
   location: str
   
class GardenerTool:
    
    def __init__(self):
        self.plants: list[PlantModel] = [
            {
                "id": 1, 
                "name": "Ficus", 
                "species": "Ficus elastica", 
                "last_watered": "2025-08-10", 
                "last_fertilized": "2025-07-20", 
                "health_status": "Good", 
                "location": "Living Room"
            },
            {
                "id": 2, 
                "name": "Peace Lily", 
                "species": "Spathiphyllum", 
                "last_watered": "2025-08-05", 
                "last_fertilized": "2025-08-01", 
                "health_status": "Needs attention", 
                "location": "Bedroom"
            },
            {
                "id": 3, 
                "name": "Succulent", 
                "species": "Echeveria elegans", 
                "last_watered": "2025-07-25", 
                "last_fertilized": "2025-06-15", 
                "health_status": "Critical", 
                "location": "Kitchen"
            },
        ]
    
    @kernel_function
    async def get_plants(self) -> List[PlantModel]:
        """Gets a list of all plants and their current status."""
        return self.plants

    @kernel_function
    async def get_plant(self, id: Annotated[int, "The ID of the plant"]) -> Optional[PlantModel]:
        """Gets the status of a particular plant."""
        for plant in self.plants:
            if plant["id"] == id:
                return plant
        return None

    @kernel_function
    async def water_plant(self, id: Annotated[int, "The ID of the plant"], date: Annotated[str, "The date in YYYY-MM-DD format"]) -> Optional[PlantModel]:
        """Updates the last watered date for a plant."""
        for plant in self.plants:
            if plant["id"] == id:
                plant["last_watered"] = date
                # If plant was critical and is now watered, update status
                if plant["health_status"] == "Critical":
                    plant["health_status"] = "Needs attention"
                return plant
        return None
    
    @kernel_function
    async def fertilize_plant(self, id: Annotated[int, "The ID of the plant"], date: Annotated[str, "The date in YYYY-MM-DD format"]) -> Optional[PlantModel]:
        """Updates the last fertilized date for a plant."""
        for plant in self.plants:
            if plant["id"] == id:
                plant["last_fertilized"] = date
                # If plant needed attention and is now fertilized, update status
                if plant["health_status"] == "Needs attention":
                    plant["health_status"] = "Good"
                return plant
        return None
        
    @kernel_function
    async def update_health_status(self, id: Annotated[int, "The ID of the plant"], status: Annotated[str, "The new health status"]) -> Optional[PlantModel]:
        """Updates the health status of a plant."""
        for plant in self.plants:
            if plant["id"] == id:
                plant["health_status"] = status
                return plant
        return None
        
    @kernel_function
    async def relocate_plant(self, id: Annotated[int, "The ID of the plant"], new_location: Annotated[str, "The new location"]) -> Optional[PlantModel]:
        """Moves a plant to a new location."""
        for plant in self.plants:
            if plant["id"] == id:
                plant["location"] = new_location
                return plant
        return None
