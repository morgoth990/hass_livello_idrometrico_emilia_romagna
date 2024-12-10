"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from .entity import IntegrationBlueprintEntity

from homeassistant.const import CONF_NAME, UnitOfLength

from .const import CONF_STATION_NAME, DOMAIN, LOGGER


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import BlueprintDataUpdateCoordinator
    from .data import IntegrationBlueprintConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: IntegrationBlueprintConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    entity_description_value = SensorEntityDescription(
        key="livelloIdrometricoEmiliaRomagna",
        name=entry.data[CONF_STATION_NAME] + " Water level",
        icon="mdi:waves-arrow-up",
    )
    entity_description_soglia1 = SensorEntityDescription(
        key="livelloIdrometricoEmiliaRomagna_level1",
        name=entry.data[CONF_STATION_NAME] + " Theshold 1 [YELLOW]",
        icon="mdi:format-header-1",
    )
    entity_description_soglia2 = SensorEntityDescription(
        key="livelloIdrometricoEmiliaRomagna_level2",
        name=entry.data[CONF_STATION_NAME] + " Theshold 2 [ORANGE]",
        icon="mdi:format-header-2",
    )
    entity_description_soglia3 = SensorEntityDescription(
        key="livelloIdrometricoEmiliaRomagna_level3",
        name=entry.data[CONF_STATION_NAME] + " Theshold 3 [RED]",
        icon="mdi:format-header-3",
    )

    async_add_entities(
        {
            IntegrationBlueprintSensor(
                "value",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_value,
            ),
            IntegrationBlueprintSensor(
                "soglia1",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia1,
            ),
            IntegrationBlueprintSensor(
                "soglia2",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia2,
            ),
            IntegrationBlueprintSensor(
                "soglia3",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia3,
            ),
        }
    )


class IntegrationBlueprintSensor(IntegrationBlueprintEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        value_name: str,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""

        self._attr_unique_id = coordinator.config_entry.entry_id + "_" + value_name
        self.value_name = value_name
        self.entity_description = entity_description

        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

        super().__init__(coordinator)

    @property
    def native_unit_of_measurement(self) -> str | None:
        return UnitOfLength.METERS

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.value_name)
