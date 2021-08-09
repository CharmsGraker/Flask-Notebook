const form=document.getElementById('form');
const username=document.getElementById('username');
const password=document.getElementById('password');
form.addEventListener('submit',(e)=>{
    e.preventDefault();
    checkInputs();
});
function checkInputs(){
    const usernameValue=username.value.trim();
    const passwordValue=password.value.trim();
    var usernameValid=false;
    var passwordValid=false;
    if(usernameValue.length<2||usernameValue.length>25){
        setErrorFor(username,'请输入有效的用户名');
    }else{
        usernameValid = true;
        setSuccessFor(username);
    }
    if(passwordValue.length<8||passwordValue.length>16){
        setErrorFor(password, '请输入有效的密码');
    }else{
        passwordValid = true;
        setSuccessFor(password);
    }
    if(usernameValid && passwordValid){
        form.submit();
    }
}
