def policy_check(prompt, consent_scope):
    blocked_terms = ["impersonate", "sound exactly like", "be ", "call as "]
    if any(term in prompt.lower() for term in blocked_terms):
        return "block"
    if "politics" in prompt.lower() and "political content" in consent_scope.get("prohibited_uses", []):
        return "block"
    return "allow"
