function setErrorFor(input, message){
    const formControl = input.parentElement;//.form-group
    const helper = formControl.querySelector('.help-block');

    helper.innerHTML = message;
    helper.style.display="inline";
    formControl.className = "form-group has-error";
}
function setSuccessFor(input){
    const formControl = input.parentElement;//.form-group
    const helper = formControl.querySelector('.help-block');
    helper.style.display="none";
    formControl.className = "form-group success";
}