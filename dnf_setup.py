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
        print ("Your are root, installing git and continuing on...")
        return False
    else:
        print ("This should be run as root, please change to root access and rerun.")
        return True

# Get the requirements file
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
# Install on my zsh and configure
def zsh():
    os.system("dnf install zsh -y")
    os.system("git clone https://github.com/ryanoasis/nerd-fonts.git")
    os.system("cd nerd-fonts && ./install.sh Noto")
    os.system("dnf install starship -y")
    os.system("cp ./zshrc ~/.zshrc && cp ./starship.toml ~/.config/starship.toml")
    # os.system("curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh")
    z_file = open("~/.zshrc", "a+")
    z_file.write("alias upy='sudo dnf update && sudo dnf upgrade -y && sudo dnf autoremove'\n")
    z_file.close()

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
    #install vim-plug
    os.system("curl -fLo ~/.vim/autoload/plug.vim --create-dirs \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    # copy .vimrc
    os.system("cp ./vimrc ~/.vimrc")
    #install vim plugins
    os.system("vim +PlugInstall +qall")

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
    # Install oh my zsh and modify .zshrc
    print ("Installing zsh...")
    zsh()
    print ("Setting up vim...")
    vim()
    print ("Installing docker...")
    docker()
    print ("Setting up kubernetes...")
    k8s()
    # Modify .vimrc
    # setup crontab
