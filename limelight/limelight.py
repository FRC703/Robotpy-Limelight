from networktables import NetworkTables
from enum import Enum
import typing
from typing import Tuple


class LEDState(Enum):
    """
    |LEDState|Sets limelight's LED state|
    |-|-|
    |0|use the LED Mode set in the current pipeline|
    |1|force off|
    |2|force blink|
    |3|force on|
    """
    MATCH_PIPELINE = 0
    OFF = 1
    BLINK = 2
    ON = 3


class CamMode(Enum):
    """
    |CamMode|Sets limelight's operation mode|
    |-|-|
    |PROCESSED|Vision processor|
    |DRIVER|Driver camera (increases exposure, disables vision processing)|
    """
    PROCESSED = 0
    DRIVER = 1


class StreamMode(Enum):
    """
    |StreamMode|Sets limelight's streaming mode|
    |-|-|
    |0|Standard - Side-by-side streams if a webcam is attached to Limelight|
    |1|PiP Main - The secondary camera stream is placed in the lower-right corner of the primary camera stream|
    |2|PiP Secondary - The primary camera stream is placed in the lower-right corner of the secondary camera stream|
    """
    STANDARD = 0
    PIP_MAIN = 1
    PIP_SECONDARY = 2


class SnapshotMode(Enum):
    """
    |SnapshotMode|Allows users to take snapshots during a match|
    |-|-|
    |0|Stop taking snapshots|
    |1|Take two snapshots per second|
    """
    NONE = 0
    TAKE_2_PS = 1


class Limelight:
    _enabled = 1
    _light = LEDState.OFF
    _stream_mode = 0
    _snapshots = 0
    __nt = None
    _active_pipeline = 0

    def __init__(self, nt=None, camera=False, light=False):
        """
        Creates an instance of a limelight

        Args:
            nt: Pass in a custom networktables table if your limelight is running
                on a table other than `limelight`

            camera: Processed pipeline or driver control mode.

            light: Default state of the light to set when camera is connected to the code
        """
        if nt:
            self.__nt = nt
        else:
            self.__nt = NetworkTables.getTable("limelight")
        self._enabled = camera
        self._light = light

    @property
    def valid_targets(self) -> bool:
        """
        Whether the camera has found a valid target

        Returns:
            Any valid targets?
        """
        return bool(self.__nt.getNumber("tv"))

    @property
    def horizontal_offset(self) -> float:
        """
        Gives the horizontal offset from the crosshair to the target
        LL1: -27° - 27°
        LL2: -29.8° - 29.8°

        Returns:
            The horizontal offest from the crosshair to the target.

        """
        return self.__nt.getNumber("tx")

    @property
    def vertical_offset(self) -> float:
        """
        Gives the vertical offset from the crosshair to the target
        LL1: -20.5° - 20.5°
        LL2: -24.85° - 24.85°

        Returns:
            The vertical offset from the crosshair to the target
        """
        return self.__nt.getNumber("ty")

    @property
    def target_area(self) -> float:
        """
        How much of the image is being filled by the target

        Returns:
            0% - 100% of image
        """
        return self.__nt.getNumber("ta")

    @property
    def skew(self) -> float:
        """
        How much the target is skewed

        Returns:
            -90° - 0°
        """
        return self.__nt.getNumber("ts")

    @property
    def latency(self) -> float:
        """
        How much the pipeline contributes to the latency. Adds at least 11ms for image capture

        Returns:
            Latency contribution
        """
        return self.__nt.getNumber("tl")

    @property
    def bb_short(self) -> float:
        """
        Sidelength of the shortest side of the fitted bouding box (pixels)

        Returns:
            Shortest sidelength
        """
        return self.__nt.getNumber("tshort")

    @property
    def bb_long(self) -> float:
        """
        Sidelength of the longest side of the fitted bouding box (pixels)

        Returns:
            Longest sidelength
        """
        return self.__nt.getNumber("tlong")

    @property
    def bb_horizontal(self) -> float:
        """
        Horizontal sidelength of the rough bounding box (0 - 320 px)

        Returns:
            The horizontal sidelength
        """
        return self.__nt.getNumber("thor")

    @property
    def bb_vertical(self) -> float:
        """
        Vertical sidelength of the rough bounding box (0 - 320 px)

        Returns:
            The vertical sidelength
        """
        return self.__nt.getNumber("tvert")

    @property
    def bounding_box(self) -> Tuple[float, float]:
        return (self.bb_horizontal, self.bb_vertical)

    def camtran(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """
        Results of a 3D solution position, 6 numbers: Translation(x,y,z) Rotation(pitch, yaw, roll)
        Honestly I have no clue what this does yet without some testing.
        """
        return self.__nt.getNumber("camtran")

    @property
    def crosshair_ax(self) -> float:
        """
        Get crosshair A's X position
        """
        return self.__nt.getNumber("cx0")

    @property
    def crosshair_ay(self) -> float:
        """
        Get crosshair A's Y position
        """
        return self.__nt.getNumber("cy0")

    @property
    def crosshair_bx(self) -> float:
        """
        Get crosshair B's X position
        """
        return self.__nt.getNumber("cx1")

    @property
    def crosshair_by(self) -> float:
        """
        Get crosshair B's Y position
        """
        return self.__nt.getNumber("cy1")

    def camera(self, camMode: CamMode) -> None:
        """
        Set the camera mode. You can set this to be driver operated or to run on a pipeline.

        Args:
            camMode: The camera mode to set
        """
        self._enabled = camMode
        self.__nt.putNumber("camMode", camMode.value)

    def light(self, status: LEDState) -> None:
        """
        Set the status of the limelight lights

        Args:
            status: The status to set the light to
        """
        self._light = status
        self.__nt.putNumber("ledMode", status.value)

    def pipeline(self, pipeline: int):
        """
        Sets the currently active pipeline

        Args:
            pipeline: The pipeline id to set to be active
        """
        self._active_pipeline = 0
        self.__nt.putNumber("pipeline", pipeline)

    def snapshot(self, snapshotMode: SnapshotMode):
        """
        Allow users to take snapshots during a match

        Args:
            snapshotMode: The state to put the camera in
        """
        self._snapshots = snapshotMode
        self.__nt.putNumber("snapshot", snapshotMode.value)
