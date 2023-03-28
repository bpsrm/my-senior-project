<script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    navigator.mediaDevices.getUserMedia({
            video: true
        })
        .then(stream => {
            video.srcObject = stream;
            video.play();
        })
        .catch(error => {
            console.error('Could not access camera:', error);
        });


    let intervalId;

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
                    Swal.fire({
                        title: 'ข้อความของคุณคือ: ' + data.text,
                        text: 'เสียงบรรยายจากเว็บไซต์ AI FOR THAI',
                        buttons: {
                            cancel: true,
                            confirm: "Play"
                        }
                    }).then((result) => {
                        if (result) {
                            function TextToSpeech() {
                                var settings = {
                                    url: "https://api.aiforthai.in.th/vaja9/synth_audiovisual",
                                    method: "POST",
                                    headers: {
                                        Apikey: "letBGyiaspJ9ERccDfEB5R4vKeCMKfQy",
                                        "Content-Type": "application/json",
                                    },
                                    data: JSON.stringify({
                                        input_text: data.text,
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
                            };
                            const audio = document.createElement("audio");
                            audio.src = "your-audio-source.mp3";
                            audio.controls = true;
                            audio.autoplay = true;

                            swal({
                                content: audio
                            });

                        } else {
                            intervalId = setInterval(detectText, 3000);
                        }
                    })
                    setTimeout(() => {
                        if (!Swal.isLoading()) {
                            Swal.close();
                            intervalId = setInterval(detectText, 3000);
                        }
                    }, 5000);;
                } else if (data.status === 'error') {
                    result.textContent = "เริ่มต้นการตรวจจับข้อความจากกล้องของคุณ";
                }

            })
            .catch(error => {
                console.error('ไม่สามารถค้นหาข้อความใน', error);
            });
    }

    intervalId = setInterval(detectText, 3000);
</script>

<///////////////////////////////////////////////////////////>
<script>
      const video = document.getElementById("video");
      const canvas = document.getElementById("canvas");
      const ctx = canvas.getContext("2d");
      const url = "https://api.aiforthai.in.th/vaja9/synth_audiovisual";

      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          video.srcObject = stream;
          video.play();
        });

      setInterval(() => {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const data = canvas.toDataURL("image/png");

        fetch("/detect-text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.success) {
              const text = data.text;
              fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text }),
              })
                .then((res) => res.json())
                .then((data) => {
                  const audio = new Audio(data.sound);
                  audio.play();
                  Swal.fire({
                    title: "Success!",
                    text: `Text detected: ${text}`,
                    icon: "success",
                  });
                })
                .catch((error) => console.error(error));
            } else {
              fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: "ไม่สามารถตรวจจับข้อความได้" }),
              })
                .then((res) => res.json())
                .then((data) => {
                  const audio = new Audio(data.sound);
                  audio.play();
                  Swal.fire({
                    title: "Error!",
                    text: "No text detected.",
                    icon: "error",
                  });
                })
                .catch((error) => console.error(error));
            }
          })
          .catch((error) => console.error(error));
      }, 3000);
</script>