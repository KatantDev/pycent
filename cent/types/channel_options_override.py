from typing import Optional

from cent.types.base import CentResult
from cent.types.bool_value import BoolValue


class ChannelOptionsOverride(CentResult):
    """Override object."""

    presence: Optional[BoolValue] = None
    """Override presence."""
    join_leave: Optional[BoolValue] = None
    """Override join_leave."""
    force_push_join_leave: Optional[BoolValue] = None
    """Override force_push_join_leave."""
    force_positioning: Optional[BoolValue] = None
    """Override force_positioning."""
    force_recovery: Optional[BoolValue] = None
    """Override force_recovery."""