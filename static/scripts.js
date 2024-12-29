
function topFunction() {
    document.body.scrollTop = 0; // สำหรับ Safari
    document.documentElement.scrollTop = 0; // สำหรับ Chrome, Firefox, IE และ Opera
}

function previewImage(event) {
    const preview = document.getElementById('preview');
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function () {
        preview.src = reader.result;
        preview.style.display = 'inline';
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}

function formatResults(data) {
    if (data.status === 'error') {
        return `<div class="error">เกิดข้อผิดพลาด: ${data.error}</div>`;
    }

    return `<div class="text-response">${data.text}</div>`;
}

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            const fileInput = document.getElementById('imageInput');
            const resultDiv = document.getElementById('result');

            if (fileInput.files.length === 0) {
                alert('กรุณาเลือกไฟล์ภาพ');
                return;
            }

            formData.append('file', fileInput.files[0]);
            resultDiv.innerHTML = '<div class="loading">กำลังประมวลผล...</div>';
            resultDiv.style.display = 'block';

            try {
                const response = await fetch('/process-receipt/', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                resultDiv.innerHTML = formatResults(data);
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">เกิดข้อผิดพลาด: ' + error.message + '</div>';
            }
        });
    } else {
        console.error('ไม่พบองค์ประกอบที่มี id="uploadForm"');
    }
});