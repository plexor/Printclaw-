from printclaw.core.agent import PrintclawAgent


def test_registry_loads_skills():
    agent = PrintclawAgent()
    skills = agent.registry.list()
    assert len(skills) >= 9
    assert any(s['id'] == 'windows_list_printers' for s in skills)
