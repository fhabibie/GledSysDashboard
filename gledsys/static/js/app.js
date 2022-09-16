// APP.JS

(function($) {
    'use strict';
    
    const uploadForm = $('#upload-form');
    const inputFiles = $('#id_files');
    const progressBar = $('#upload-progress-bar');
    const uploadBtn = $('#upload-btn')

    uploadForm.change(function(e) {
        e.preventDefault();
        const csvs = inputFiles[0].files;
        if (csvs.length > 0) uploadBtn.attr('disabled', false);
        // TODO: handle validation of filename format in YYYYMMDD


    });

    // Handle upload files
    uploadForm.submit(function(e) {
        e.preventDefault();
        const fd = new FormData();
        const csvs = inputFiles[0].files;
        $.each(csvs, function(i, file) {
            fd.append('files[]', file)
        });
        // Reset progress bar
        $('#uploaded-bar').css("width", `0%`);
        $('#uploaded-bar').text(`0%`);
        $.ajax({
            type: 'POST',
            url: uploadForm.action,
            enctype: 'multipart/form-data',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            data: fd,
            beforeSend: function() {
                progressBar.removeClass('d-none');
            },
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        var percent = (e.loaded / e.total) * 100;
                        $('#uploaded-bar').css("width", `${percent.toFixed(1)}%`);
                        $('#uploaded-bar').text(`${percent.toFixed(1)}%`);
                        console.log(percent);
                        if(percent === 100) {
                            console.log('waiting...')
                            $('#uploaded-bar').text('Importing csv into database...');
                        }
                    }
                });
                return xhr;
            },
            success: function(res) {
                uploadForm[0].reset();
                progressBar.addClass('d-none');
                $('#alert-container').append(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>Success!</strong> Your file(s) has been successfully uploaded.
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>`);

            },
            error: function(err) {
                console.log(err)
            },
            processData: false,
            caches: false,
            contentType: false,

        });
    });

    // Utils Get Cookies
    function getCookie(name) {
        var cookieValue = null;
    
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
    
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    
                    break;
                }
            }
        }
    
        return cookieValue;
    }

})(jQuery)
// Handle upload files