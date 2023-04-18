
old version
<script>
        //dropdown show list
    const dropdownButton = document.querySelector('#dropdown_speech');
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        $(item).click(function(e) {
            e.preventDefault();
            dropdownButton.textContent = item.textContent;
        });

    });
    $(".show_detect").css("display", "none");

    let intervalID;

    $(".btn_start").click(function(e) {
        e.preventDefault();
        $(".btn_start").hide();
        $(".show_detect").css("display", "block");

        //open video to detect text in camera
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');

        navigator.mediaDevices.getUserMedia({
            video: true
        }).then(stream => {
            video.srcObject = stream;
            video.play();
        }).catch(error => console.error('Could not access camera:', error));

        intervalID = setInterval(detectText, 5000);

        function detectText() {

            //get image data and send to python file to check text
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
            }).then(response => response.json()).then(data => {
                if (data.status !== 'success') {
                    Swal.fire({
                        position: 'top',
                        icon: 'error',
                        title: 'ไม่สามารถค้นหาข้อความได้',
                        text: 'กรุณาลองอีกครั้งใน 5 วินาที',
                        timer: 5000,
                        timerProgressBar: true,
                        showConfirmButton: false,
                        willClose: () => {
                            intervalID = setInterval(detectText, 5000);
                        }
                    });
                } else {
                    clearInterval(intervalID);
                    Swal.fire({
                        icon: 'success',
                        title: 'ข้อความของคุณคือ',
                        text: data.text,
                        // timer: 5000,
                        // timerProgressBar: true,
                        showConfirmButton: true,
                    }).then((result) => {
                        if (result.isConfirmed) {
                            // setup api parameter
                            let urlAPI = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual'
                            var setting_API = {
                                url: urlAPI,
                                method: "POST",
                                headers: {
                                    "Apikey": "letBGyiaspJ9ERccDfEB5R4vKeCMKfQy",
                                    "Content-Type": "application/json",
                                },
                                data: JSON.stringify({
                                    input_text: data.text,
                                    speaker: 0,
                                    phrase_break: 0,
                                    audiovisual: 0,
                                })
                            };

                            Swal.fire({
                                title: 'กำลังประมวลผลเสียง...',
                                allowEscapeKey: false,
                                allowOutsideClick: false,
                                didOpen: () => {
                                    Swal.showLoading();
                                }
                            });
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
                                    audioSource.onended = onFinished;
                                    audioSource.play();
                                    // clearInterval(intervalID)
                                }
                            }
                            $.ajax(setting_API).done(function(response) {
                                // check status
                                console.log(response);
                                if (response.msg == "success") {
                                    Swal.close();
                                    Swal.fire({
                                        icon: 'success',
                                        title: 'เสียงของคุณพร้อมแล้ว!',
                                        text: 'คลิกเพื่อฟัง',
                                        confirmButtonText: 'เล่นเสียง',
                                        allowOutsideClick: false,
                                    }).then((result) => {
                                        if (result.isConfirmed) {
                                            clearInterval(intervalID)
                                            play_wav(response.wav_url);
                                        }
                                    });
                                } else {
                                    Swal.close();
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'ไม่สามารถสร้างเสียงได้',
                                        text: 'กรุณาลองอีกครั้งในภายหลัง',
                                        allowOutsideClick: false,
                                    });
                                }
                            }).fail(function(jqXHR, textStatus) {
                                Swal.close();
                                Swal.fire({
                                    icon: 'error',
                                    title: 'ไม่สามารถเชื่อมต่อ API ได้',
                                    text: 'กรุณาลองใหม่ในภายหลัง',
                                    confirmButton: false,
                                    timer: 3000,
                                    timerProgressBar: true,
                                });

                                setTimeout(function() {
                                    window.location.href = '/detect';
                                }, 3000);
                            });
                        }
                    });



                }

                function onFinished() {
                    const btnListen = document.createElement("button");
                    let audioSRC = document.getElementById('audio')
                    btnListen.className = "btn_listen w-100";
                    btnListen.textContent = "เสร็จสิ้นการฟังเสียง";
                    $(".show_detect").append(btnListen);
                    btnListen.addEventListener("click", function() {
                        // isListening = true;
                        audioSRC.src = ""
                        $(".btn_listen").hide();
                        // clearInterval(intervalId);
                        intervalId = setInterval(detectText, 5000)
                    });
                }
            }).catch(error => {
                console.error('Error:', error);
                clearInterval(intervalID);
            });
        }
    })
</script>

new version
<script>
    //dropdown show list
    const dropdownButton = document.querySelector('#dropdown_speech');
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        $(item).click(function(e) {
            e.preventDefault();
            dropdownButton.textContent = item.textContent;
        });

    });

    $(".show_detect").css("display", "none");
    let intervalID;

    $(".btn_start").click(function(e) {
        e.preventDefault();
        $(".btn_start").hide();
        $(".show_detect").css("display", "block");

        //open video to detect text in camera
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');

        navigator.mediaDevices.getUserMedia({
            video: true
        }).then(stream => {
            video.srcObject = stream;
            video.play();
        }).catch(error => console.error('Could not access camera:', error));

        // start detecting text
        intervalID = setInterval(detectText, 5000);

        function detectText() {
            // get image data and send to python file to check text
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL("image/png");

            fetch("/detect-text", {
                    method: "POST",
                    body: JSON.stringify({
                        imageData: imageData,
                    }),
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status !== "success") {
                        clearInterval(intervalID);
                        handleFailure();
                    } else {
                        clearInterval(intervalID);
                        handleSuccess(data.text);
                    }
                })
                .catch((error) => {
                    clearInterval(intervalID);
                    console.error("Could not detect text:", error);
                });
        }

        function handleFailure() {
            Swal.fire({
                position: "top",
                icon: "error",
                title: "ไม่สามารถค้นหาข้อความได้",
                text: "กรุณาลองอีกครั้งใน 5 วินาที",
                timer: 5000,
                timerProgressBar: true,
                showConfirmButton: false,
                willClose: () => {
                    intervalID = setInterval(detectText, 5000);
                },
            });
        }

        function handleSuccess(text) {
            Swal.fire({
                icon: "success",
                title: "ข้อความของคุณคือ",
                text: text,
                showConfirmButton: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    playAudio(text);
                }
            });
        }
    });


    function playAudio(text) {

        // setup api parameter
        let urlAPI = 'https://api.aiforthai.in.th/vaja9/synth_audiovisual';
        var setting_API = {
            url: urlAPI,
            method: "POST",
            headers: {
                "Apikey": "letBGyiaspJ9ERccDfEB5R4vKeCMKfQy",
                "Content-Type": "application/json",
            },
            data: JSON.stringify({
                input_text: text,
                speaker: 0,
                phrase_break: 0,
                audiovisual: 0,
            })
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
                audioSource.onended = onFinished;
                audioSource.play();
            }
        }

        // Make an API call to generate the audio file
        $.ajax(setting_API).done(function(response) {
            // check status
            console.log(response);
            if (response.msg == "success") {
                Swal.fire({
                    icon: 'success',
                    title: 'เสียงของคุณพร้อมแล้ว!',
                    text: 'คลิกเพื่อฟัง',
                    confirmButtonText: 'เล่นเสียง',
                    allowOutsideClick: false,
                }).then((result) => {
                    if (result.isConfirmed) {
                        clearInterval(intervalID)
                        play_wav(response.wav_url);
                    }
                });
            } else {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'ไม่สามารถสร้างเสียงได้',
                    text: 'กรุณาลองอีกครั้งในภายหลัง',
                    allowOutsideClick: false,
                });
            }
        }).fail(function(jqXHR, textStatus) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'ไม่สามารถเชื่อมต่อ API ได้',
                text: 'กรุณาลองใหม่ในภายหลัง',
                confirmButton: false,
                timer: 3000,
                timerProgressBar: true,
            });

            setTimeout(function() {
                window.location.href = '/detect';
            }, 3000);
        });

        function onFinished() {
            const btnListen = document.createElement("button");
            let audioSRC = document.getElementById('audio')
            btnListen.className = "btn_listen w-100 mt-3";
            btnListen.textContent = "เสร็จสิ้นการฟังเสียง";
            $(".show_detect").append(btnListen);
            btnListen.addEventListener("click", function() {
                audioSRC.src = ""
                $(".btn_listen").hide();
                window.location.reload();
            });

        }

    }
</script>

