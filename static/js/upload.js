/**
 * SmartRetail AI - Dataset Upload & Cleansing Pipeline
 * Author: Ananthi Merciya M (Reg No: ASML24005)
 */

document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const selectedFileInfo = document.getElementById('selectedFileInfo');
    const startUploadBtn = document.getElementById('startUploadBtn');
    const uploadProgressBar = document.getElementById('uploadProgressBar');
    const inspectionSection = document.getElementById('inspectionSection');

    let currentFile = null;

    if (browseBtn) {
        browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileInput.click();
        });
    }

    if (dropZone) {
        dropZone.addEventListener('click', () => fileInput.click());

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.style.borderColor = '#14b8a6';
                dropZone.style.background = 'rgba(20, 184, 166, 0.15)';
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.style.borderColor = 'rgba(20, 184, 166, 0.4)';
                dropZone.style.background = 'rgba(15, 23, 42, 0.6)';
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                handleFileSelection(files[0]);
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                handleFileSelection(this.files[0]);
            }
        });
    }

    function handleFileSelection(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['csv', 'xlsx', 'xls'].includes(ext)) {
            if (window.showToast) window.showToast('Please select a valid CSV or Excel file (.xlsx, .xls)', 'error');
            return;
        }

        currentFile = file;
        const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
        selectedFileInfo.innerHTML = `<i class="bi bi-file-earmark-check me-1"></i> Selected: <strong>${file.name}</strong> (${sizeMb} MB)`;
        selectedFileInfo.classList.remove('d-none');
        startUploadBtn.classList.remove('d-none');
    }

    if (startUploadBtn) {
        startUploadBtn.addEventListener('click', function () {
            if (!currentFile) {
                if (window.showToast) window.showToast('Please select a dataset file first.', 'warning');
                return;
            }

            const formData = new FormData();
            formData.append('file', currentFile);

            uploadProgressBar.classList.remove('d-none');
            startUploadBtn.disabled = true;
            startUploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Processing Pipeline...';

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                uploadProgressBar.classList.add('d-none');
                startUploadBtn.disabled = false;
                startUploadBtn.innerHTML = '<i class="bi bi-play-circle-fill me-1"></i> Process &amp; Ingest File';

                if (!data.success) {
                    throw new Error(data.error || 'Dataset validation failed');
                }

                if (window.showToast) {
                    window.showToast('Dataset validated and processed successfully!', 'success');
                }

                renderInspectionResults(data);
            })
            .catch(err => {
                uploadProgressBar.classList.add('d-none');
                startUploadBtn.disabled = false;
                startUploadBtn.innerHTML = '<i class="bi bi-play-circle-fill me-1"></i> Process &amp; Ingest File';
                console.error('Upload Error:', err);
                if (window.showToast) {
                    window.showToast('Upload Error: ' + err.message, 'error');
                }
            });
        });
    }

    function renderInspectionResults(data) {
        inspectionSection.classList.remove('d-none');
        inspectionSection.scrollIntoView({ behavior: 'smooth' });

        const insp = data.inspection || {};
        const clean = data.cleaning || {};

        document.getElementById('auditRows').textContent = Number(clean.processed_rows || insp.rows || 0).toLocaleString();
        document.getElementById('auditCols').textContent = insp.columns_count || 0;
        document.getElementById('auditMissing').textContent = Number(insp.total_missing || 0).toLocaleString();
        document.getElementById('auditDuplicates').textContent = Number(clean.dropped_duplicates || insp.duplicate_count || 0).toLocaleString();

        // Populate Column Breakdown Table
        const tbody = document.getElementById('columnsTableBody');
        tbody.innerHTML = '';
        if (insp.columns_info) {
            insp.columns_info.forEach((col, idx) => {
                const tr = document.createElement('tr');
                const isRequired = ['Order Date', 'Sales', 'Profit', 'Quantity', 'Discount', 'Category'].includes(col.name);
                tr.innerHTML = `
                    <td>${idx + 1}</td>
                    <td><strong>${col.name}</strong> ${isRequired ? '<span class="badge bg-teal ms-1">Required</span>' : ''}</td>
                    <td><code>${col.dtype}</code></td>
                    <td><span class="${col.missing > 0 ? 'text-warning fw-bold' : 'text-secondary'}">${col.missing}</span></td>
                    <td>${col.unique.toLocaleString()}</td>
                    <td><span class="badge bg-success-subtle text-success border border-success">Valid</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Populate Preview Table
        const preview = insp.preview || [];
        const thead = document.getElementById('previewTableHead');
        const previewBody = document.getElementById('previewTableBody');
        thead.innerHTML = '';
        previewBody.innerHTML = '';

        if (preview.length > 0) {
            const headers = Object.keys(preview[0]);
            let headerHtml = '<tr>';
            headers.forEach(h => {
                headerHtml += `<th>${h}</th>`;
            });
            headerHtml += '</tr>';
            thead.innerHTML = headerHtml;

            preview.forEach(row => {
                let rowHtml = '<tr>';
                headers.forEach(h => {
                    let val = row[h];
                    if (val === null || val === undefined) val = '<span class="text-muted">null</span>';
                    else if (typeof val === 'number') val = val.toLocaleString();
                    rowHtml += `<td>${val}</td>`;
                });
                rowHtml += '</tr>';
                previewBody.insertAdjacentHTML('beforeend', rowHtml);
            });
        }
    }
});

