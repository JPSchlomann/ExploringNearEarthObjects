"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""

from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, hazardous, diameter, name):
        """Create a new `NearEarthObject`.

        :param designation: The NEO’s primary designation.
        :param hazardous: Whether the NEO is potentially hazardous.
        :param diameter: The NEO’s diameter.
        :param name: The NEO’s IAU name.
        """

        self.designation = designation

        if hazardous.upper() == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        if diameter == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(diameter)

        if name == '':
            self.name = None
        else:
            self.name = name

        # empty initial collection of linked approaches.
        # NEO and approaches are linked in via class NEODatabase in database.py
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        else:
            return f"{self.designation}"

    def __str__(self):
        """produces a human-readable description of the contents of the object"""
        if self.hazardous:
            return f"{self.fullname} has a diameter of {self.diameter} km and is potentially hazardous."
        else:
            return f"{self.fullname} has a diameter of {self.diameter} km and is not potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, time, distance, velocity, designation):
        """Create a new `CloseApproach`.

        :param time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param distance: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param velocity: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        :param designation: The NEO’s primary designation before the Approach is linked to its NEO via class NEODatabase in database.py.
        """
        self._designation = designation
        self.time = cd_to_datetime(time) # TODO: Use the cd_to_datetime function for this attribute.
        self.distance = float(distance)
        self.velocity = float(velocity)

        # attribute for the referenced NEO, originally None.
        # NEO and approaches are linked in via class NEODatabase in database.py
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # formatted representation of the approach time.
        return datetime_to_str(self.time)

    def __str__(self):
        """produces a human-readable description of the contents of the object"""
        return f"On {self.time_str} {self._designation} approaches Earth at a distance of {self.distance} au and a velocity of {self.velocity} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
