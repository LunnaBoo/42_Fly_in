from typing import Any
from src.GraphLogic import Zone, Connection


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

    @classmethod
    def parse_data(cls, filename: str) -> dict[str, Any]:
        data: dict[str, Any] = {}
        with open(filename, "r") as file:
            for i, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    raise ValueError(f"ERROR: Invalid formatting in map file at line {i}.")
                if "nb_drones" not in data and "nb_drones" not in line:
                    raise ValueError("ERROR: In the map file nb_drones must be "
                                     "defined in the first line after empty or "
                                     "comment lines.")
                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip()

                if key not in cls.valid_keys:
                    raise ValueError(f"ERROR: Invalid key in map file at line {i}.")
                if key != "hub" and key != "connection":
                    if key in data:
                        raise ValueError(f"ERROR: Duplicate key in map file at line {i}.")
                if not value:
                    raise ValueError(f"ERROR: Empty value in map file at line {i}.")
                if key == "nb_drones":
                    try:
                        data["nb_drones"] = MapParser.__parse_nb_drones(value)
                    except Exception:
                        raise ValueError(f"ERROR: Invalid value in map file at line {i}."
                                         "Only positive numbers are allowed for nb_drones.")
                elif key == "hub":
                    try:
                        data["hub"] = MapParser.__parse_hub(key, value)
                    except Exception:
                        raise ValueError("ERROR: Invalid hub in map file "
                                         f"at line {i}.")
                elif key == "start_hub":
                    try:
                        data["start_hub"] = MapParser.__parse_hub(key, value)
                    except Exception:
                        raise ValueError("ERROR: Invalid start_hub in map file "
                                         f"at line {i}.")
                elif key == "end_hub":
                    try:
                        data["end_hub"] = MapParser.__parse_hub(key, value)
                    except Exception:
                        raise ValueError("ERROR: Invalid end_hub in map file "
                                         f"at line {i}.")
                elif key == "connection":
                    try:
                        data["connection"] = MapParser.__parse_connection(value,
                                                                          data["hub"])
                    except Exception:
                        raise ValueError("ERROR: Invalid connection in map file "
                                         f"at line {i}.")
                else:
                    raise ValueError(f"ERROR: Unknown key in map file at line {i}")
        return MapParser.__validate(data)

    @staticmethod
    def __parse_nb_drones(value: str) -> int:
        try:
            parsed_value: int = int(value)
            if parsed_value < 0:
                raise Exception
        except Exception:
            raise ValueError()
        return parsed_value

    @staticmethod
    def __parse_hub(key: str, value: str) -> Zone:
        try:
            split = value.split(" ", 3)
            if len(split) > 3:
                name, x, y, metadata = split
            else:
                name, x, y = split
                metadata = None
            x = int(x)
            y = int(y)
            pos: tuple[int, int] = (y, x)
            zone_type: str = "normal"
            color: str | None = None
            max_drones: int = 1
            is_start: bool = False
            is_end: bool = False
            if key == "start_hub":
                is_start = True
            elif key == "end_hub":
                is_end = True
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
                    else:
                        raise ValueError("ERROR: Unsupported metadata in map file.")
            zone = Zone(name=name, zone_type=zone_type, pos=pos,
                        color=color, max_drones=max_drones,
                        is_start=is_start, is_end=is_end)
        except Exception:
            raise ValueError()
        return zone

    @staticmethod
    def __parse_connection(value: str, hub: Zone) -> Connection:
        try:
            max_link: int = 1
            next_zone = None
            prev_zone = None
            zone_list = hub._all_zones
            split = value.split(" ", 1)
            name = split[0]
            if len(split) > 1:
                metadata = split[1]
            else:
                metadata = None
            zone_names = name.split("-", 1)
            for item in zone_list:
                if item.name == zone_names[0]:
                    prev_zone = item
                elif item.name == zone_names[1]:
                    next_zone = item
            if metadata:
                metadata = metadata.removeprefix("[")
                metadata = metadata.removesuffix("]")
                split = metadata.split("=", 1)
                max_link = int(split[1])
            connection = Connection(name, prev_zone, next_zone, max_link)
        except Exception:
            raise ValueError()
        return connection

    @staticmethod
    def __validate(data: dict[str, Any]) -> dict[str, Any]:
        zone_list = data["hub"]._all_zones
        connection_list = data["connection"]._all_connections
        name_list = []
        for item in zone_list:
            if item.name in name_list:
                raise ValueError("ERROR: Hubs with identical names in map file.")
            if "-" in item.name or " " in item.name:
                raise ValueError("ERROR: Invalid hub name in map file")
            name_list.append(item.name)
        name_list.clear()
        for item in connection_list:
            if item.name in name_list:
                raise ValueError("ERROR: Duplicate connections in map file.")
            name_list.append(item.name)
        # Missing validation for duplicate a-b b-a
        return data
