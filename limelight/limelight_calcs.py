from .limelight import Limelight
import math


def calc_distance(
    camera_angle: float, mount_height: float, target_height: float, limelight: Limelight
):
    """
    Calculate the distance from the camera to the wall the target is mounted on

    Args:
        camera_angle: The angle of the camera, either known or calculated from the calc_camera_angle method
        mount_height: The height that the camera is mounted off the floor
        target_height:The height the target is from the floor
        limelight: The limelight object to pull networktables values from

    Returns:
        Gives the distance (in the same units that were used for the input) away from the wall that has the target
    """
    d = (target_height - mount_height) / math.tan(
        math.radians(camera_angle + limelight.vertical_offset)
    )
    return d


def calc_camera_angle(
    x_distance: float, mount_height: float, target_height: float, limelight
):
    """
    Calculate the camera's mounted angle from known properties. Set the robot to a fixed
    distance away from the target and pass in the other properties and it will calculate
    the angle to put into the calc_distance function

    Args:
        x_distance: The known distance away from the wall the target is on
        mount_height: The height that the camera is mounted off the floor
        target_height: The height the target is from the floor
        limelight: The limelight object to pull networktables values from

    Returns:
        Gives the angle (in degrees) that the camera is mounted at
    """
    a1 = -limelight.vertical_offset + math.degrees(
        math.atan((target_height - mount_height) / x_distance)
    )
    return a1
