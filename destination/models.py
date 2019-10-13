from neomodel import StringProperty, StructuredNode, RelationshipFrom, IntegerProperty, FloatProperty

from trip_app_sample.nodeutils import NodeUtils


class Country(StructuredNode):
    official_name_en = StringProperty()
    Languages = StringProperty()
    Capital = StringProperty()
    Dial = StringProperty()
    Continent = StringProperty()
    name = StringProperty()
    is_independent = StringProperty()


class City(StructuredNode, NodeUtils):
    elevation = StringProperty()
    digital_elevation_model = IntegerProperty()
    geonameid = IntegerProperty()
    timezone = StringProperty()
    latitude = FloatProperty()
    population = IntegerProperty()
    alternatenames = StringProperty()
    country_code = StringProperty()
    feature_class = StringProperty()
    composite_id = StringProperty()
    name = StringProperty()
    asciiname = StringProperty()
    feature_code = StringProperty()
    alternate_country_codes = FloatProperty()
    longitude = FloatProperty()
    country = RelationshipFrom(Country, 'IS_IN')

    @property
    def serialize(self):
        return {
            'node_properties': {
                "elevation": self.elevation,
                "digital_elevation_model": self.digital_elevation_model,
                "geonameid": self.geonameid,
                "timezone": self.timezone,
                "latitude": str(self.latitude),
                "population": self.population,
                "alternatenames": self.alternatenames,
                "country_code": self.country_code,
                "feature_class": self.feature_class,
                "composite_id": self.composite_id,
                "name": self.name,
                "asciiname": self.asciiname,
                "feature_code": self.feature_code,
                "alternate_country_codes": str(self.alternate_country_codes),
                "longitude": str(self.longitude)
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Country',
                'nodes_related': self.serialize_relationships(self.country.all()),
            },
        ]

    def getData(self, city_name, country_code):
        self.cypher("MATCH (c:City) where toLower(c.name) = {city_name} and "
                    "c.country_code = {country_code} and toString(c.latitude) "
                    "starts with toString({city_lat}) and toString(c.longitude) "
                    "starts with toString({city_lon}) MATCH (u:User)  "
                    "where u.id = {current_user_id}")