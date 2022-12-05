function likeCounters() {

    var headers = new Headers();
    var csrftoken = getCookie('csrftoken');
    headers.append('X-CSRFToken', csrftoken);
    headers.append('Accept', 'application/json, text/plain, */*');
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    fetch("/api/LikeApi/", {
        method: "PUT",
        headers: headers,
        body: JSON.stringify({
            userId: 1,
        }),
    })
    .then(function(response){
          if (response.status === 200){
              LikeButtonChange()
          }else{
              window.location.replace('/accounts/login/')
          }
      })

    }
/*
function LikeButtonChange() {
    var pastButtonText = document.getElementById('like-button').innerText
    if (pastButtonText == 'LIKE💛'){
        document.getElementById('like-button').innerHTML = 'UNLIKE🤍'
    }else{
        document.getElementById('like-button').innerHTML = 'LIKE💛'
    }
}
*/
function LikeButtonChange() {
    var pastButtonText = document.getElementById('like-button').getAttribute('data')
    if (pastButtonText === '1'){
        document.getElementById('like-button').innerHTML = 'UNLIKE🤍'
        document.getElementById('like-button').setAttribute('data','0')
    }else{
        document.getElementById('like-button').innerHTML = 'LIKE💛'
        document.getElementById('like-button').setAttribute('data','1')

    }
}


function commentsInit() {
    fetch("/api/CommentsApi/")
        .then((response) => response.json())
        .then((data) => loadComments(data))
}


function loadComments(data) {
//dom 복제
    clearCommentsDom()
    let commentItems = document.getElementById('dummy').querySelector('.comments_item')
    let commentList = document.getElementById('comments_list')
    for (var i = 0; i<data.length; i++){
        let cloneNodes = commentItems.cloneNode(true)
        commentList.appendChild(cloneNodes)
    }


//dom에 데이터 채우기
    for (var i =0; i<data.length; i++){
        document.querySelectorAll('.comments_item_body')[i].innerText = data[i].body
        document.querySelectorAll('.comments_item_author')[i].innerText = data[i].username
        document.querySelectorAll('.comments_item_created')[i].innerText = data[i].created_at
    }
}



function clearCommentsDom() {
    let commentList = document.getElementById('comments_list')
    commentList.innerHTML = ""
}


function postComment(){
    let targetTitle = document.getElementById('comment_body').value
    var headers = new Headers();
    var csrftoken = getCookie('csrftoken');
    headers.append('X-CSRFToken', csrftoken);
    headers.append('Accept', 'application/json, text/plain, */*');
    headers.append('Content-Type', 'application/x-www-form-urlencoded');

    if (document.getElementById('comment_body').value.length < 10 ){
        console.log(document.getElementById('comment_body').value.length)
        alert('내용을 입력해 주세요!')
    }else{
        fetch("/api/CommentsApi/", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                body: targetTitle,
            }),
        })
        .then(() => {
            document.getElementById('comment_body').value=""
            commentsInit()
        })
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// 이미지 관련

function imageInit() {
    fetch("/api/uploader/")
      .then((response) => response.json())
      .then((data) => displayImage(data));
}

function displayImage(data) {
    document.getElementById("updatedImg").innerHTML=""
    var imageList = document.getElementById("updatedImg")
    var imageBlock = document.getElementById('thumb_dummy').querySelector(".uk-inline")
    var cnt = 0
    for (var item of data['img']){
        var cloneNodes = imageBlock.cloneNode(true)

        //close button - 이미지 삭제 api
        var part_btn = cloneNodes.childNodes.item(1).childNodes.item(1).childNodes.item(1)
        part_btn.setAttribute(`onclick`, `onDeleteImage(this)`)
        part_btn.setAttribute('data', cnt)

      //이미지
        var part_img = cloneNodes.childNodes.item(1).childNodes.item(3)
        part_img.setAttribute('src', item)
        part_img.setAttribute('onclick', 'window.navigator.clipboard.writeText("http://" + window.location.host + this.getAttribute("src")).then(() => {copiedText()});')
        imageList.appendChild(cloneNodes)

        cnt += 1

    }
}


function copiedText() {
    alert("이미지 주소를 복사했습니다. ")
}


function setThumbnail() {

    let file = document.getElementById('image').files[0];
    let formData = new FormData();

    formData.append('file', file);

    var headers = new Headers();
    var csrftoken = getCookie('csrftoken');
    headers.append('X-CSRFToken', csrftoken);
    headers.append('Accept', 'application/json, text/plain, */*');

    fetch('/api/uploader/', {
      method: "POST",
      headers: headers,
      body: formData
    })
        .then((response) => response.json())
        .then((data) => imageInit());
  }


function onDeleteImage(e) {
    var headers = new Headers();
    var csrftoken = getCookie('csrftoken');
    headers.append('X-CSRFToken', csrftoken);
    headers.append('Accept', 'application/json, text/plain, */*');
    headers.append('Content-Type', 'application/x-www-form-urlencoded');
    fetch("/api/uploader/", {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify({
            order: e.getAttribute('data'),
        }),
    })
        .then((response) => response.json())
        .then((data) => imageInit());
}

