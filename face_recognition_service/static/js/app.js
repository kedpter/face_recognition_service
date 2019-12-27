$(document).ready(function() {
    $('#add_encoding_form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
        url: 'api/v1/face/encodings',
        type: 'POST',
        data: formData,
        success: function (data) {
            alert('Success');
        },
        error: function(xhr, status, error) {
            var json = JSON.parse(xhr.responseText);
            var msg = "unknown error";
            if (json != null)
            {
                msg = JSON.stringify(json);
            }
            alert('Fail:' + msg);
        },
        cache: false,
        contentType: false,
        processData: false
    });

    });

    $('#recognize_form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
        url: 'api/v1/face/comparison/distances',
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function (data) {
            var json = data;
            // console.log(json);
            var min = 1;
            var msg = "No match id";
            var user_id = null;
            for (var key in json){
                if (json[key] < min)
                {
                    min = json[key];
                    user_id = key;
                }
            }
            // console.log(user_id);
            if (user_id != null)
            {
                msg = "Find match: " + user_id;
            }
            alert(msg);
            // loop json items
            // find the minimum value
            // print id
        },
        error: function(xhr, status, error) {
        },
        cache: false,
        contentType: false,
        processData: false
    });

    });


});
