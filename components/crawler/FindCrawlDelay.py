def find_crawl_delay(user_agent_sections):
    """Finds Crawl-delay values."""
    return {agent: line.split(":")[1].strip() for agent, section in user_agent_sections for line in section if "crawl-delay:" in line.lower()}