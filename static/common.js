function sign_up() {
    let user_id = $("#input-user_id").val()
    let password = $("#input-password").val()
    let password2 = $("#input-password2").val()
    let nickname = $("#input-nickname").val()
    let cat_name = $("#input-cat_name").val()
    let intro = $("#input-intro").val()
    let file = $('#file')[0].files[0]

    if ($("#help-id").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    if (password == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return;
    } else if (!is_password(password)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
        $("#input-password").focus()
        return
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }
    if (password2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else if (password2 != password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#input-password2").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }

    if (nickname == "") {
        alert("닉네임을 입력해주세요.")
        $("#input-nickname").focus()
        return
    }

    if (cat_name == "") {
        alert("고양이 이름을 입력해주세요.")
        $("#input-cat_name").focus()
        return
    }

    if (file == "") {
        alert("고양이 사진을 업로드해주세요.")
        $("#file").focus()
        return
    }

    let form_data = new FormData()

    form_data.append("file", file)
    form_data.append("user_id", user_id)
    form_data.append("password", password)
    form_data.append("nickname", nickname)
    form_data.append("cat_name", cat_name)
    form_data.append("intro", intro)

    $.ajax({
        type: "POST",
        url: "/sign_up",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/")
        }
    });

}

function update_user() {
    let user_id = $("#hidden-user_id").val()
    let password = $("#input-password").val()
    let password2 = $("#input-password2").val()
    let nickname = $("#input-nickname").val()
    let cat_name = $("#input-cat_name").val()
    let intro = $("#input-intro").val()
    let file = $('#file')[0].files[0]
    let fileName = $('#fileName').val()

    let form_data = new FormData()

    if (password == "" && password2 == ""){
        if(!confirm("비밀번호 변경 없이 회원 정보를 수정하시겠습니까?"))
            return
    } else {
        if (password == "") {
            $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
            $("#input-password").focus()
            return;
        } else if (!is_password(password)) {
            $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
            $("#input-password").focus()
            return
        } else {
            $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
        }
        if (password2 == "") {
            $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
            $("#input-password2").focus()
            return;
        } else if (password2 != password) {
            $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
            $("#input-password2").focus()
            return;
        } else {
            $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
        }

        form_data.append("password", password)
    }

    if (nickname == "") {
        alert("닉네임을 입력해주세요.")
        $("#input-nickname").focus()
        return
    }

    if (cat_name == "") {
        alert("고양이 이름을 입력해주세요.")
        $("#input-cat_name").focus()
        return
    }

    form_data.append("user_id", user_id)
    form_data.append("fileName", fileName)
    form_data.append("file", file)
    form_data.append("nickname", nickname)
    form_data.append("cat_name", cat_name)
    form_data.append("intro", intro)

    $.ajax({
        type: "POST",
        url: "/update_user",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert("회원정보를 수정하였습니다!")
            window.location.replace("/")
        }
    });

}

function default_password(){
    $("#modal-default-pw").addClass("is-active")
}

function default_password_api(){

    user_id = $("#modal-user_id").val()
    cat_name = $("#modal-cat_name").val()

    $.ajax({
        type: "POST",
        url: "/default_password",
        data: {
            user_id: user_id,
            cat_name: cat_name
        },
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });

}

function is_user_id(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function check_dup() {
    let user_id = $("#input-user_id").val()

    if (user_id == "") {
        $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#input-user_id").focus()
        return;
    }
    if (!is_user_id(user_id)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
        $("#input-user_id").focus()
        return;
    }
    $("#help-id").addClass("is-loading")

    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            user_id: user_id
        },
        success: function (response) {

            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-user_id").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-id").removeClass("is-loading")

        }
    });
}

function go_main(){
    window.location.href = '/'
}

function sign_out() {
    $.removeCookie('user_token', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/"
}