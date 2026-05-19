import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_CHANNEL, CONF_ID

from .. import WavinAHC9000, ns

CONF_PARENT_ID = "wavinahc9000v3_id"
CONF_TYPE = "type"

WavinChildLockSwitch = ns.class_("WavinChildLockSwitch", switch.Switch)
WavinConfigBitSwitch = ns.class_("WavinConfigBitSwitch", switch.Switch)

# Bit masks per AC-116 Modbus spec 1.6.9 (Packed Configuration register).
TYPE_BIT_MASKS = {
    "control_lock": 0x0400,       # bit 10 — display padlock ("user can't change anything")
    "service_menu_lock": 0x0800,  # bit 11 — INT LOCK ("user can't enter service menu")
    "floor_sensor": 0x4000,       # bit 14 — FLOOR ENA, drives the "floor sensor active" dash icon
}

CONFIG_SCHEMA = cv.typed_schema(
    {
        "child_lock": switch.switch_schema(WavinChildLockSwitch).extend(
            {
                cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
                cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
            }
        ),
        "control_lock": switch.switch_schema(WavinConfigBitSwitch).extend(
            {
                cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
                cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
            }
        ),
        "service_menu_lock": switch.switch_schema(WavinConfigBitSwitch).extend(
            {
                cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
                cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
            }
        ),
        "floor_sensor": switch.switch_schema(WavinConfigBitSwitch).extend(
            {
                cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
                cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
            }
        ),
    },
    key=CONF_TYPE,
    default_type="child_lock",
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])
    ch = config[CONF_CHANNEL]
    typ = config[CONF_TYPE]
    var = await switch.new_switch(config)
    cg.add(var.set_parent(hub))
    cg.add(var.set_channel(ch))

    if typ == "child_lock":
        cg.add(hub.add_channel_child_lock_switch(ch, var))
    elif typ == "control_lock":
        cg.add(var.set_bit_mask(TYPE_BIT_MASKS[typ]))
        cg.add(hub.add_channel_control_lock_switch(ch, var))
    elif typ == "service_menu_lock":
        cg.add(var.set_bit_mask(TYPE_BIT_MASKS[typ]))
        cg.add(hub.add_channel_service_menu_lock_switch(ch, var))
    elif typ == "floor_sensor":
        cg.add(var.set_bit_mask(TYPE_BIT_MASKS[typ]))
        cg.add(hub.add_channel_floor_sensor_switch(ch, var))
