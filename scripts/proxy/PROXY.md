
# IA DeepSeek - API

## EXTENSION VSC Cline + DeepSeek

Intérêt du proxy (qui désactive le Thinking)

| Modèle              | Gain estimé avec proxy (sur tokens de sortie) |
| ------------------- | --------------------------------------------- |
| `deepseek-v4-flash` | 30 % à 55 %                                   |
| `deepseek-v4-pro`   | 30 % à 55 % *(identique)*                     |

### API Provider : DeepSeek

Simple, mais à ce jour, pas de toggle pour Thinking.

### API Provider : OpenAI Compatible

Permet d'activer et d'utiliser le proxy pour désactiver le 'Thinking'.

```bash
npm init -y
npm install express node-fetch cors
node proxy.js
```

### Fonctionnement du proxy

Le proxy est un petit serveur Express (`proxy.js` à la racine `C:\gsm\`) qui se place
entre Cline (ou tout client OpenAI-compatible) et l'API DeepSeek. Son rôle est de
**désactiver le mode 'Thinking'** sur chaque requête, ce que Cline ne permet pas
nativement avec le provider natif « DeepSeek ».

1. **Démarrage** : le proxy écoute sur `http://localhost:3000`.
   ```bash
   node proxy.js
   ```

2. **Endpoints exposés** :
   - `GET /v1/models` → fournit les métadonnées + prix des modèles (pour la config Cline).
   - `GET /v1/models/:model` → métadonnées d'un modèle précis (404 si inconnu).
   - `POST /v1/chat/completions` → relais vers DeepSeek avec Thinking désactivé.

3. **Injection du 'Thinking'** : sur chaque `POST /v1/chat/completions`, le payload
   reçu est dupliqué (sans muter le corps de la requête) puis on force :

   ```js
   payload.thinking = { type: "disabled" };
   ```

   Cette ligne est l'équivalent serveur du champ `"thinking": { "type": "disabled" }`
   documenté plus bas pour les appels API directs.

4. **Streaming** : si la requête demande `stream: true`, le proxy ajoute
   `stream_options.include_usage` (pour renvoyer les usages de tokens) et relaie le
   flux brut (`response.data.pipe(res)`). Le header `content-length` n'est jamais
   copié car la longueur du corps est recalculée selon le format réellement renvoyé.

5. **Erreurs** : les réponses d'erreur venant de DeepSeek sont relues (le corps est un
   stream) puis retransmises proprement en JSON avec le bon status HTTP.

6. **Source de vérité des modèles** : les modèles et leurs prix sont chargés depuis
   `scripts/proxy/models.json` (source unique, cf. principe DRY). La config Cline qui
   pointe vers ce proxy peut être régénérée avec :
   ```bash
   node scripts/proxy/generate-models-cline.js
   ```

7. **Config Cline associée** (provider « OpenAI Compatible ») :

   ```json
   {
     "baseUrl": "http://localhost:3000/v1",
     "model": "deepseek-v4-flash"
   }
   ```

   La clé API utilisée par le proxy reste celle de DeepSeek (transmise telle quelle au
   header `Authorization`).

## 📌 Pour les appels API hors Cline

// Non-thinking (mode recommandé pour un enchaînement d'agents)
{ "model": "deepseek-v4-flash", "thinking": { "type": "disabled" } }
// ou
{ "model": "deepseek-v4-flash", "reasoning_effort": "none" }
