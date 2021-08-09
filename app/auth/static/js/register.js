const form=document.getElementById('formm');
const email = document.getElementById('email');
const username=document.getElementById('username');
const password=document.getElementById('password');
const password_confirm=document.getElementById('password_confirm');
form.addEventListener('submit',(e)=>{
    e.preventDefault();
    checkInputs();
});

function checkInputs(){
    const emailValue = email.value.trim();
    const usernameValue = username.value.trim();
    const passwordValue = password.value.trim();
    const passwordConfirmValue = password_confirm.value.trim();

    var emailOK=false;
    var usernameOK=false;
    var passwordOK=false;
    var password_confirmOK=false;

    if(emailValue.length<10){
        setErrorFor(email,'邮箱格式不正确');
    }else {
        emailOK=true;
        setSuccessFor(email);
    }

    if(usernameValue==''){
        setErrorFor(username,'用户名不能设置为空');
    }else if(usernameValue.length<2||usernameValue.length>25){
        setErrorFor(username,'用户名在2至25个字符之间');
    }else {
        usernameOK=true;
        setSuccessFor(username);
    }

    if(passwordValue =='' ) {
        setErrorFor(password, '密码不能设置为空');
    }else if(passwordValue.length<8||passwordValue.length>16){
        setErrorFor(password,'密码在8至16个字符之间');
    }else{
        passwordOK=true;
        setSuccessFor(password);
    }

    if(passwordConfirmValue ==''||passwordConfirmValue!==passwordValue){
        setErrorFor(password_confirm,'两次密码输入不一样');
    }else{
        password_confirmOK=true;
        setSuccessFor(password_confirm);
    }

    if(emailOK&&usernameOK&&passwordOK&&password_confirmOK){
        form.submit();
    }
}

