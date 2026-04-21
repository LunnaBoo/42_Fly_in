from typing import Any
from src.Zone import Zone


class MapParser:
    """
    Class with all necessary methods for not only parsing
    data from an input .txt file but also validating it
    according to our program's rules.
    """
    valid_keys: list[str] = [
            "nb_drones", "start_hub", "end_hub",
            "hub", "connection"
            ]
    loaded_keys: list[str] = [
            "nb_drones", "start_hub", "end_hub",
            "hubs", "connections"
            ]

    @classmethod
    def load_data(cls, filename: str) -> dict[str, dict | str]:
        """
        Reads from input file and returns a dict with all
        extracted information organized.

        Parameters
        ----------
        filename: str
            String with the input file's filename

        Returns
        -------
        dict[str, dict | str]
            A dictionary with string keys and values that vary
            between dictionaries, for hubs and connections, and
            plain strings, for the rest of the data.
        """
        raw_data: dict[str, dict | str] = {}
        hubs: dict[str, str] = {}
        connections: dict[str, str] = {}
        with open(filename, "r") as file:
            for i, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    raise ValueError(f"Invalid format at line {i}:"
                                     " missing ':'.")

                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                
                if key not in cls.valid_keys:
                    raise ValueError(f"Invalid key at line {i}: '{key}'.")
                if key != "hub" and key != "connection":
                    if key in raw_data:
                        raise ValueError(f"Duplicate key found at line {i}: "
                                         f"'{key}'.")
                if not value:
                    raise ValueError(f"Empty value for key '{key}' "
                                     f"at line {i}.")
                if key == "hub":
                    split = value.split(" ", 1)
                    name = split[0]
                    value = split[1]
                    hubs[name] = value
                elif key == "connection":
                    split = value.split(" ", 1)
                    name = split[0]
                    if len(split) > 1:
                        value = split[1].split("=", 1)[1]
                        value = value.removesuffix("]")
                        connections[name] = value
                    else:
                        connections[name] = "1"
                else:
                    raw_data[key] = value
            raw_data["hubs"] = hubs
            raw_data["connections"] = connections
            for key in cls.loaded_keys:
                if key not in raw_data.keys():
                    raise ValueError(f"Missing key: '{key}'.")
        return raw_data

    @staticmethod
    def string_parser(key: str, value: str,
                      zone_type: str, color: str | None,
                      max_drones: int) -> Zone | int:
        """
        Helper method used in parse_data() method.
        Parses string values, such as end_hub, start_hub
        and nb_drones.

        Parameters
        ----------
        key: str
            Dictionary key
        value: str,
            Dictionary value
        zone_type: str
            Store zone_type in case of hubs
        color: str | None
            Stores zone color in case of hubs
        max_drones: int
            Stores max drones number in case of hubs

        Returns
        -------
        Zone | int
            Zone in case of hubs, int in case of
            nb_drones.
        """

        if key == "nb_drones":
            return int(value)
        else:
            is_start: bool = True
            is_end: bool = True
            if key == "start_hub":
                is_end = False
            else:
                is_start = False
            split = value.split(" ", 3)
            if len(split) > 3:
                name, x, y, metadata = split
            else:
                name, x, y = split
                metadata = None
            x = int(x)
            y = int(y)
            pos: tuple[int, int] = (x, y)
            if metadata:
                split = metadata.split()
                for item in split:
                    n_key, n_value = item.split("=", 1)
                    n_key = n_key.removeprefix("[")
                    n_value = n_value.removesuffix("]")
                    if n_key == "zone":
                        zone_type = n_value
                    elif n_key == "color":
                        color = n_value
                    elif n_key == "max_drones":
                        max_drones = int(n_value)
            zone: Zone = Zone(name=name, zone_type=zone_type,
                              pos=pos, is_start=is_start,
                              is_end=is_end, color=color,
                              max_drones=max_drones)
            return zone

    @staticmethod
    def dict_parser(key: str, n_key: str, value: dict, zone_type: str,
                    color:str | None,
                    max_drones: int) -> tuple[str, Zone] | tuple[str, int]:
        """
        Helper method used in parse_data() method.
        Parses dictionary values, specifically hubs and
        connections from input file.

        Parameters
        ----------
        key: str
            Key from outer dictionary. Ex.: "hubs", "connections"
        n_key: str
            Key from inner dictionary. It's the name of the Zone/hub.
        value: dict
            The inner dicionary itself.
        zone_type: str
            Stores zone_type in case of hubs
        color: str | None
            Stores zone color in case of hubs
        max_drones: int
            Stores maximum drones number in case of hubs.

        Returns
        -------
        tuple[str, int] | tuple[str, Zone]
            Extracted data. String will be used as key in the
            main method outside this function, and int | Zone
            will be the value. Int in case of connections and
            Zone in case of hubs.
        """
        if key == "hubs":
            name = n_key
            split = value[n_key].split(" ", 2)
            if len(split) > 2:
                x, y, metadata = split
            else:
                x, y = split
                metadata = None
            x = int(x)
            y = int(y)
            pos: tuple[int, int] = (x, y)
            if metadata:
                split = metadata.split()
                for item in split:
                    new_key, new_value = item.split("=", 1)
                    new_key = new_key.removeprefix("[")
                    new_value = new_value.removesuffix("]")
                    if new_key == "zone":
                        zone_type = new_value
                    elif new_key == "color":
                        color = new_value
                    elif new_key == "max_drones":
                        max_drones = int(new_value)
            zone: Zone = Zone(name=name, zone_type=zone_type,
                              pos=pos, color=color,
                              max_drones=max_drones)
            return (n_key, zone)
        elif key == "connections":
            name = n_key
            max_link_capacity = int(value[n_key])
            return (name, max_link_capacity)
        raise ValueError("MapParser ERROR: Something went wrong during parsing")

    @classmethod
    def parse_data(cls, 
                   raw_data: dict[str, dict | str]) -> dict[str, Any]:
        """
        Applies data types other than str to the values of
        the raw_data dictionary received by parameter.
        Also acts as validation.

        Parameters
        ----------
        raw_data: dict[str, dict | str]
            Output from load_data method

        Returns
        -------
        dict[str, Any]
            Parsed data.
        """

        parsed_data: dict[str, Any] = {}
        hub_dict = {}
        connection_dict = {}
        try:
            for key, value in raw_data.items():
                zone_type: str = "normal"
                color: str | None = None
                max_drones: int = 1 
                if isinstance(value, str):
                    parsed_data[key] = MapParser.string_parser(key, value,
                                                          zone_type,
                                                          color,
                                                          max_drones)
                if isinstance(value, dict):
                    try:
                        start_name = parsed_data["start_hub"].name
                        hub_dict[start_name] = parsed_data["start_hub"]
                    except Exception as e:
                        raise ValueError("MapParser ERROR in 'start_hub' key:", e)
                    for n_key in value:
                        res: tuple[str, int] | tuple[str, Zone] = (
                                MapParser.dict_parser(key, n_key, value,
                                                      zone_type, color,
                                                      max_drones)
                                )
                        name, n_value = res
                        if isinstance(n_value, int):
                            connection_dict[name] = n_value
                            parsed_data[key] = connection_dict
                        elif isinstance(n_value, Zone):
                            hub_dict[name] = n_value
                            parsed_data[key] = hub_dict
        except Exception as e:
            raise ValueError(f"MapParser ERROR in '{key}':", e)

        end_name = parsed_data["end_hub"].name
        hub_dict[end_name] = parsed_data["end_hub"]
        parsed_data["hubs"] = hub_dict
        parsed_data.pop("start_hub")
        parsed_data.pop("end_hub")
        return parsed_data

#    @classmethod
#    def link_connections_to_zones(
#            cls, parsed_data: dict[str, Any]
#            ) -> dict[str, Any]:
#        hubs: dict[str, Zone] = parsed_data["hubs"]
#        connections: dict[str, int] = parsed_data["connections"]
#        try:
#            for key in connections:
#                hub1, hub2 = key.split("-", 1)
#                max_link_capacity = connections[key]
#                zone1 = None
#                zone2 = None
#                for n_key in hubs:
#                    if n_key == hub1:
#                        zone1 = hubs[n_key]
#                    elif n_key == hub2:
#                        zone2 = hubs[n_key]
#                    if zone1 and zone2:
#                        break
#                if isinstance(zone1, Zone) and isinstance(zone2, Zone):
#                    connection = Connection(zone1, zone2, max_link_capacity)
#                    zone1.connections.append(connection)
#                    zone2.connections.append(connection)
#                else:
#                    raise Exception("Error during zone object instantiation")
#        except Exception as e:
#            raise ValueError(f"MapParser ERROR in '{key}':", e)
#        parsed_data["hubs"] = hubs
#        parsed_data["connections"] = connections
#        return parsed_data
