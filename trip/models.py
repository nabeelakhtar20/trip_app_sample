from datetime import datetime

from neomodel import StringProperty, StructuredNode, RelationshipTo, \
    IntegerProperty, DateTimeProperty, UniqueIdProperty, JSONProperty, DateProperty

from auth.models import User


class Trip(StructuredNode):
    uid = UniqueIdProperty()
    destination = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    adults = IntegerProperty()
    infants = IntegerProperty()
    estimated_budget_start = IntegerProperty()
    estimated_budget_end = IntegerProperty()
    events = JSONProperty()
    creation_date = DateTimeProperty(default=datetime.now())
    last_updated = DateTimeProperty(default=datetime.now())

    user = RelationshipTo(User, 'PLANNED_BY')

    @property
    def serialize(self):
        return {
            'node_properties': {
                "id": self.uid,
                "destination": self.destination,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "adults": self.adults,
                "infants": self.infants,
                "estimated_budget_start": self.estimated_budget_start,
                "estimated_budget_end": self.estimated_budget_end,
                "events": self.events,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'User',
                'nodes_related': self.serialize_relationships(self.user.all()),
            },
        ]