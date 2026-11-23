#!/usr/bin/env node
/**
 * Génère le fichier de config Cline (modèles + prix) à partir de la source
 * unique de vérité c:\gsm\scripts\proxy\models.json (principe DRY).
 *
 * Usage :
 *   node generate-models-cline.js                # écrit par défaut
 *   node generate-models-cline.js <chemin>       # écrit vers un autre type de config Cline
 *   node generate-models-cline.js --dry-run      # affiche sans écrire
 *
 * Les prix de models.json sont exprimés en $ / 1M tokens, exactement au format
 * attendu par Cline (inputPrice, outputPrice, cacheReadsPrice).
 */
'use strict';

const fs = require('fs');
const path = require('path');

// Chemin du fichier de config Cline (machine locale de l'utilisateur).
const TARGETS = [
  'C:\\Users\\utilisateur\\.cline\\data\\settings\\models.json'
].map((p) => path.normalize(p));

const SOURCE = path.join(__dirname, 'models.json');

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const explicitTargets = args.filter((a) => !a.startsWith('--'));

  const catalog = readSource(SOURCE);

  const out = {
    version: 1,
    providers: {
      'openai-compatible': {
        provider: {
          name: 'OpenAI Compatible',
          baseUrl: catalog.baseUrl,
          defaultModelId: catalog.defaultModelId
        },
        models: buildModels(catalog)
      }
    }
  };

  const targets = explicitTargets.length > 0 ? explicitTargets : TARGETS;

  for (const target of targets) {
    if (dryRun) {
      console.log(`[dry-run] Écriture dans ${target}`);
      console.log(JSON.stringify(out, null, 2));
      continue;
    }
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, JSON.stringify(out, null, 2) + '\n', 'utf8');
    console.log(`✔ Config Cline mise à jour : ${target}`);
  }
}

function readSource(file) {
  let raw;
  try {
    raw = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    console.error(`✖ Impossible de lire ${file} : ${e.message}`);
    process.exit(1);
  }
  if (!raw.models || Object.keys(raw.models).length === 0) {
    console.error(`✖ Aucun modèle trouvé dans ${file}`);
    process.exit(1);
  }
  return raw;
}

// Convertit chaque modèle source (format proxy) en entrée Cline.
function buildModels(catalog) {
  const models = {};
  for (const model of Object.values(catalog.models)) {
    models[model.id] = {
      name: model.name || model.id,
      contextWindow: catalog.contextWindow,
      maxInputTokens: catalog.maxInputTokens,
      capabilities: model.capabilities,
      inputPrice: model.pricing.prompt,          // $ / 1M tokens (cache miss)
      outputPrice: model.pricing.completion,     // $ / 1M tokens
      cacheReadsPrice: model.pricing.cache_hit,  // $ / 1M tokens (cache hit)
      cacheWritesPrice: 0
    };
  }
  return models;
}

if (require.main === module) {
  main();
}

module.exports = { buildModels, readSource };
