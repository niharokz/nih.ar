---
title : "One Git with Multiple Remotes" 
subtitle : "use gitlab and github together for same repository on one machine" 
showInHome : True
date : 2021-02-14
---

This article is about how to sync Gitlab, Github and Codeberg directly from the command line using git pull or push commands. Unlike mirror repositories, these repositories will be independent of each other. We also don't need different remote names for these repositories.

But if you want to keep a mirror copy of Gitlab in Github or vice-versa, [this article from Github](https://docs.gitlab.com/ee/user/project/repository/repository_mirroring.html) is for you.

If you want to keep github and gitlab repositories independent, then follow the below guidelines.

## Adding SSH-keys to your local machine. [optional step]

We can use same keys for each git source. But I like to use different keys for different sources.
 
Generate unique SSH keys for Codeberg, Gitlab and Github.
	
	ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_codeberg
	ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_gitlab 
	ssh-keygen -t rsa -C "some@mail.com" -f ~/.ssh/id_rsa_github

Add public keys to Codeberg, Gitlab and Github.

	Add ~/.ssh/id_rsa_codeberg.pub to GitHub SSH-keys.
	Add ~/.ssh/id_rsa_gitlab.pub to GitLab SSH-keys.
	Add ~/.ssh/id_rsa_github.pub to GitHub SSH-keys.

Register the keys in your local machine

	ssh-add ~/.ssh/id_rsa_codeberg
	ssh-add ~/.ssh/id_rsa_github
	ssh-add ~/.ssh/id_rsa_gitlab

Edit ~/.ssh/config  with below content

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


## Configure repositories and remotes

Clone the original repository from Gitlab/Github/Codeberg to your local machine

	git clone git@github.com:username/repository_name.git

Create a remote instance of the same

	cd repository_name
	git remote set-url origin --add git@gitlab.com:username/repository_name.git
	git remote set-url origin --add git@codeberg.org:username/repository_name.git

To check all the remote for the repository, run the below

	git remote -v

The command should return something like 

	origin	https://github.com/username/repository_name.git (fetch)
	origin	https://github.com/username/repository_name.git (push)
	origin	https://gitlab.com/username/repository_name.git (push)
	origin	https://codeberg.org/username/repository_name.git (push)

Now you can just use git push and it will push on all remote.
