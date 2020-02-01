# ISTBot

## Workflow
Cada equipa deve trabalhar no seu branch. Quando um subprojecto estiver terminado será merged para a ```master branch```.
* Criar uma nova branch
```
git branch <new_branch_name>
```

* Mudar para a nova branch

```
git checkout <branch_name>
```

## Getting started
* Criar o vosso [bot](https://discordapp.com/developers/applications/).

* No ficheiro ```config.py``` vão encontrar o seguinte:
```
SECRET_KEY = "INSERT YOUR KEY HERE"

BOT_COGS = ["INSERT YOUR COG HERE"]
```
*  Adicionem o private token que foi gerado ao criarem o bot à variável ```SECRET_KEY```. Podem encontrar o token na secção ```Bot``` do vosso Developer Portal.
*  Adicionem o nome do ficheiro que contém a definição dos comandos ao array ```BOT_COGS```.
