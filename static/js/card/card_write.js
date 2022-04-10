// 페이지간 이동
const deco_page = document.querySelector("#deco_page");
const deco_prev = document.querySelector("#deco_prev");
const deco_next = document.querySelector("#deco_next");

const msg_page = document.querySelector("#msg_page");
const msg_prev = document.querySelector("#msg_prev");
const msg_next = document.querySelector("#msg_next");

const gift_page = document.querySelector("#gift_page");
const gift_prev = document.querySelector("#gift_prev");
const gift_next = document.querySelector("#gift_next");

const view_page = document.querySelector("#view_page");
const view_prev = document.querySelector("#view_prev");
const view_next = document.querySelector("#view_next");

deco_next.addEventListener("click", ()=>{deco_page.className = "sub_container moved";});
deco_prev.addEventListener("click",()=>{
    window.location.pathname = toUserId
})

msg_prev.addEventListener("click", ()=>{deco_page.className = "sub_container back";});        
gift_prev.addEventListener("click", ()=>{msg_page.className = "sub_container back";});        
view_prev.addEventListener("click", ()=>{gift_page.className = "sub_container back";});
// 장식페이지
// function readImage(input) {
//     // 인풋 태그에 파일이 있는 경우
//     if(input.files && input.files[0]) {
//         // FileReader 인스턴스 생성
//         const reader = new FileReader();
//         // 이미지가 로드가 된 경우
//         reader.onload = (event) => {
//             const previewImage = document.getElementById("preview_image")
//             previewImage.src = event.target.result
//         };
//         // reader가 이미지 읽도록 하기
//         reader.readAsDataURL(input.files[0]);
//     }
// };

// const customImage = document.getElementById("custom_image")
// customImage.addEventListener("change", (event) => {
//     readImage(event.target)
// });

const previewImage = document.getElementById("preview_image")
const decoList = Array.from(document.querySelector(".deco_selec_wrap").children);

decoList[0].className = "deco_selec selected"
previewImage.src = decoList[0].firstChild.src
previewImage.alt = decoList[0].firstChild.alt

decoList.forEach(element => {
    element.addEventListener("click", (e) => {
        decoList.forEach(el => {
            el.className = "deco_selec"
        })
        if (e.target.className === "deco_selec") {
            previewImage.src = e.target.firstChild.src
            previewImage.alt = e.target.firstChild.alt
            e.target.className = "deco_selec selected"
        } else if (e.target.className === "deco_radio_img"){
            previewImage.src = e.target.src
            previewImage.alt = e.target.alt
            e.target.parentNode.className = "deco_selec selected"
        }
        
    
    })
});



// 메시지 페이지
const pathname = window.location.pathname
const toUserId = pathname.split("/")[pathname.split("/").length - 1]
const msgNext = document.getElementById("msg_next")
const message = document.getElementById("message")
const messageResult = document.getElementById("message_result")
const modal_wrap = document.createElement("div")
modal_wrap.className = "modal_wrap"
modal_wrap.innerHTML = "<div class='modal_div'><div class='modal_text'>잠시만 기다려 주세요</div></div>"


function fetchRecommend(data) {
    return new Promise((receive) => { 
        fetch("/api/v1/card/", {
            method:"POST",
            body: data,
            credentials: 'same-origin',
            redirect: "follow",
        }).then((response) => {
            receive(response.json());
        }).catch((err)=>{
            console.info(err);
        }); 
    }); 
}

async function postToGift() {
    let data = new FormData();
    data.append("id", toUserId);
    data.append("msg", message.value);
    // data.append('csrfmiddlewaretoken', csrftoken);
    document.querySelector("body").appendChild(modal_wrap);

    let jsonData = await fetchRecommend(data);
    showRecommendList(jsonData);
    // console.log(jsonData);
    document.querySelector("body").removeChild(document.querySelector(".modal_wrap"));
    msg_page.className = "sub_container moved";
}

async function msgToGift() {
    if (message.value.length > 0) {
        messageResult.value = message.value
        await postToGift();
    } else {
        alert("메시지를 입력하세요");
    };
}

msgNext.addEventListener("click", msgToGift);

// 선물 페이지
const $search = document.querySelector("#search_gift")
const $searchButton = document.querySelector(".search_button")
const $glCont = document.querySelector(".gift_list_container_wrap")
const $gcCont = document.querySelector(".gift_cont_container")
const $gsCont = document.querySelector(".gift_search_container")
let giftWrap = document.querySelectorAll(".gift_box_wrap");


function showRecommendList(jsondata) {
    $gcCont.innerHTML = ""
    $gsCont.innerHTML = ""
    // let tagList = jsondata.slice(1);

    let reList = [jsondata.slice(0,8)];
    reList.forEach(giftList => {
        let $reListCon = document.createElement("div")
        $reListCon.className = "gift_box_container"
        $reListCon.innerHTML = '<div class="gift_tag">메시지 기반 추천 선물</div>'
        let $reWrap = document.createElement("div")
        $reWrap.className = "gift_box_wrap"
        $reListCon.appendChild($reWrap)
        giftList.forEach(e => {
            let gBox = document.createElement("div")
            gBox.className = "gift_box"
            // gBox.innerHTML = `<img src="${e.gift_img}" alt="${e.id}" class="gift_img"><div class="gift_img_name">${e.gift_name}</div>`
            gBox.innerHTML = `<img src="${e.gift_img}" alt="${e.id}" class="coupon_img"/><div style="display: none;">${e.gift_name}</div>`
            $reWrap.append(gBox)
        });
        $gcCont.appendChild($reListCon)
        giftWrap = document.querySelectorAll(".gift_box_wrap");
        giftWrap.forEach(element => {
            element.addEventListener("click", giftSelect)
        });
    });

    let tagList = [jsondata.slice(8,)];
    if (tagList[0].length != 0) {
        tagList.forEach(giftList => {
            let $reListCon = document.createElement("div")
            $reListCon.className = "gift_box_container"
            $reListCon.innerHTML = '<div class="gift_tag">유저 선호 태그 관련 선물</div>'
            let $reWrap = document.createElement("div")
            $reWrap.className = "gift_box_wrap"
            $reListCon.appendChild($reWrap)
            giftList.forEach(e => {
                let gBox = document.createElement("div")
                gBox.className = "gift_box"
                gBox.innerHTML = `<img src="${e.gift_img}" alt="${e.id}" class="gift_img"><div class="gift_img_name">${e.gift_name}</div>`
                $reWrap.append(gBox)
            });
            $gcCont.appendChild($reListCon)
            giftWrap = document.querySelectorAll(".gift_box_wrap");
            giftWrap.forEach(element => {
                element.addEventListener("click", giftSelect)
            });
        });
    } else {
        let $reListCon = document.createElement("div")
        $reListCon.className = "gift_box_container"
        $reListCon.innerHTML = '<div class="gift_tag">유저의 선호 태그가 없습니다.</div>'
        $gcCont.appendChild($reListCon)
    }
}

function fetchSearch(data) {
    return new Promise((receive) => {
        fetch("/api/v1/card/search/", {
            method:"POST",
            body: data,
            credentials: 'same-origin',
            redirect: "follow",
        }).then((response) => {
            receive(response);
        }).catch((err)=>{
            console.info(err);
        });
    });
}

function showSearchList(jsondata) {
    // console.log(jsondata)
    $gsCont.innerHTML = ""
    let $reListCon = document.createElement("div")
    $reListCon.className = "gift_box_container"
    $reListCon.innerHTML = '<div class="gift_tag">검색 결과</div>'
    let $reWrap = document.createElement("div")
    $reWrap.className = "gift_box_wrap"
    $reListCon.appendChild($reWrap)
    jsondata.forEach(e => {
        let gBox = document.createElement("div")
        gBox.className = "gift_box"
        gBox.innerHTML = `<img src="${e.gift_img}" alt="${e.id}" class="gift_img">${e.gift_name}`
        $reWrap.append(gBox)
    });
    $gsCont.appendChild($reListCon);
    giftWrap = document.querySelectorAll(".gift_box_wrap");
    giftWrap.forEach(element => {
        element.addEventListener("click", giftSelect)
    });

}


function showSearchErr(jsondata) {
    // console.log(jsondata)
    $gsCont.innerHTML = ""
    let $reListCon = document.createElement("div")
    $reListCon.className = "gift_box_container"
    $reListCon.innerHTML = `<div class="gift_tag">${jsondata.err_msg}</div>`
    $gsCont.appendChild($reListCon);
    giftWrap = document.querySelectorAll(".gift_box_wrap");
    giftWrap.forEach(element => {
        element.addEventListener("click", giftSelect)
    });
}


async function searchGift() {
    let keyword = $search.value
    let data = new FormData();
    data.append("keyword", keyword);

    let response = await fetchSearch(data);
    let code = await response.status
    let jsondata = await response.json()
    if (code === 200) {
        showSearchList(jsondata);
    } else {
        showSearchErr(jsondata);
    }
    $glCont.scrollTo(0,0)
}

$search.addEventListener('keyup', (e)=>{
    if (e.keyCode === 13) {
        searchGift();
    }
});

$searchButton.addEventListener("click", searchGift)

function nameSelectedGift() {
    try {
        let giftSelected = document.getElementsByClassName("gift_box selected_gift")[0];
        let $src = giftSelected.firstChild.src;
        gift_next.innerHTML = `<div class="gift_button_span">${giftSelected.innerText}</div><div class="gift_button_span_two"> 선택하기</div>`

    } catch (error) {
        gift_next.innerHTML = `<div class="gift_button_span_two">선물을 선택하세요</div>`
    }
}


function giftSelect(event) {
    // console.info(event)
    giftWrap.forEach(el => {
        Array.from(el.children).forEach(e=>{
            e.className = "gift_box"
        })
    })
    if (event.target.className === "gift_img" || event.target.className === "coupon_img"){
        event.target.parentNode.className = "gift_box selected_gift"
    } else if (event.target.className === "gift_box_wrap") {
    } else if (event.target.className === "gift_box") {
        event.target.className = "gift_box selected_gift"
    }
    nameSelectedGift()
}

giftWrap.forEach(element => {
    element.addEventListener("click", giftSelect)
});



function giftPageMoved() {
    let giftSelected = document.getElementsByClassName("gift_box selected_gift")[0];
    try {
        $previewImage.src = giftSelected.firstChild.src;
        $previewImage.alt = giftSelected.firstChild.alt;
        gift_page.className = "sub_container moved";
        title.value = giftSelected.innerText;
    } catch (error) {
        alert("선물을 선택하세요!")
    }

}


gift_next.addEventListener("click", giftPageMoved);

// 미리보기 페이지
const title = document.querySelector("#title")
const author = document.querySelector("#author")
const csrftoken = document.querySelector("#cs input").value;
const $previewImage = document.getElementById("preview_img")
const titleBtn = document.querySelector("#title_btn")
const authorBtn = document.querySelector("#author_btn")

titleBtn.addEventListener("click", ()=>{
    title.select()
})

authorBtn.addEventListener("click", ()=>{
    author.select()
})



function fetchPostMessage(data) {
    return new Promise((receive) => {
        fetch(pathname, {
            method:"POST",
            body: data,
            credentials: 'same-origin',
            redirect: "follow",
        }).then((response) => {
            receive(response.json());
        }).catch((e)=>{
            console.info(err + " url : " + url);
        });
    });
}


async function postMessage(event) {
    let clickTime = event['timeStamp'];
    if (clickTime && (clickTime - _lastClickTime) < 100) {
        let giftSelected = document.getElementsByClassName("gift_box selected_gift")[0]
        let giftId = giftSelected.firstChild.alt
        let decoSelected = previewImage.src.split("?")[0]
        if (title.value === "") {
            return alert("상품 제목을 붙여주세요!")
        } else if (author.value === "") {
            return alert("보내는 이를 적어주세요!")
        }

        let data = new FormData();
        data.append("csrfmiddlewaretoken", csrftoken)
        data.append("to_user_id", toUserId)
        data.append("gift_id", giftId)
        data.append("msg", message.value)
        data.append("deco", decoSelected)
        data.append("title", title.value)
        data.append("author", author.value)

        let server_msg = await fetchPostMessage(data)
        console.log(server_msg)
        alert(server_msg.server)
        window.location.pathname = toUserId
    };
    console.log("clicked")
    _lastClickTime = clickTime;
}

// 353*720
let _lastClickTime = new Date().getTime();

view_next.addEventListener("click", postMessage)