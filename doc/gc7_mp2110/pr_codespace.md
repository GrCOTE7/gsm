# Mémo pour PR (En CLI) depuis un codespace de MP21170

## Avoir **gh** installé dans le codespace (Exprès non pérenne)

```bash
type -p curl >/dev/null || sudo apt install curl -y
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
```

## Fixer le repo destinataire du PR

```bash
gh repo set-default GrCOTE7/gsm
```

Et vérifier

```bash
gh repo set-default --view
```

## Valider le PR

```bash
gh pr create \
  --base main \
  --head MP21170:feat/doc-pr \
  --title "doc: ajout mineur dans 0110" \
  --body "Corrections de doc."
```
