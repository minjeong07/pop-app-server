function eventHandler(e) {
    const $eTarget = $(e.currentTarget);
    if ($eTarget.hasClass("active") === true) {
        $eTarget.attr("aria-selected", false).removeClass("active");
    } else if ($eTarget.hasClass("active") === false) {
        $eTarget.attr("aria-selected", true).addClass("active"); // 구버전 IE
    }
}

function getitem() {
    var rr = [];
    var l = 0;
    for (var i = 1; i < 11; i++) {
        var t = "#tag" + i; //태그10번까지 탐색
        var tag = $(t);
        if (tag.hasClass("active") === true) {
            //클릭된 요소는 active라는 클래스가 추가되므로 이를이용하여 판별
            let tagg = tag.text().split("\n", 1); //널문자 제거를위해 \n을기준으로 자름
            rr[l] = tagg;
            // alert(rr[l]);
            l += 1; //클릭된 요소가 있을때만 추가되도록 설정
        }
    }

    for (let i = 0; i < rr.length; i++) {
        var temp = "taginput" + i;
        var temphtml = `<input type="text" id= "${temp}" style="display: none;"  name="${temp}" >`;
        var temp2 = "#" + temp;
        $("#tempspace").append(temphtml);
        $(temp2).val(rr[i]);
    }
    var tag_count_html = `<input type="text" id= "tag_count" style="display: none;"  name="tag_count" >`;
    $("#tempspace").append(tag_count_html);
    $("#tag_count").val(rr.length);
}

$('[role="option"]').on("click", eventHandler);
$('[role="button"]').on("click", getitem);

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#blah").attr("src", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

const originTags = Array.from(document.querySelectorAll("#hidden_origin_tags li"))
const tagList = Array.from(document.querySelectorAll(".tag-item"))
originTags.forEach(element => {
    tagList.forEach(e => {
        if (element.innerText === e.innerText) {
            e.className = "tag-item active";
        }
    })
})


function preview(input) {
    const validExtensions = ["image/jpeg", "image/jpg", "image/png", "image/JPG", "image/JPEG", "image/PNG"];
    const new_image = input.files[0];
    const type = new_image.type
    if (validExtensions.includes(type)) {
        const profile = document.getElementById('blah');
        profile.src = URL.createObjectURL(new_image);
    } else {
        alert("이미지 파일만 업로드할 수 있습니다")
        window.location.href = '/mypage/'
    }
}