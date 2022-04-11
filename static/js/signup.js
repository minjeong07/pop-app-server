const username = document.getElementById('username')
const password = document.getElementById('password')
const checkPassword = document.getElementById('password2')
const bio = document.getElementById('bio')
const errorBox = document.getElementById('error')
const messageBox = document.getElementById('pointer')
const btn = document.getElementById('signup-btn')

$(document).ready(function () {
    if (username.value.replace(/(\s*)/g, "") === "") {
        messageBox.innerText = "이름은 필수 입력사항 입니다"
        $('#pointer').show();
    }
    $('#error').hide();
    $('#signup-btn').attr('disabled', 'true')
})

function valid_username(username) {
    const regex = /^[a-zA-Z가-힣ㄱ-ㅎㅏ-ㅣ]+[0-9a-zA-Z가-힣ㄱ-ㅎㅏ-ㅣ_-]{1,}$/;
    return regex.test(username)
}

function valid_password(password) {
    const regex = /^[a-z0-9_-]{8,}$/;
    return regex.test(password)
}

function double_check_password(password, checkPassword) {
    return password === checkPassword;
}

function valid_bio(bio) {
    const regex = /^.{1,120}$/
    return regex.test(bio)
}

username.addEventListener('keyup', function () {
    if (!valid_username(username.value)) {
        errorBox.innerText = "이름은 한글,영어(+숫자)로 최소 2자 이상으로 설정해 주세요";
        $('#error').show();
        $('#pointer').hide();
    } else {
        $('#error').hide();
        $('#pointer').hide();
    }
    btn.disabled = !(valid_username(username.value) && valid_password(password.value) && double_check_password(password.value, checkPassword.value) && valid_bio(bio.value));
})

password.addEventListener('keyup', function () {
    if (!valid_password(password.value)) {
        errorBox.innerText = "비밀번호는 8자 이상으로 설정해 주세요"
        $('#error').show();
        $('#pointer').hide();
    } else {
        $('#error').hide();
    }
    btn.disabled = !(valid_username(username.value) && valid_password(password.value) && double_check_password(password.value, checkPassword.value) && valid_bio(bio.value));
})

checkPassword.addEventListener('keyup', function () {
    if (!double_check_password(password.value, checkPassword.value)) {
        errorBox.innerText = "비밀번호가 일치하지 않습니다";
        $('#error').show();
        $('#pointer').hide();
    } else if (bio.value.replace(/(\s*)/g, "") === "") {
        messageBox.innerText = "소개글을 작성해 주세요"
        $('#error').hide();
        $('#pointer').show();
    } else {
        $('#error').hide();
        $('#pointer').hide();
    }
    btn.disabled = !(valid_username(username.value) && valid_password(password.value) && double_check_password(password.value, checkPassword.value) && valid_bio(bio.value));
})

bio.addEventListener('keyup', function () {
    if (!valid_bio(bio.value)) {
        errorBox.innerText = "소개글을 120자 이내로 작성해 주세요";
        $('#error').show();
        $('#pointer').hide();
    } else {
        $('#error').hide();
        $('#pointer').hide();
    }
    btn.disabled = !(valid_username(username.value) && valid_password(password.value) && double_check_password(password.value, checkPassword.value) && valid_bio(bio.value));
})