__all__ = ["Limelight", "LEDState", "CamMode", "StreamMode", "SnapshotMode"]

from networktables import NetworkTables
from enum import Enum
import typing
from typing import Tuple

class LEDState(Enum):
    MATCH_PIPELINE = 0
    OFF = 1
    BLINK = 2
    ON = 3

class CamMode(Enum):
    PROCESSED = 0
    DRIVER = 1

class StreamMode(Enum):
    STANDARD = 0
    PIP_MAIN = 1
    PIP_SECONDARY = 2

class SnapshotMode(Enum):
    NONE = 0
    TAKE_2_PS = 1

class Limelight:
    _enabled = 1
    _light = 1
    _stream_mode = 0
    _snapshots = 0
    __nt = None
    _active_pipeline = 0

    def __init__(self, camera=False, light=False):
        NetworkTables.initialize()
        __nt = NetworkTables.getTable("limelight")
        self._enabled = camera
        self._light = light



    # @property
    # def raw_screenspace_x(self):
    #     self.__nt.getNumber('tx0')
    # @property
    # def raw_screenspace_y(self):
    #     self.__nt.getNumber('ty0')
    # @property
    # def area(self):
    #     self.__nt.getNumber('ta0')
    # @property
    # def skew_rot(self):
    #     self.__nt.getNumber('ts0')
    # @property
    # def tx1(self):
    #     self.__nt.getNumber('tx1')
    # @property
    # def ty1(self):
    #     self.__nt.getNumber('ty1')
    # @property
    # def ta1(self):
    #     self.__nt.getNumber('ta1')
    # @property
    # def ts1(self):
    #     self.__nt.getNumber('ts1')
    # @property
    # def tx2(self):
    #     self.__nt.getNumber('tx2')
    # @property
    # def ty2(self):
    #     self.__nt.getNumber('ty2')
    # @property
    # def ta2(self):
    #     self.__nt.getNumber('ta2')
    # @property
    # def ts2(self):
    #     self.__nt.getNumber('ts2')

    @property
    def valid_targets(self) -> bool:
        return self.__nt.getNumber("tv")

    @property
    def horizontal_offset(self) -> float:
        return self.__nt.getNumber("tx")

    @property
    def vertical_offset(self) -> float:
        return self.__nt.getNumber("ty")

    @property
    def target_area(self) -> float:
        return self.__nt.getNumber("ta")
    
    @property
    def skew(self) -> float:
        return self.__nt.getNumber("ts")
    
    @property
    def latency(self) -> float:
        return self.__nt.getNumber("tl")
    
    @property
    def bb_short(self) -> float:
        return self.__nt.getNumber("tshort")
    
    @property
    def bb_long(self) -> float:
        return self.__nt.getNumber("tlong")
    
    @property
    def bb_horizontal(self) -> float:
        return self.__nt.getNumber("thor")
    
    @property
    def bb_vertical(self) -> float:
        return self.__nt.getNumber("tvert")
    
    @property
    def bb(self) -> Tuple[float, float]:
        return (self.bb_horizontal, self.bb_vertical)

    @property
    def crosshair_ax(self):
        """
        Get crosshair A's X position
        """
        return self.__nt.getNumber('cx0')
    @property
    def crosshair_ay(self):
        """
        Get crosshair A's Y position
        """
        return self.__nt.getNumber('cy0')
    @property
    def crosshair_bx(self):
        """
        Get crosshair B's X position
        """
        return self.__nt.getNumber('cx1')
    @property
    def crosshair_by(self):
        """
        Get crosshair B's Y position
        """
        return self.__nt.getNumber('cy1')

    def camera(self, camMode: CamMode) -> None:
        """
        Set the camera mode. You can set this to be driver operated or to run on a pipeline.

        :param camMode: The camera mode to set
        """
        self._enabled = camMode
        self.__nt.putNumber("camMode", camMode)
        
    def light(self, status: LEDState) -> None:
        """
        Set the status of the limelight lights

        :param status: The status to set the light to
        """
        self._light = status
        self.__nt.putNumber("ledMode", status)
    
    def pipeline(self, pipeline):
        """
        Sets the currently active pipeline

        :param pipeline: The pipeline id to set to be active
        """
        self._active_pipeline = 0
        self.__nt.putNumber("pipeline", pipeline)
    
    def snapshot(self, snapshotMode: SnapshotMode):
        """
        Allow users to take snapshots during a match

        :param snapshotMode: The state to put the camera in
        """
        self._snapshots = snapshotMode
        self.__nt.putNumber("snapshot", snapshotMode)

