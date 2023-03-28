<script>
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({
    video: true
}).then(stream => {
    video.srcObject = stream;
    video.play();
}).catch(error => console.error('Could not access camera:', error));

let intervalId = setInterval(detectText, 3000);


function detectText() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');
     fetch('/detect-text', {
                method: 'POST',
                body: JSON.stringify({
                    imageData: imageData
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    clearInterval(intervalId);
                    // add the code here to show the SweetAlert and play the text using TextToSpeech
                } else if (data.status === 'error') {
                    Swal.fire({
                        title: 'Error',
                        text: 'Could not detect text. Retrying in 5 seconds...',
                        timer: 5000,
                        onBeforeOpen: () => {
                            Swal.showLoading();
                        },
                        onClose: () => {
                            intervalId = setInterval(detectText, 3000);
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Could not detect text:', error);
            });
}

</script>

<script>
        let url_textToSpeech = "https://api.aiforthai.in.th/vaja9/synth_audiovisual"

        function TextToSpeech(text) {
        var settings = {
            url: url_textToSpeech,
            method: "POST",
            headers: {
                Apikey: "letBGyiaspJ9ERccDfEB5R4vKeCMKfQy",
                "Content-Type": "application/json",
            },
            data: JSON.stringify({
                input_text: text,
                speaker: 0,
                phrase_break: 0,
                audiovisual: 0,
            }),
        };

        async function play_wav(wav) {
            const audioSource = document.getElementById("audio");
            const result = await fetch(wav, {
                headers: {
                    Apikey: "letBGyiaspJ9ERccDfEB5R4vKeCMKfQy",
                },
            });

            const blob = await result.blob();
            if (blob) {
                audioSource.src = URL.createObjectURL(blob);
            }
        }
        $.ajax(settings).done(function(response) {
            play_wav(response.wav_url);
        });
    }
</script>