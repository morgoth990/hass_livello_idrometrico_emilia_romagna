"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from ast import Num
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
    entity_description_alert = SensorEntityDescription(
        key="livelloIdrometricoEmiliaRomagna_alert",
        name=entry.data[CONF_STATION_NAME] + " Alert",
        icon="mdi:alert",
    )

    async_add_entities(
        {
            WaterLevelSensor(
                "value",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_value,
            ),
            WaterLevelSensor(
                "soglia1",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia1,
            ),
            WaterLevelSensor(
                "soglia2",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia2,
            ),
            WaterLevelSensor(
                "soglia3",
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_soglia3,
            ),
            AlertSensor(
                coordinator=entry.runtime_data.coordinator,
                entity_description=entity_description_alert,
            ),
        }
    )


class WaterLevelSensor(IntegrationBlueprintEntity, SensorEntity):
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


class AlertSensor(IntegrationBlueprintEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        coordinator: BlueprintDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""

        self._attr_unique_id = coordinator.config_entry.entry_id + "_alert"
        self.entity_description = entity_description

        self._attr_device_class = SensorDeviceClass.ENUM
        self.options = ["None", "Yellow", "Orange", "Red"]

        super().__init__(coordinator)

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        value = self.coordinator.data.get("value")
        soglia1 = self.coordinator.data.get("soglia1")
        soglia2 = self.coordinator.data.get("soglia2")
        soglia3 = self.coordinator.data.get("soglia3")

        if value < soglia3 and value < soglia2 and value < soglia1:
            return "None"
        if value < soglia3 and value < soglia2:
            return "Yellow"
        if value < soglia3:
            return "Orange"
        return "Red"
