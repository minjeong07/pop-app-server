// 1 번째 방법!
// const container = document.querySelector(".background");
// const box = container.querySelectorAll(".area_box");
//
// const {width: containerWidth, height: containerHeight} =
//     container.getBoundingClientRect();
// const {width: boxWidth, height: boxHeight} =
//     box.getBoundingClientRect();
// let isDragging = null;
// let originLeft = null;
// let originTop = null;
// let originX = null;
// let originY = null;
//
// box.addEventListener("mousedown", (e) => {
//     isDragging = true;
//     originX = e.clientX;
//     originY = e.clientY;
//     originLeft = box.offsetLeft;
//     originTop = box.offsetTop;
// });
//
//
// document.addEventListener("mousemove", (e) => {
//     if (isDragging) {
//         const diffX = e.clientX - originX;
//         const diffY = e.clientY - originY;
//         const end0fXPoint = containerWidth - boxWidth;
//         const end0fYPoint = containerHeight - boxHeight;
//         box.style.left = `${Math.min(Math.max(0, originLeft + diffX), end0fXPoint)}px`;
//         box.style.top = `${Math.min(Math.max(0, originTop + diffY), end0fYPoint)}px`;
//     }
// });
//
// document.addEventListener("mouseup", (e) => {
//     isDragging = false;
//
// });

// 2번째 방법
const container = document.querySelector(".background");
const box = container.querySelectorAll(".change_num");

const {width: containerWidth, height: containerHeight} =
    container.getBoundingClientRect();

for (let i = 0; box.length; i++) {
    const {width: boxWidth, height: boxHeight} =
        box[i].getBoundingClientRect();
    let isDragging = null;
    let originLeft = null;
    let originTop = null;
    let originX = null;
    let originY = null;

    box[i].addEventListener("mousedown", (e) => {
        isDragging = true;
        originX = e.clientX;
        originY = e.clientY;
        originLeft = box[i].offsetLeft;
        originTop = box[i].offsetTop;
    });


    box[i].addEventListener("mousemove", (e) => {
        if (isDragging) {
            const diffX = e.clientX - originX;
            const diffY = e.clientY - originY;
            const end0fXPoint = containerWidth - boxWidth;
            const end0fYPoint = containerHeight - boxHeight;
            box[i].style.left = `${Math.min(Math.max(0, originLeft + diffX), end0fXPoint)}px`;
            box[i].style.top = `${Math.min(Math.max(0, originTop + diffY), end0fYPoint)}px`;
        }
    });

    box[i].addEventListener("mouseup", positionhandler);

    // 여기에 ajax씀, url로 보내면 views함수가 실행됨 (origin left top)

    async function positionhandler(event) {
        let id = this.id
        let top = this.style.top
        let left = this.style.left
        // console.log('id', id)
        isDragging = false;

        let data = new FormData()
        data.append("id", id)
        data.append("top", top.split("p")[0])
        data.append("left", left.split("p")[0])

        let r = await fetchmsg(data)
        let code = await r.status
        if (code === 200) {
            let jsondata = await r.json()
            window.location.href = jsondata.url
        }

    }
}


function fetchmsg(data) {
    return new Promise((receive) => {
        fetch("/api/v1/card/deco/move/", {
            method: "POST",
            body: data,
            credentials: 'same-origin',
        }).then((response) => {
            receive(response);
        }).catch((err) => {
            console.info(err);
        });
    });
}


// 3번째 방법!
// $(document).ready(function () {
//     let $container = $(".background");
//     let $banner_img = $(".background img");
//     let img_left = 0;
//     let img_top = 0;
//     let mouse_state = false;
//
//     $banner_img.each(function () {
//         img_left = Math.random() * ($container.width() - $(this).width());
//         img_top = Math.random() * ($container.height() - $(this).width());
//         $(this).css({
//             left: img_left,
//             top: img_top
//         });
//     });
//
//     $banner_img.mousedown(function (e) {
//         let container_x = $container.offset().left;
//         let container_y = $container.offset().top;
//         $(this).css({
//             left: e.clientX - container_x - ($banner_img.width() / 2),
//             top: e.clientY - container_y - ($banner_img.height() / 2)
//         });
//         mouse_state = true;
//     });
//
//     $banner_img.mousemove(function (e) {
//         let container_x = $container.offset().left;
//         let container_y = $container.offset().top;
//
//         if (mouse_state === true) {
//             $(this).css({
//                 left: e.clientX - container_x - ($banner_img.width() / 2),
//                 top: e.clientY - container_y - ($banner_img.height() / 2)
//             });
//         }
//     });
//
//     $banner_img.mouseup(function (e) {
//         mouse_state = false;
//     });
// });

function clip() {
    let url = '';
    const textarea = document.createElement("textarea");
    document.body.appendChild(textarea);
    url = window.document.location.href;
    textarea.value = url;
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    alert("URL이 복사되었습니다.")
}

