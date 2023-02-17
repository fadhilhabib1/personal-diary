$(document).ready(function () {
    listing();
});

function saving() {
    let img_title = $('#image-title').val();
    let img_desc = $('#image-description').val();
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();


    today = mm + '-' + dd + '-' + yyyy;

    $.ajax({
        type: 'POST',
        url: '/diary',
        data: {
            title: img_title,
            description: img_desc,
            date: today,
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function listing() {
    $.ajax({
        type: 'GET',
        url: '/diary',
        data: {},
        success: function (response) {
            let rows = response['diarys'];
            $('#cards-box').empty();
            for (let i = 0; i < rows.length; i++) {
                let image = rows[i]['image'];
                let title = rows[i]['title'];
                let description = rows[i]['description'];
                let dates = rows[i]['dates'];

                let temp_html = `<div class="col">
                <div class="card">
                    <img src="${image}"
                        class="card-img-top">
                    <div class="card-body">
                        <h5 class="card-title">${title}</h5>
                        <p class="card-text">${description}</p>
                        <h6 class="card-subtitle mb-2 text-muted">${dates}</h6>
                    </div>
                </div>
            </div>`;
                $('#cards-box').append(temp_html);
            }
        }
    })
}