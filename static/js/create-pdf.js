const $pdfFileInput = $("#pdf-file-input");
const $pdfPreviewContainer = $("#pdf-preview-container");

$pdfFileInput.on("change", function() {

  const selectedFile = $pdfFileInput[0].files[0];


  const fileReader = new FileReader();

  fileReader.onload = function() {

    const arrayBuffer = fileReader.result;


    pdfjsLib.getDocument(arrayBuffer).promise.then(function(pdf) {

      pdf.getPage(1).then(function(page) {

        const canvas = document.createElement("canvas");
        const canvasContext = canvas.getContext("2d");


        const viewport = page.getViewport({ scale: 0.5 });
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        const renderContext = {
          canvasContext,
          viewport,
        };
        page.render(renderContext).promise.then(function() {

          $pdfPreviewContainer.empty().append(canvas);
        });
      });
    });
  };

  fileReader.readAsArrayBuffer(selectedFile);
});