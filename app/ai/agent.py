# app/ai/agent.py
import re
from app.database.vector_store import VectorDB
from app.utils.i18n import TRANSLATIONS

class EcommerceMCPAgent:
    def __init__(self, db: VectorDB):
        self.db = db

    def process_message(self, user_prompt: str, lang: str) -> dict:
        prompt_lower = user_prompt.lower()
        t = TRANSLATIONS[lang]
        
        # Match English search terms or Hindi search terms (खोजें / ढूंढें / चाहिए)
        if any(kw in prompt_lower for kw in ["find", "search", "show", "need", "खोज", "ढूंढ", "चाहिए", "दिखाओ"]):
            clean_search = re.sub(r'(find|search|show|need|खोजें|ढूंढें|चाहिए|दिखाओ)\b', '', prompt_lower).strip()
            matches = self.db.search_products(clean_search if clean_search else "items")
            
            if matches:
                resp = t["vector_search_log"]
                for m in matches:
                    resp += f"• **{m['name']}** — ${m['price']:.2f} *(ID: {m['id']})*\n"
                return {"action": "DISPLAY", "content": resp}
            return {"action": "DISPLAY", "content": t["not_found"]}

        # Match English add terms or Hindi add terms (जोड़ें / डालो)
        elif any(kw in prompt_lower for kw in ["add", "जोड़ें", "डालो"]):
            matches = self.db.search_products(prompt_lower, limit=1)
            if matches:
                target_item = matches[0]
                return {
                    "action": "ADD_TO_CART",
                    "item": target_item,
                    "content": t["cart_add_log"].format(name=target_item['name'], price=target_item['price'])
                }
            return {"action": "DISPLAY", "content": t["specific_add"]}

        else:
            return {"action": "DISPLAY", "content": t["welcome_fallback"]}
