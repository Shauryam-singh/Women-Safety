document.addEventListener('DOMContentLoaded', function() {
    const routeForm = document.getElementById('route-form');
    if (routeForm) {
        routeForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const start = document.getElementById('start').value;
            const end = document.getElementById('end').value;

            fetch('/route-finder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ start, end })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('route-results').innerText = JSON.stringify(data, null, 2);
            })
            .catch(error => console.error('Error:', error));
        });
    }

    function uploadVideo() {
        const videoUpload = document.getElementById('video-upload');
        const file = videoUpload.files[0];
        // Handle file upload and processing
        console.log('Video file:', file);
    }

    function uploadAudio() {
        const audioUpload = document.getElementById('audio-upload');
        const file = audioUpload.files[0];
        // Handle file upload and processing
        console.log('Audio file:', file);
    }
});
