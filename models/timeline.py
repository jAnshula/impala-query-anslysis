from dataclasses import dataclass,field
@dataclass
class Timeline:

    def __init__(self, events=None):

        self.events = events or {}

    def get(
        self,
        key,
        default=None
    ):
        return self.events.get(
            key,
            default
        )

    def __getitem__(
        self,
        key
    ):
        return self.events[key]

    def __contains__(
        self,
        key
    ):
        return key in self.events

    def keys(self):
        return self.events.keys()

    def values(self):
        return self.events.values()

    def items(self):
        return self.events.items()

    def to_dict(self):
        return dict(self.events)

    def __repr__(self):
        return (
            f"Timeline(events={self.events})"
        )

