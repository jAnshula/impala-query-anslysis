from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Timeline:
    """Represents query execution timeline with phase-based events.
    
    Provides dictionary-like access to timeline events and metrics.
    """

    events: Dict[str, Any] = field(
        default_factory=dict
    )

    def get(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """Get timeline event by key with optional default.
        
        Args:
            key: Timeline event key (e.g., 'planning_ms')
            default: Value to return if key not found
            
        Returns:
            Event value or default if not found
        """
        return self.events.get(key, default)

    def __getitem__(
        self,
        key: str
    ) -> Any:
        """Get timeline event by key. Raises KeyError if not found."""
        return self.events[key]

    def __contains__(
        self,
        key: str
    ) -> bool:
        """Check if key exists in timeline events."""
        return key in self.events

    def keys(self):
        """Return keys of all timeline events."""
        return self.events.keys()

    def values(self):
        """Return values of all timeline events."""
        return self.events.values()

    def items(self):
        """Return (key, value) pairs of all timeline events."""
        return self.events.items()

    def to_dict(self) -> Dict[str, Any]:
        """Convert timeline to dictionary representation."""
        return dict(self.events)

    def __repr__(self) -> str:
        """String representation of Timeline."""
        return f"Timeline(events={self.events})"