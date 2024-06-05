---
title : "CLI sync for GitLab, GitHub, Codeberg" 
subtitle : "use gitlab and github together for same repository on one machine" 
showInHome : True
date : 2021-02-14
---

This article focuses on syncing GitLab, GitHub, and Codeberg directly from the command line using git pull or push commands. Unlike mirrored repositories, these repositories will remain independent of each other, eliminating the need for different remote names.

However, if you're interested in maintaining a mirrored copy of GitLab in GitHub or vice versa, GitHub provides a specific article for that purpose.

If your aim is to keep GitHub and GitLab repositories independent, follow these guidelines:


## 1. Adding SSH Keys to Your Local Machine (Optional Step)

While you can use the same keys for each Git source, I prefer using different keys for different sources. Generate unique SSH keys for Codeberg, GitLab, and GitHub:

    ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_codeberg
    ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_gitlab 
    ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_github

Add the public keys to Codeberg, GitLab, and GitHub:

* Add ~/.ssh/id_rsa_codeberg.pub to GitHub SSH keys.
* Add ~/.ssh/id_rsa_gitlab.pub to GitLab SSH keys.
* Add ~/.ssh/id_rsa_github.pub to GitHub SSH keys.

Register the keys on your local machine:

    ssh-add ~/.ssh/id_rsa_codeberg
    ssh-add ~/.ssh/id_rsa_github
    ssh-add ~/.ssh/id_rsa_gitlab

## 2. Editing ~/.ssh/config

Edit the ~/.ssh/config file with the following content:

    Host codeberg.org
        HostName codeberg.org
        User git
        IdentityFile ~/.ssh/id_rsa_codeberg
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_rsa_gitlab
    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_rsa_github

## 3. Configuring Repositories and Remotes

* Clone the original repository from GitLab/GitHub/Codeberg to your local machine:

    git clone git@github.com:username/repository_name.git

* Create a remote instance of the same:

    cd repository_name
    git remote set-url origin --add git@gitlab.com:username/repository_name.git
    git remote set-url origin --add git@codeberg.org:username/repository_name.git

## 4. Checking Remote Repositories

To check all the remotes for the repository, run:

    git remote -v

The command should return something like:

    origin  https://github.com/username/repository_name.git (fetch)
    origin  https://github.com/username/repository_name.git (push)
    origin  https://gitlab.com/username/repository_name.git (push)
    origin  https://codeberg.org/username/repository_name.git (push)


Now you can simply use git push, and it will push changes to all remotes.

