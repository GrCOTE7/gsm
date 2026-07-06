# Server

## Ajout d'un DMN (ou sub-dmn)

### Installer les containers

1 - Dossier comme 

```bash
sudo mkdir /opt/gsm
sudo chown ubuntu:ubuntu /opt/gsm
```

2 - Copier ton projet GSM dans /opt/gsm

```bash
z/deploy
```

qui exécutera :

```bash
scp -r C:/gsm ubuntu@137.74.118.122:/opt/gsm/
OU si on est sûr d'être dans C:/gsm
scp -r C:/gsm ubuntu@137.74.118.122:/opt/gsm/
```

Si erreur, et pour tout effacer dans le dossier :

```bash
rm -rf /opt/gsm/*
rm -rf /opt/gsm/.*
```

### Gérer la redir du dmn

1 -  Trouver le caddyfile utilisé

```bash
docker inspect vps_caddy | grep Source
```

exemple avec:

"Source": "/opt/pyproject_template/deploy/proxy/Caddyfile",
...

2 - Éditer le fichier

```bash
nano /opt/pyproject_template/deploy/proxy/Caddyfile
```

Y ajouter le bloc :

```bash
gsm.cote7.com {
    reverse_proxy localhost:8000
}
```

Vérification "locale" :

```bash
curl http://localhost:7777
```

### Lancer le container Docker

```bash
cd /opt/gsm
docker compose -f docker-compose.prod.yml up -d --build
```

Pour arrêter

```bash
docker compose -f docker-compose.prod.yml down 
```

docker inspect vps_caddy | grep Source

ls -l /opt/pyproject_template/deploy/proxy


 docker restart vps_caddy