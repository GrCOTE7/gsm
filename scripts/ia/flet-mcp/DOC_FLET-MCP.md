# Flet-MCP

Permet à l'IA de s'appuyer sur l'API Flet pour fournir une documentation fidèle à la version installée.

Accessible dans l'assistant (DSH, etc.) et Copilot-chat
(Pas pour auto-complétion qui reste légère exprès, sans agents extérieurs)

## Install

* Global, pour tous les projets Flet, dans un env dédié

```bash
uv tool install flet-mcp
```


* Dans la config MCP VSCode

### Install globale (Sera compétent pour tous les projets)

    * Pour l'ouvrir facilement : Ctrl+Shift+P
    → taper MCP: Open User Configuration

```json
{
  "servers": {
    "flet-mcp": {
      "type": "stdio",
      "command": "flet",
      "args": ["mcp"]
    }
  }
}
```

DSH a corrigé

```json
{
  "servers": {
    "flet-mcp": {
      "type": "stdio",
      "command": "C:\\Users\\utilisateur\\AppData\\Roaming\\uv\\tools\\flet\\Scripts\\flet.exe",
      "args": ["mcp", "--transport", "stdio"],
      "env": {
        "FASTMCP_SHOW_SERVER_BANNER": "false",
        "FASTMCP_LOG_LEVEL": "WARNING"
      }
    }
  }
}
```

→ Le code sera dans (Windows) : %APPDATA%\Code\User\mcp.json

### local, projet GSM uniquement

même code dans .vscode/mcp.json à la racine du projet

---

Pour DSH, ajout dans C:\Users\utilisateur\.dsh\profiles\web\cordis.patch.yml de :

```yaml
# Your patch layer for this dsh profile, applied after every bundle layer:
# a top-level YAML array of loader patch entries (id-targeted config
# overrides, disables, and insert lists; `!!js` expressions allowed).
# MCP Flet (flet-mcp) — même serveur que celui utilisé par VS Code.
# Outils exposés au modèle : mcp__flet__get_api, mcp__flet__find_icon, ...
- insert:
    - id: mcp-flet
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: flet
        transport: stdio
        command: 'C:\Users\utilisateur\AppData\Roaming\uv\tools\flet\Scripts\flet.exe'
        args:
          - mcp
          - --transport
          - stdio
        env:
          FASTMCP_SHOW_SERVER_BANNER: 'false'
          FASTMCP_LOG_LEVEL: WARNING
```

et dans C:/Users/utilisateur/.dsh/mcp-flet.cordis.yml

```yaml
# MCP Flet pour DSH — même serveur que celui utilisé par VS Code.
# Usage ponctuel : dsh web --patch C:\Users\utilisateur\.dsh\mcp-flet.cordis.yml
# Usage permanent : fusionner le bloc `insert` ci-dessous dans
#   $DSH_HOME\profiles\<profil>\cordis.patch.yml  (un profil)
#   $DSH_HOME\cordis.patch.yml                    (tous les profils)
# Outils exposés au modèle : mcp__flet__get_api, mcp__flet__find_icon, ...
- insert:
    - id: mcp-flet
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: flet
        transport: stdio
        command: 'C:\Users\utilisateur\AppData\Roaming\uv\tools\flet\Scripts\flet.exe'
        args:
          - mcp
          - --transport
          - stdio
        env:
          FASTMCP_SHOW_SERVER_BANNER: 'false'
          FASTMCP_LOG_LEVEL: WARNING
```


Vérifier l'install

```bash

# Pour DSH
pnpm -C C:\ai\dsh dsh web --dump-config

```
