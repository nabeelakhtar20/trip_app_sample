from datetime import datetime

from neomodel import StringProperty, StructuredNode, RelationshipTo, BooleanProperty, \
    DateTimeProperty, EmailProperty, UniqueIdProperty, JSONProperty
from destination.models import City


class User(StructuredNode):
    uid = UniqueIdProperty()
    address = StringProperty()
    currency = StringProperty()
    date_joined = DateTimeProperty(default=datetime.now())
    favourites = JSONProperty()
    first_name = StringProperty()
    latitude = StringProperty()
    longitude = StringProperty()
    last_name = StringProperty()
    username = StringProperty(unique_index=True)
    email = EmailProperty(unique_index=True)
    is_active = BooleanProperty()
    last_login = DateTimeProperty()
    password = StringProperty()
    city = RelationshipTo(City, 'LIVES_IN')

    @property
    def serialize(self):
        return {
            'node_properties': {
                "id": self.uid,
                "address": self.address,
                "currency": self.currency,
                "date_joined": self.date_joined,
                "first_name": self.first_name,
                "latitude": str(self.latitude),
                "longitude": str(self.longitude),
                "last_name": self.last_name,
                "username": self.username,
                "email": self.email,
                "favourites": self.favourites,
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'City',
                'nodes_related': self.serialize_relationships(self.city.all()),
            },
        ]