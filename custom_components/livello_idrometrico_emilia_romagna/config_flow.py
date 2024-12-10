"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    IntegrationBlueprintApiClient,
    IntegrationBlueprintApiClientCommunicationError,
    IntegrationBlueprintApiClientError,
)
from .const import CONF_STATION_NAME, DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_station_name(
                    station_name=user_input[CONF_STATION_NAME]
                )
            except IntegrationBlueprintApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except IntegrationBlueprintApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_STATION_NAME],
                    data=user_input,
                )

        station_names = []
        client = IntegrationBlueprintApiClient(
            station_name="",
            session=async_create_clientsession(self.hass),
        )
        result = await client.async_get_stations()
        for station in result:
            if self.find_config_entry_with_title(station["nomestaz"]) is None:
                station_names.append(station["nomestaz"])  # noqa: PERF401

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_STATION_NAME,
                        default=(user_input or {}).get(
                            CONF_STATION_NAME, vol.UNDEFINED
                        ),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(options=station_names, sort=True),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_station_name(self, station_name: str) -> None:
        """Validate credentials."""
        client = IntegrationBlueprintApiClient(
            station_name=station_name,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

    def find_config_entry_with_title(
        self, title_to_search: str
    ) -> config_entries.ConfigEntry | None:
        """Find a conf entry with the specified title."""
        for entry in self.hass.config_entries.async_entries():
            if entry.title == title_to_search:
                return entry
        return None
