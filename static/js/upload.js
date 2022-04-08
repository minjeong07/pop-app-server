function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah2').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }


}

let today = new Date();
let hours = ('0' + today.getHours()).slice(-2);
let minutes = ('0' + today.getMinutes()).slice(-2);
let seconds = ('0' + today.getSeconds()).slice(-2);
let timeString = hours + '_' + minutes + '_' + seconds;

function kandinsky() {
    let title = 'kan' + timeString
    let file = $('#uploaded_file')[0].files[0]
    let form_data = new FormData()

    form_data.append("key", title)
    form_data.append("img", file)
    $.ajax({
        type: "POST",
        url: "http://nst10-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/nsts/",
        dataType: 'json',
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            let urls = response['file_url']

           $('#card-cadin-select1').attr('src', urls)

        }
    })
}



function close_box() {
    $('#blank').hide()
    $('#card-cadin-select1').show()
}

function close_box2() {
    $('#blank2').hide()
    $('#blah2').show()


}