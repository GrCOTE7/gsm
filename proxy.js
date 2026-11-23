const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// Source unique de vérité : métadonnées + prix de tous les modèles.
// À maintenir dans scripts/proxy/models.json (utilisé aussi par
// scripts/proxy/generate-models-cline.js pour mettre à jour la config
// Cline, cf. DRY).
const MODEL_CATALOG = require('./scripts/proxy/models.json');

// Endpoint pour que Cline récupère les métadonnées du modèle
app.get('/v1/models', (req, res) => {
  res.json({
    object: 'list',
    data: Object.values(MODEL_CATALOG.models)
  });
});

app.get('/v1/models/:model', (req, res) => {
  const model = MODEL_CATALOG.models[req.params.model];
  if (model) {
    res.json(model);
  } else {
    res.status(404).json({ error: 'Model not found' });
  }
});

app.post('/v1/chat/completions', async (req, res) => {
  // Copie de travail du payload pour ne pas muter req.body
  const payload = { ...req.body };
  // payload.thinking = { type: "disabled" };

  if (payload.stream === true) {
    payload.stream_options = { include_usage: true };
  }

  try {
    const response = await axios({
      method: 'POST',
      url: 'https://api.deepseek.com/v1/chat/completions',
      data: payload,
      headers: {
        'Authorization': req.headers.authorization,
        'Content-Type': 'application/json',
        'Accept': req.headers.accept || 'application/json'
      },
      responseType: 'stream'
    });

    // On ne copie jamais Content-Length : la longueur du body sera
    // recalculée selon le format réellement renvoyé ci-dessous.
    const headers = { ...response.headers };
    delete headers['content-length'];

    if (payload.stream === true) {
      res.set(headers);
      res.status(response.status);
      response.data.pipe(res);
    } else {
      const body = await collectBody(response.data);
      res.set(headers);
      try {
        res.status(response.status).json(JSON.parse(body));
      } catch (e) {
        res.status(response.status).send(body);
      }
    }
  } catch (error) {
    if (error.response) {
      // error.response.data est un Stream (responseType: 'stream') : on
      // doit le lire avant de pouvoir répondre un JSON d'erreur propre.
      try {
        const errBody = await collectBody(error.response.data);
        res.set({
          'Content-Type': error.response.headers['content-type'] || 'application/json'
        });
        try {
          res.status(error.response.status).json(JSON.parse(errBody));
        } catch (e) {
          res.status(error.response.status).send(errBody);
        }
      } catch (e) {
        res.status(error.response.status).send({ error: error.message });
      }
    } else {
      res.status(500).json({ error: error.message });
    }
  }
});

// Lit tout un stream et en renvoie le contenu sous forme de chaîne.
function collectBody(stream) {
  return new Promise((resolve, reject) => {
    let data = '';
    stream.on('data', chunk => data += chunk);
    stream.on('error', reject);
    stream.on('end', () => resolve(data));
  });
}

app.listen(3000, () => {
  console.log('✅ Proxy DeepSeek actif - mode thinking désactivé');
  console.log('   Métadonnées de prix disponibles sur /v1/models');
  console.log('   http://localhost:3000');
});

// Starter dans WIN + R  → shell:startup en PROXY.bat

// @echo off
// rem Démarre le proxy DeepSeek (Cline / Insomnia) au login - fenêtre minimisée.
// start "" /min node "C:\gsm\proxy.js"