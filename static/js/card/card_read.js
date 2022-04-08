$(document).ready(function () {
    $('#modal').hide();
    $('.popup').hide();
})

// 기프티콘 미리보기 이미지 클릭 시 모달 나오게
jQuery('.preview').click(function () {
    if ($('.popup').css('display') === 'none') {
        jQuery('.popup').show();
    } else {
        jQuery('.popup').hide();
    }
});
// 기프티콘 모달 끄기
jQuery('#close-icon').click(function () {
    $('.popup').hide();
})

// '삭제' 클릭하면 모달 나오게
jQuery('#delete-btn').click(function () {
    if ($('#modal').css('display') === 'none') {
        jQuery('#modal').show();
    } else {
        jQuery('#modal').hide();
    }
});

// 삭제 확인 모달에서 '아니요' 클릭하면 모달 끄기
jQuery('#close-modal').click(function () {
    $('#modal').hide();
});

// 카드 삭제하기
function delete_message() {
    const url = window.location.href;
    const arr = url.split('/');
    window.location.replace(`https://paperonpresent.com/card/delete/${arr[5]}`);
    // window.location.replace(`http://127.0.0.1:8000/card/delete/${arr[5]}`);
}
