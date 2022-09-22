/*
const thisIsButton = document.getElementsByClassName('comment_btn')[0];
//버튼요소 변수 할당

thisIsButton.addEventListener('click', function () {
    const commentEl = document.getElementsByClassName('input_comment')[0].value;

    let createComment = document.createElement("div");

    createComment.innerHTML = `<strong>username:</strong> ${commentEl}`;

    createComment.className = 'savedComment';

    let commentInsert = document.querySelector('.comments-box');
    commentInsert.appendChild(createComment);

    var input_clear = document.getElementById('clear');
    input_clear.value = null;
});*/

const toTopEl = document.querySelector('#to-top');
toTopEl.addEventListener('click', function () {
 gsap.to(window, .7, {
  scrollTo: 0
 })
});

window.addEventListener('scroll', _.throttle(function () {
  console.log(window.scrollY);
  if (window.scrollY > 50) {
    // 맨위로 올라가기 버튼보이기!
    gsap.to(toTopEl, .2, {
      x: 0
    });
  } else {
    // 맨위로 올라가기 버튼 숨기기!
    gsap.to(toTopEl, .2, {
      x: 100
    });
  }
}, 300));