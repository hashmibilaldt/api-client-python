from datetime import datetime
from typing import List, Optional

from dynatrace.environment_v2.entity_type import EntityType
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.management_zone import ManagementZone
from dynatrace.configuration_v1.metag import METag
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList


class EntityService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        entity_selector: str,
        time_from: str = "now-2h",
        time_to: str = "now",
        fields: Optional[str] = None,
        page_size=50,
    ) -> PaginatedList["Entity"]:
        """
        :return: A list of monitored entities along with their properties.
        """
        params = {"pageSize": page_size, "entitySelector": entity_selector, "from": time_from, "to": time_to, "fields": fields}
        return PaginatedList(Entity, self.__http_client, "/api/v2/entities", params, list_item="entities")

    def list_types(self, page_size=50) -> PaginatedList[EntityType]:
        """
        Gets a list of properties for all entity types

        :param page_size: The desired amount of entities in a single response payload.
            The maximal allowed page size is 500.
            If not set, 50 is used.
        :return: A list of properties of all available entity types.
        """
        params = {"pageSize": page_size}
        return PaginatedList(EntityType, self.__http_client, "/api/v2/entityTypes", params, list_item="types")


class Entity(DynatraceObject):
    @property
    def from_relationships(self):
        # TODO
        return ""

    @property
    def to_relationships(self):
        # TODO
        return ""

    @property
    def first_seen_t_ms(self) -> datetime:
        # TODO
        """
        The timestamp at which the entity was first seen, in UTC milliseconds.
        :return:
        """
        return datetime.now()

    @property
    def last_seen_t_ms(self) -> datetime:
        # TODO
        """
        The timestamp at which the entity was last seen, in UTC milliseconds.
        :return:
        """
        return datetime.now()

    @property
    def entity_id(self) -> str:
        """
        The ID of the entity.
        :return:
        """
        return self._entity_id

    @property
    def display_name(self) -> str:
        """
        The name of the entity, displayed in the UI.
        :return:
        """
        return self._display_name

    @property
    def management_zones(self) -> List[ManagementZone]:
        return []

    @property
    def tags(self) -> List[METag]:
        return self._tags

    @property
    def properties(self) -> List[dict]:
        return self._properties

    def _create_from_raw_data(self, raw_element: dict):
        self._display_name = raw_element.get("displayName")
        self._entity_id = raw_element.get("entityId")
        self._properties = raw_element.get("properties", {})
        self._tags: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("tags", {})]

class EntityShortRepresentation(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")
