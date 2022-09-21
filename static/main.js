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
});