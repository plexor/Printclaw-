from printclaw.core.agent import PrintclawAgent
from printclaw.core.context import AgentContext


def test_session_store_save_and_get():
    agent = PrintclawAgent()
    payload = agent.run_diagnostics(AgentContext())
    fetched = agent.session_store.get(payload['session_id'])
    assert fetched is not None
    assert fetched['session_id'] == payload['session_id']
