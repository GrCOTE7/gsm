# Dossier local du projet
$local = "C:\gsm"

# Dossier distant sur le VPS
$remote = "ubuntu@137.74.118.122:/opt/gsm"

# Liste des éléments à copier
$items = @(
    "src",
    "docker-compose.prod.yml",
    "Dockerfile.prod",
    "Caddyfile",
    "pyproject.toml",
    ".env",
    "uv.lock"
)

# Copie propre
foreach ($item in $items) {
    scp -r "$local\$item" $remote
}
