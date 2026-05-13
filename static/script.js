document.addEventListener('DOMContentLoaded', () => {
    console.log('--- MAILFORGE SCRIPT LOADED ---');
    
    // Selectors
    const campaignForm = document.getElementById('campaign-form');
    const configForm = document.getElementById('config-form');
    const logDisplay = document.getElementById('log-display');
    const clearLogsBtn = document.getElementById('clear-logs');
    const campaignStatus = document.getElementById('campaign-status');
    const configStatus = document.getElementById('config-status');

    // Modal Logic
    const openSettingsBtn = document.getElementById('open-settings');
    const closeSettingsBtn = document.getElementById('close-settings');
    const modalWrap = document.getElementById('modal-wrap');

    const toggleModal = (show) => {
        modalWrap.style.display = show ? 'flex' : 'none';
        if (show) fetchConfig();
    };

    openSettingsBtn.onclick = () => toggleModal(true);
    closeSettingsBtn.onclick = () => toggleModal(false);
    modalWrap.onclick = (e) => { if (e.target === modalWrap) toggleModal(false); };

    // File Upload Handling
    const csvZone = document.getElementById('csv-drop-zone');
    const csvInput = document.getElementById('csv_file');
    const csvName = document.getElementById('csv-name');

    const templateZone = document.getElementById('template-drop-zone');
    const templateInput = document.getElementById('template_file');
    const templateName = document.getElementById('template-name');

    csvZone.onclick = () => csvInput.click();
    templateZone.onclick = () => templateInput.click();

    csvInput.onchange = () => {
        csvName.textContent = csvInput.files[0]?.name || 'None';
    };

    templateInput.onchange = () => {
        templateName.textContent = templateInput.files[0]?.name || 'None';
    };

    // Schedule Toggle
    const scheduleToggle = document.getElementById('schedule-toggle');
    const scheduleOptions = document.getElementById('schedule-options');
    const scheduledAtInput = document.getElementById('scheduled_at');

    scheduleToggle.onchange = () => {
        scheduleOptions.style.display = scheduleToggle.checked ? 'block' : 'none';
    };

    // Analytics Handling
    const statSent = document.getElementById('stat-sent');
    const statOpens = document.getElementById('stat-opens');
    const statOpenRate = document.getElementById('stat-open-rate');
    const statClicks = document.getElementById('stat-clicks');
    const statClickRate = document.getElementById('stat-click-rate');
    const insightsContainer = document.getElementById('ab-results-container');

    async function fetchAnalytics() {
        try {
            const response = await fetch('/api/analytics');
            const data = await response.json();
            
            if (data.stats) {
                statSent.textContent = data.stats.sent;
                statOpenRate.textContent = `${data.stats.open_rate}%`;
                statOpens.textContent = `${data.stats.opens} total opens`;
                statClickRate.textContent = `${data.stats.click_rate}%`;
                statClicks.textContent = `${data.stats.clicks} total clicks`;

                // Single subject analytics - Insights container cleared for simplicity
                insightsContainer.innerHTML = `
                    <div style="text-align: center; color: var(--text-muted); margin-top: 2rem;">
                        <p style="font-size: 0.85rem; font-weight: 600;">Active Campaign: ${data.campaign_name}</p>
                        <p style="font-size: 0.75rem;">Engine running with optimized single-subject delivery.</p>
                    </div>
                `;
            }
        } catch (err) {
            console.error('Analytics fetch failed:', err);
        }
    }

    // Run Campaign
    campaignForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        alert('Form Submit Event Fired!');
        
        if (!csvInput.files[0] || !templateInput.files[0]) {
            alert('Please select both CSV and Template files');
            return;
        }

        const formData = new FormData();
        formData.append('csv_file', csvInput.files[0]);
        formData.append('template_file', templateInput.files[0]);
        formData.append('campaign_name', document.getElementById('campaign_name').value);
        formData.append('rate_limit', document.getElementById('rate_limit').value);

        if (scheduleToggle.checked && scheduledAtInput.value) {
            formData.append('scheduled_at', scheduledAtInput.value);
        }

        alert('Sending request to server...');
        campaignStatus.textContent = 'Initializing Engine...';
        campaignStatus.style.color = 'var(--primary)';

        try {
            const response = await fetch('/api/run-campaign', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            alert('Server responded: ' + result.message);
            campaignStatus.textContent = result.message;
            campaignStatus.style.color = 'var(--success)';
            
            if (!scheduleToggle.checked) {
                campaignForm.reset();
                csvName.textContent = 'None';
                templateName.textContent = 'None';
            }
        } catch (err) {
            campaignStatus.textContent = 'Deployment Failed';
            campaignStatus.style.color = 'var(--error)';
        }
    });

    // Config Logic
    async function fetchConfig() {
        try {
            const response = await fetch('/api/config');
            const data = await response.json();
            document.getElementById('config_display_name').value = data.DISPLAY_NAME || '';
            document.getElementById('config_sender_email').value = data.SENDER_EMAIL || '';
            document.getElementById('config_smtp_host').value = data.SMTP_HOST || '';
            document.getElementById('config_smtp_port').value = data.SMTP_PORT || 587;
            document.getElementById('config_retry_count').value = data.RETRY_COUNT || 3;
        } catch (err) {
            console.error('Config fetch failed:', err);
        }
    }

    configForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('display_name', document.getElementById('config_display_name').value);
        formData.append('sender_email', document.getElementById('config_sender_email').value);
        formData.append('password', document.getElementById('config_password').value);
        formData.append('smtp_host', document.getElementById('config_smtp_host').value);
        formData.append('smtp_port', document.getElementById('config_smtp_port').value);
        formData.append('rate_limit', '1.0');
        formData.append('retry_count', document.getElementById('config_retry_count').value);

        configStatus.textContent = 'Updating...';
        configStatus.style.color = 'var(--primary)';

        try {
            const response = await fetch('/api/config', { method: 'POST', body: formData });
            const result = await response.json();
            configStatus.textContent = result.message;
            configStatus.style.color = 'var(--success)';
            setTimeout(() => toggleModal(false), 1000);
        } catch (err) {
            configStatus.textContent = 'Update Failed';
            configStatus.style.color = 'var(--error)';
        }
    });

    // Log Polling
    async function fetchLogs() {
        try {
            const response = await fetch('/api/logs');
            const data = await response.json();
            if (data.logs && data.logs.length > 0) {
                logDisplay.innerHTML = data.logs.map(log => {
                    let type = 'info';
                    if (log.includes('| ERROR |')) type = 'error';
                    if (log.includes('| SUCCESS |') || log.includes('sent') || log.includes('Campaign started')) type = 'success';
                    return `<div class="log-item ${type}">${log}</div>`;
                }).join('');
                logDisplay.scrollTop = logDisplay.scrollHeight;
            }
        } catch (err) {
            console.error('Log fetch failed:', err);
        }
    }

    clearLogsBtn.onclick = fetchLogs;
    setInterval(() => { fetchLogs(); fetchAnalytics(); }, 3000);
    fetchLogs(); fetchAnalytics();
});
