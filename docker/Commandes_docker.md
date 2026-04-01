# Commandes Docker
## Créer et lancer un conteneur

'''invite de commandes
docker run <nom de l'image>
'''
## lister des conteneurs 
'''invite de commandes
docker ps 
docker container ps
'''
## Lister tous les conteneurs
'''invite de commandes
docker ps -a
docker container ps -a
'''
## Lister les images 
'''invite de commandes
docker image ls
docker images
'''
## Supprimer un ou des conteneurs
'''invite de commande
docker rm <id du conteneur>
docker container rm <id du conteneur>
'''
## Supprimer un image
'''invite de commande
docker image rm <id de conteneur>
docker rmi <id de l'image>
'''
## Construire une image personnalisée avec dockerfile
'''terminal vscode
docker build -t <nom de l'image> .
docker construit -t nom de l'image suivi d'un chemin de l'image
'''

## Dokerfile
### Construire une image
''' invite des commandes
docker build -t <image> .
'''
### Ajouter l'image au Dockerhub
'''invite des commandes
docker tag <image><repository>
docker push <reposotory>
'''

