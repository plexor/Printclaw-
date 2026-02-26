let latestSession = null;

async function fetchJSON(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}

async function refreshSessions() {
  const data = await fetchJSON('/api/sessions');
  const block = document.getElementById('sessions') || document.getElementById('sessionsList');
  if (block) block.textContent = JSON.stringify(data.sessions, null, 2);
}

async function refreshLogs() {
  const data = await fetchJSON('/api/logs/latest');
  const block = document.getElementById('logs');
  if (block) block.textContent = JSON.stringify(data.entries, null, 2);
}

async function runDiagnostics() {
  const spinner = document.getElementById('spinner');
  spinner?.classList.remove('hidden');
  try {
    const targetIp = document.getElementById('targetIp')?.value;
    const payload = await fetchJSON(`/api/diagnose${targetIp ? `?target_ip=${encodeURIComponent(targetIp)}` : ''}`, { method: 'POST' });
    latestSession = payload;
    document.getElementById('printers').textContent = JSON.stringify(payload.printers, null, 2);
    document.getElementById('spooler').textContent = JSON.stringify(payload.skills_ran.find(s => s.skill_id === 'windows_spooler_status')?.data ?? {}, null, 2);
    document.getElementById('network').textContent = JSON.stringify(payload.skills_ran.filter(s => s.skill_id.startsWith('network_')).map(s => s.data), null, 2);
    document.getElementById('issues').textContent = JSON.stringify(payload.issues_found, null, 2);
    document.getElementById('fixes').textContent = JSON.stringify(payload.recommended_fixes, null, 2);
    document.getElementById('confidence').textContent = `${payload.confidence_score}%`;
    alert('Diagnostics complete.');
    await refreshSessions();
  } catch (error) {
    alert(`Diagnostics failed: ${error.message}`);
  } finally {
    spinner?.classList.add('hidden');
  }
}

async function exportLatest() {
  if (!latestSession) return alert('Run diagnostics first.');
  window.location.href = `/api/sessions/${latestSession.session_id}/export?format=json`;
}

function copySummary() {
  if (!latestSession) return alert('No session yet.');
  navigator.clipboard.writeText(latestSession.ticket_summary);
  alert('Ticket summary copied.');
}

async function loadSessionDetailsIfNeeded() {
  if (!window.SESSION_ID) return;
  const payload = await fetchJSON(`/api/sessions/${window.SESSION_ID}`);
  document.getElementById('sessionDetails').textContent = JSON.stringify(payload, null, 2);
}

document.getElementById('runBtn')?.addEventListener('click', runDiagnostics);
document.getElementById('exportBtn')?.addEventListener('click', exportLatest);
document.getElementById('copySummaryBtn')?.addEventListener('click', copySummary);

refreshSessions().catch(() => {});
refreshLogs().catch(() => {});
loadSessionDetailsIfNeeded().catch(() => {});
