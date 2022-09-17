#!/usr/bin/python3

# Owen Watkins
# Script to set up a bare debian based linux environment how I want
# Initial develop on 1/18/2020

import os
from os import path

reqs = [] # Array to hold individual requirements

# Will use boolean input many times
def is_true(inp):
    if (inp.lower() != "y" and inp != ""):
        return False
    else:
        return True
# Ensuring root here will allow the script to run through
def check_if_root():
    is_root = input("Are you in root? [Y/n]")
    if (is_true(is_root)):
        print ("Your are root, continuing on...")
        return False
    else:
        print ("This should be run as root, please change to root access and rerun.")
        return True

# # Get the requirements file
def get_reqs():
    with open("requirements.txt", "r+") as reqs_file:
        r_lines = reqs_file.readlines()
        for r in r_lines:
            reqs.append(r)
        for rq in reqs:
            try:
                os.system(f"dnf install {rq} -y")
            except OSError:
                print (f"{rq} did NOT install")

# Install rpmfusion
def rpmfusion():
    os.system("dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm -y")
    os.system("dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y")

# Install media codecs
def media():
    os.system("dnf install gstreamer1-plugins-bad-free gstreamer1-plugins-bad-freeworld gstreamer1-plugins-ugly gstreamer1-plugins-ugly-free gstreamer1-plugins-ugly-freeworld gstreamer1-plugins-bad-free-extras gstreamer1-plugins-bad-freeworld-extras gstreamer1-plugins-ugly-extras gstreamer1-plugins-ugly-free-extras gstreamer1-plugins-ugly-freeworld-extras gstreamer1-plugins-good-extras gstreamer1-plugins-good gstreamer1-plugins-good-free-extras gstreamer1-plugins-good-extras gstreamer1-plugins-good-free gstreamer1-plugins-good-freeworld gstreamer1-plugins-good-freeworld-extras gstreamer1-plugins-base-tools gstreamer1-plugins-base gstreamer1-plugins-base-extras gstreamer1-plugins-base-free gstreamer1-plugins-base-free-extras gstreamer1-plugins-base-freeworld gstreamer1-plugins-base-freeworld-extras gstreamer1-libav gstreamer1 -y")

# Prepare for brave-browser
def brave():
    os.system("dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/")
    os.system("rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc")

# Install on my zsh and configure
def zsh():
    os.system("dnf install zsh -y")
    os.system("git clone https://github.com/ryanoasis/nerd-fonts.git")
    os.system("cd nerd-fonts && ./install.sh Noto")
    os.system("dnf install starship -y")
    os.system("cp ./zshrc ~/.zshrc && cp ./starship.toml ~/.config/starship.toml")
    z_file = open("~/.zshrc", "a+")
    z_file.write("alias upy='sudo dnf update && sudo dnf upgrade -y && sudo dnf autoremove'\n")
    z_file.close()

#install Golang
def golang():
    os.system("dnf install golang -y")

#install rust
def rust():
    os.system("dnf install rust -y")

#install nodejs
def nodejs():
    os.system("dnf install nodejs -y")

#install npm
def npm():
    os.system("dnf install npm -y")

#install yarn
def yarn():
    os.system("dnf install yarn -y")

#Install docker
def docker():
    os.system("dnf config-manager --add-repo=https://download.docker.com/linux/fedora/docker-ce.repo")
    os.system("dnf install docker-ce --nobest -y")
    os.system("systemctl start docker")
    os.system("systemctl enable docker")
    os.system("usermod -aG docker $USER")

# Install kubernetes
def k8s():
    os.system("dnf install kubectl -y")
    os.system("dnf install kubeadm -y")
    os.system("dnf install kubelet -y")
    os.system("dnf install kubernetes-cni -y")
    os.system("dnf install kubernetes-client -y")
    os.system("dnf install kubernetes-node -y")
    os.system("dnf install kubernetes-master -y")
    os.system("dnf install kubernetes -y")

#Setup vim
def vim():
    os.system("dnf install vim -y")
    #install vim-plug
    os.system("curl -fLo ~/.vim/autoload/plug.vim --create-dirs \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    # copy .vimrc
    os.system("cp ./vimrc ~/.vimrc")
    #install vim plugins
    os.system("vim +PlugInstall +qall")

# Install VS-CODE
def vscode():
    os.system("dnf install code -y")

# main program
def main():
    # Check if root
    check_if_root()
    # do update and upgrade
    os.system("dnf update && dnf upgrade -y")
    print ("Installing git...")
    os.system("dnf install git -y")
    # some base applications
    print ("Installing curl...")
    os.system("dnf install curl -y")
    # check if there is a requirements file
    print ("Checking for requirements.txt file...")
    f = path.exists("requirements.txt")
    # Do dnf installs from reqs doc
    if (f):
        print ("Requirements file found, installing apps...")
        get_reqs()
    print("Installing rpmfusion...")
    rpmfusion()
    print("Installing media codecs...")
    media()
    print("Installing brave-browser...")
    brave()
    print ("Installing zsh...")
    zsh()
    print ("Installing golang...")
    golang()
    print ("Installing rust...")
    rust()
    print ("Installing nodejs...")
    nodejs()
    print ("Installing npm...")
    npm()
    print ("Installing yarn...")
    yarn()
    print ("Setting up vim...")
    vim()
    print ("Installing docker...")
    docker()
    print ("Setting up kubernetes...")
    k8s()
    print ("Installing VS-CODE...")
    vscode()
    print ("Done!")
    # setup crontab
