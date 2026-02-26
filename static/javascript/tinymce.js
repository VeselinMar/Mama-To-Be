document.addEventListener("DOMContentLoaded", function() {
    tinymce.init({
        selector: 'textarea',
        height: 500,
        width: '100%',
        plugins: 'advlist autolink lists link image charmap preview hr pagebreak ' +
                 'searchreplace wordcount visualblocks visualchars code fullscreen ' +
                 'media nonbreaking save table directionality ' +
                 'emoticons paste textpattern imagetools autoresize',
        toolbar: 'undo redo | styleselect formatselect | bold italic underline strikethrough | ' +
                 'alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | ' +
                 'link image media | preview fullscreen | charmap emoticons',
        image_advtab: true,
        media_live_embeds: true,
        automatic_uploads: true,
        images_reuse_filename: false,
        file_picker_types: 'image',
        images_upload_url: '/upload-image/',
        file_picker_callback: function(callback, value, meta) {
            window.open('/file-picker/', '_blank');
        },
        content_style: "body { font-family: Arial, Helvetica, sans-serif; font-size: 14px; }",
        font_family_formats: 
            'Arial=arial,helvetica,sans-serif;' +
            'Arial Black=arial black,avant garde;' +
            'Times New Roman=times new roman,times;' +
            'Courier New=courier new,courier;' +
            'Roboto=Roboto,sans-serif;' +
            'Open Sans=Open Sans,sans-serif',
        font_size_formats: '10px 12px 14px 16px 18px 24px 36px',
    });
});