import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor

from . import WavinAHC9000

CONF_PARENT_ID = "wavin_ahc9000_id"
CONF_TYPE = "type"
CONF_CHANNEL = "channel"


def _validate_alarm_channel(config):
    if config[CONF_TYPE] == "alarm" and CONF_CHANNEL not in config:
        raise cv.Invalid("'channel' is required when type is 'alarm'")
    return config


CONFIG_SCHEMA = cv.All(
    binary_sensor.binary_sensor_schema().extend(
        {
            cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
            cv.Required(CONF_TYPE): cv.one_of("yaml_ready", "alarm", lower=True),
            cv.Optional(CONF_CHANNEL): cv.int_range(min=1, max=16),
        }
    ),
    _validate_alarm_channel,
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])
    bs = await binary_sensor.new_binary_sensor(config)
    if config[CONF_TYPE] == "yaml_ready":
        cg.add(hub.set_yaml_ready_binary_sensor(bs))
    elif config[CONF_TYPE] == "alarm":
        cg.add(hub.add_channel_alarm_binary_sensor(config[CONF_CHANNEL], bs))
        cg.add(hub.add_active_channel(config[CONF_CHANNEL]))
