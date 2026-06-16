let currentWallet = null;

function getChain() {
    return document.getElementById('chain').value;
}

function showStatus(message, type = 'info') {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type}`;
    status.classList.remove('hidden');
    setTimeout(() => status.classList.add('hidden'), 5000);
}

function createWallet() {
    fetch('/api/wallet/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chain: getChain() })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showStatus('Error: ' + data.error, 'error');
        } else {
            currentWallet = data;
            displayResult(data);
            showStatus('Wallet created successfully!', 'success');
        }
    })
    .catch(e => showStatus('Error: ' + e, 'error'));
}

function showImportForm() {
    document.getElementById('importForm').classList.remove('hidden');
}

function hideImportForm() {
    document.getElementById('importForm').classList.add('hidden');
    document.getElementById('mnemonicInput').value = '';
}

function importWallet() {
    const mnemonic = document.getElementById('mnemonicInput').value.trim();
    if (!mnemonic) {
        showStatus('Please enter a mnemonic phrase', 'error');
        return;
    }

    fetch('/api/wallet/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chain: getChain(), mnemonic })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showStatus('Error: ' + data.error, 'error');
        } else {
            currentWallet = data;
            displayResult(data);
            hideImportForm();
            showStatus('Wallet imported successfully!', 'success');
        }
    })
    .catch(e => showStatus('Error: ' + e, 'error'));
}

function showLoadForm() {
    document.getElementById('loadForm').classList.remove('hidden');
}

function hideLoadForm() {
    document.getElementById('loadForm').classList.add('hidden');
    document.getElementById('loadPassword').value = '';
}

function loadWallet() {
    const password = document.getElementById('loadPassword').value;
    if (!password) {
        showStatus('Please enter a password', 'error');
        return;
    }

    fetch('/api/wallet/load', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showStatus('Error: ' + data.error, 'error');
        } else {
            document.getElementById('chain').value = data.chain;
            importWallet();
            hideLoadForm();
            showStatus('Wallet loaded successfully!', 'success');
        }
    })
    .catch(e => showStatus('Error: ' + e, 'error'));
}

function showSignForm() {
    if (!currentWallet || !currentWallet.mnemonic) {
        showStatus('Please create or import a wallet first', 'error');
        return;
    }
    document.getElementById('signForm').classList.remove('hidden');
}

function hideSignForm() {
    document.getElementById('signForm').classList.add('hidden');
    document.getElementById('messageInput').value = '';
}

function signMessage() {
    const message = document.getElementById('messageInput').value.trim();
    if (!message) {
        showStatus('Please enter a message', 'error');
        return;
    }

    if (!currentWallet || !currentWallet.mnemonic) {
        showStatus('Please create or import a wallet first', 'error');
        return;
    }

    fetch('/api/wallet/sign-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            chain: getChain(),
            mnemonic: currentWallet.mnemonic,
            message
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showStatus('Error: ' + data.error, 'error');
        } else {
            displayResult(data);
            hideSignForm();
            showStatus('Message signed!', 'success');
        }
    })
    .catch(e => showStatus('Error: ' + e, 'error'));
}

function showSaveForm() {
    if (!currentWallet || !currentWallet.mnemonic) {
        showStatus('Please create or import a wallet first', 'error');
        return;
    }
    document.getElementById('saveForm').classList.remove('hidden');
}

function hideSaveForm() {
    document.getElementById('saveForm').classList.add('hidden');
    document.getElementById('savePassword').value = '';
    document.getElementById('savePasswordConfirm').value = '';
}

function saveWallet() {
    const pwd = document.getElementById('savePassword').value;
    const pwdConfirm = document.getElementById('savePasswordConfirm').value;

    if (!pwd || !pwdConfirm) {
        showStatus('Please enter both passwords', 'error');
        return;
    }

    if (pwd !== pwdConfirm) {
        showStatus('Passwords do not match', 'error');
        return;
    }

    if (!currentWallet || !currentWallet.mnemonic) {
        showStatus('Please create or import a wallet first', 'error');
        return;
    }

    fetch('/api/wallet/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            chain: getChain(),
            mnemonic: currentWallet.mnemonic,
            password: pwd
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            showStatus('Error: ' + data.error, 'error');
        } else {
            hideSaveForm();
            showStatus('Wallet saved and encrypted!', 'success');
        }
    })
    .catch(e => showStatus('Error: ' + e, 'error'));
}

function displayResult(data) {
    const result = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    resultContent.textContent = JSON.stringify(data, null, 2);
    result.classList.remove('hidden');
}

function copyResult() {
    const content = document.getElementById('resultContent').textContent;
    navigator.clipboard.writeText(content).then(() => {
        showStatus('Copied to clipboard!', 'success');
    });
}

function clearResult() {
    document.getElementById('result').classList.add('hidden');
    currentWallet = null;
}
