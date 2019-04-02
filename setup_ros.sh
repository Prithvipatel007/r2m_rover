#!/bin/bash
#author : Prithvi Patel
#Company : R2M Team

#Simple setup_ros.sh for configuring Ubuntu based workstation

# this was ripped out of bashlib
confirm() {
  # call with a prompt string or use a default
  read -r -p "${1:- Are you sure? [y/N]} " response
  case $response in
    [yY][eE][sS] | [yY])
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# update pkgs
sudo apt-get update

# main apps
sudo apt-get install -y vim vim-nox ctags xournal meld rdesktop terminator geany python3

# system utilities
sudo apt-get install -y screen sshfs autofs curl git subversion sqlite3

# build utilities
sudo apt-get install -y build-essential g++ automake autoconf cmake


# ros install steps

# 1.2 sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list'

# 1.3 keys
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

# 1.4 installation
sudo apt-get update
# Desktop-Full Install: (Recommended) :
#
# ROS, rqt, rviz, robot-generic libraries,
# 2D/3D simulators, navigation and 2D/3D perception
sudo apt-get install -y ros-kinetic-desktop-full

# ALTERNATIVELY:

# Desktop Install:
#
# ROS, rqt, rviz, and robot-generic libraries
#sudo apt-get install -y ros-kinetic-desktop

# ROS-Base:
#
# (Bare Bones) ROS package, build, and communication libraries.
# No GUI tools.
#sudo apt-get install -y ros-kinetic-ros-base

# Individual Package:
#
# You can also install a specific ROS package
#(replace underscores with dashes of the package name):
#sudo apt-get install ros-kinetic-PACKAGE
# e.g. sudo apt-get install -y ros-kinetic-slam-gmapping

# To find available packages, use:
#apt-cache search ros-kinetic

# 1.5 Init rosdep
sudo rosdep init
rosdep update

# git clone and install master dotfiles (will inject stuff into them)
./install_dotfiles.sh

# 1.6 ENV setup
echo -e "\n# ROS environment setup" >> ~/.bashrc_custom
echo ". /opt/ros/kinetic/setup.bash" >> ~/.bashrc_custom
. ~/.bashrc

# 1.7 Getting rosinstall
sudo apt-get install -y python-rosinstall

# Extra steps learned from youtube
sudo apt-get install -y python-catkin-tools

# we've finished installing the main ROS stuff
echo -e "\nCompleted main install of ROS!\n"

# add user to dialout for USB serial comms (arduino / etc)
sudo usermod -aG dialout $USER

# ask if user would like additional stuff for tutorials
if confirm "Would you like to install additional pkgs for tutorials? [y/N]"
then
  sudo apt-get install -y linux-headers-generic
  sudo sh -c 'echo "deb-src http://us.archive.ubuntu.com/ubuntu/ xenial main restricted
deb-src http://us.archive.ubuntu.com/ubuntu/ xenial-updates main restricted
deb-src http://us.archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu xenial-security main restricted" > \
    /etc/apt/sources.list.d/official-source-repositories.list'
  sudo apt-get update
  sudo apt-get install -y ros-kinetic-librealsense
  sudo apt-get install -y ros-kinetic-librealsense-camera
  sudo apt-get install -y \
    ros-kinetic-turtlebot \
    ros-indigo-turtlebot-apps \
    ros-indigo-turtlebot-interactions \
    ros-indigo-turtlebot-simulator \
    ros-indigo-kobuki-ftdi \
    ros-indigo-ar-track-alvar-msgs
    # ros-indigo-rocon-remocon \ -- THIS ONE NOT AVAILABLE in KINETIC!?
    # ros-indigo-rocon-qt-library \ -- THIS ONE NOT AVAILABLE in KINETIC!?
  sudo apt-get install -y arduino
fi

#Gazebo_ROS control 

sudo apt-get install ros-kinetic-ros-control ros-kinetic-ros-controllers

# done message
echo -e "\nDone running setup!"
