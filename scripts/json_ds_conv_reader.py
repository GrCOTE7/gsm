import json
import os
import re
import sys
from datetime import datetime

# ============================================================
# CONSTANTE DE CONTRÔLE
# THINK = 1  → affiche tout (y compris le "thinking")
# THINK = 0  → affiche uniquement les réponses et outils (sans le "thinking")
# ============================================================
THINK = 0 if len(sys.argv) < 2 or sys.argv[1].lower() != "0" else 0
# ============================================================

# --- 1. CHERCHER LE FICHIER ---
fichier_principal = None
for f in os.listdir("./.tmp/"):
    if f.endswith(".json") and "messages" in f.lower():
        fichier_principal = "./.tmp/" + f
        break

if not fichier_principal:
    print("❌ Aucun fichier .messages.json trouvé.")
    exit()

print(f"✅ Fichier trouvé : {fichier_principal}")

# --- 2. LIRE LE JSON ---
with open(fichier_principal, "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("messages", [])
if not messages:
    print("❌ Aucun message trouvé dans le fichier.")
    exit()

print(f"📨 {len(messages)} messages trouvés.")


# --- 3. FONCTION POUR FORMATER UN RÉSULTAT D'OUTIL ---
def format_tool_result(block):
    """Formate un bloc tool_result de façon lisible."""
    tool_use_id = block.get("tool_use_id", "inconnu")
    name = block.get("name", "outil")
    content = block.get("content", [])

    output = f"🔧 **Résultat de l'outil `{name}`** (ID: `{tool_use_id}`)\n\n"

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                if "query" in item and "result" in item:
                    query = item.get("query", "")
                    result = item.get("result", "")
                    output += f"**Requête :** `{query}`\n\n"
                    lines = result.split("\n")
                    if len(lines) > 20:
                        output += (
                            f"```\n"
                            + "\n".join(lines[:20])
                            + f"\n... (tronqué, {len(lines)-20} lignes supplémentaires)\n```\n"
                        )
                    else:
                        output += f"```\n{result}\n```\n"
                else:
                    output += f"```json\n{json.dumps(item, indent=2, ensure_ascii=False)}\n```\n"
            elif isinstance(item, str):
                output += f"```\n{item}\n```\n"
            else:
                output += (
                    f"```json\n{json.dumps(item, indent=2, ensure_ascii=False)}\n```\n"
                )
    else:
        output += f"```json\n{json.dumps(content, indent=2, ensure_ascii=False)}\n```\n"

    return output


# --- 4. GÉNÉRER LE MARKDOWN ---
markdown = f"# Conversation Cline / DeepSeek\n\n"
markdown += f"*Exporté le {datetime.now().strftime('%d/%m/%Y à %H:%M')}*\n"
markdown += f"*Session : {data.get('sessionId', 'inconnue')}*\n"
markdown += f"*Agent : {data.get('agent', 'inconnu')}*\n"
markdown += f"*Thinking : {'✅ affiché' if THINK else '❌ masqué'}*\n\n---\n\n"

for idx, msg in enumerate(messages):
    role = msg.get("role", "inconnu").upper()
    content_blocks = msg.get("content", [])

    thinking_text = ""
    response_text = ""
    tool_calls = []
    tool_results = []

    if isinstance(content_blocks, list):
        for block in content_blocks:
            block_type = block.get("type", "")
            if block_type == "thinking":
                thinking_text = block.get("thinking", "")
            elif block_type == "text":
                response_text += block.get("text", "") + "\n"
            elif block_type == "tool_use":
                tool_name = block.get("name", "outil")
                tool_input = block.get("input", {})
                tool_calls.append(f"📞 **Appel d'outil :** `{tool_name}`")
                tool_calls.append(
                    f"```json\n{json.dumps(tool_input, indent=2, ensure_ascii=False)}\n```\n"
                )
            elif block_type == "tool_result":
                tool_results.append(format_tool_result(block))
            else:
                response_text += f"[{block_type}] : {json.dumps(block, indent=2, ensure_ascii=False)}\n"
    else:
        content = str(content_blocks)
        thinking_match = re.search(r"<thinking>(.*?)</thinking>", content, re.DOTALL)
        thinking_text = thinking_match.group(1).strip() if thinking_match else ""
        response_text = re.sub(
            r"<thinking>.*?</thinking>", "", content, flags=re.DOTALL
        ).strip()

    markdown += f"### Échange #{idx+1} — **{role}**\n\n"

    # --- On affiche le thinking UNIQUEMENT si THINK = 1 ---
    if thinking_text and THINK:
        markdown += f"#### 🧠 *Thinking* (raisonnement interne) :\n```\n{thinking_text.strip()}\n```\n\n"

    if response_text:
        markdown += f"#### 💬 Réponse :\n```\n{response_text.strip()}\n```\n\n"

    for call in tool_calls:
        markdown += call + "\n"

    for result in tool_results:
        markdown += result + "\n"

    if not thinking_text and not response_text and not tool_calls and not tool_results:
        markdown += f"```json\n{json.dumps(content_blocks, indent=2, ensure_ascii=False)}\n```\n\n"

    markdown += "---\n\n"

# --- 5. SAUVEGARDER ---
nom_sortie = f"./.tmp/conversation_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
with open(nom_sortie, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"✅ Fichier généré : {nom_sortie}")
