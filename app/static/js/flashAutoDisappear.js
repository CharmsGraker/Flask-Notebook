function addListen(){
    $('.alert').removeClass('hide');

    $('.alert').addClass('show');
    $('.alert').addClass('showAlert');

    setTimeout(function(){
        // 添加一定时间后自动消失
        $('.alert').addClass('hide');
        $('.alert').removeClass('show');

    },3000);
        $('.alert').addClass('hide');
        $('.alert').removeClass('show');
}
