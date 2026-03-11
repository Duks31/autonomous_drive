from setuptools import setup
import os
from glob import glob

package_name = "autonomous_drive"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*")),
        (os.path.join("share", package_name, "meshes"), glob("meshes/*")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Chidubem Ndukwe",
    maintainer_email="chidubemjan31@gmail.com",
    description="The " + package_name + " package",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "keyboard_controller = autonomous_drive.keyboard_controller:main",
            "script_controller = autonomous_drive.script_controller:main",
            "cmd_vel_relay = autonomous_drive.cmd_vel_relay:main",
            "gamepad_controller = autonomous_drive.gamepad_controller:main",
        ],
    },
)
