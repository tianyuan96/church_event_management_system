$("#add_option").click(function (e) {
    e.preventDefault();

    var form = $("#survey_form")[0];
    var formData = new FormData(form);
    formData.append('files', $('#option_imageFile').get(0).files[0]);
    formData.append('operation',"add_option");
    alert(CKEDITOR.instances["id_description"]);
    alert(CKEDITOR.instances['id_description'].getData());
    formData.append('description', CKEDITOR.instances.id_description.getData());

    $.ajax(
        {
            type:"POST",
            url : "/survey/create/"+surveyId+"/"+eventId+"/",
            cache: false,
               contentType: false,
               processData: false,
             processData: false,
             dataType: 'html',
            data:formData,
            success: function(response) {
                $("#choices_container").html(response);
            }
        }

    );
});
