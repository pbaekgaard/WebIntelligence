import re

def find_user_agents(robots_txt_content, user_agent="*"):
    """Finds matching user-agent sections."""
    agents_sections = []
    current_agent = None
    current_section = []
    
    for line in robots_txt_content.splitlines():
        line = re.sub(r'#.*', '', line).strip()  # Remove comments and extra whitespace
        if not line:
            continue
        
        if line.lower().startswith("user-agent:"):
            if current_agent and current_section:
                agents_sections.append((current_agent, current_section))
            current_agent = line.split(":")[1].strip()
            current_section = []
        
        if current_agent:
            current_section.append(line)
    
    if current_agent and current_section:
        agents_sections.append((current_agent, current_section))
    
    return [(agent, section) for agent, section in agents_sections if agent == user_agent or agent == "*"]
