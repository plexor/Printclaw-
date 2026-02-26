from printclaw.core.kb_loader import KnowledgebaseLoader


def test_kb_loader_loads_yaml():
    loader = KnowledgebaseLoader()
    data = loader.load_all()
    assert any(path.endswith('vendors/hp.yaml') for path in data)
    hits = loader.search('driver mismatch')
    assert hits
