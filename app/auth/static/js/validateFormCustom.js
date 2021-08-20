
function setErrorFor(input, message){
    const formControl = input.parentElement;//.form-group
    let helper = formControl.querySelector('.my-tooltip-left');
    const inputSpanElement = formControl.querySelector('span');
    console.log(beforeSpanStyle);
    beforeSpanStyle.background = "#f96d00";
    helper.innerHTML = message;
    helper.style.visibility = 'visible';
    helper.style.display="inline-block";
    // formControl.className = "form-group has-error";
}
function setSuccessFor(input){
    const formControl = input.parentElement;//.form-group
    const helper = formControl.querySelector('.my-tooltip-left');
    const inputSpanElement = formControl.querySelector('span');

    inputSpanElement.style.background = "#1b1b1b";
    helper.style.display='none';
    helper.style.visibility = 'hidden';

    // formControl.className = "form-group success";
}