def parse_rules(user_agent_sections):
    """Extracts only Disallow rules."""
    rules = {"Disallow": []}  # We no longer track "Allow" rules
    
    for _, section in user_agent_sections:
        for line in section:
            if "disallow:" in line.lower():
                rules["Disallow"].append(line.split(":")[1].strip())
    
    return rules