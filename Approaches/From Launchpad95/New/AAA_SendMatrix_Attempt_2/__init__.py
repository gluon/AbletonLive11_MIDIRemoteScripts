from _Framework.Capabilities import (
    CONTROLLER_ID_KEY,
    PORTS_KEY,
    NOTES_CC,
    SCRIPT,
    SYNC,
    REMOTE,
    controller_id,
    inport,
    outport,
)
from .Launchpad import Launchpad


def create_instance(c_instance):
    """Creates and returns the Launchpad script"""
    return Launchpad(c_instance)
