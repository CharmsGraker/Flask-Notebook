const form = document.querySelector("form"),
fileInput = form.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");

//让表单监听fileInput的点击，那么fileInput的点击就带动了form的点击，从而实现一整块都可以点击上传
form.addEventListener("click", ()=>{
    fileInput.click();
});

fileInput.onchange = ({target}) => {
    let file = target.files[0];     // 如果用户多选，那么只选择第一个
    document.cookie = "filesize="+file.size;
    document.request
    if(file) {
        let fileName = file.name;
        //名字太长很不美观
        if(fileName.length >= 12){
            let splitName = fileName.split('.');
            fileName = splitName[0].substring(0, 12) + "... .";
        }
        uploadFile(fileName);
    }
}


function uploadFile(name) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST","upload_image");
    xhr.upload.addEventListener("progress", ({loaded, total}) =>{
        let fileLoaded = Math.floor((loaded / total) * 100);
        let fileTotal = Math.floor(total / 1000); // 得到KB单位的大小
        console.log(fileLoaded, fileTotal);
        let fileSize;
        //换算单位
        (fileSize < 1024) ? fileSize = fileSize + "KB" : fileSize = (loaded / (1024 * 1024)).toFixed(2) + "MB";

        let progressHTML = '<li class="row"> \
                           <i class="fa fa-file-alt"></i> \
                            <div class="content"> \
                                <div class="details"> \
                                    <span class="name">'+ name +'·Uploading</span> \
                                   <span class="percent">'+ fileLoaded + '</span> \
                                </div> \
                               <div class="progress-bar"> \
                                    <div class="progress"  style="width: '+ fileLoaded +'%"></div> \
                                </div> \
                            </div> \
                       </li>';

        progressArea.innerHTML = progressHTML;
        if(loaded == total) {
            progressArea.innerHTML = "";
             let uploadedHTML = '<li class="row">\n' +
            '                 <div class="content">\n' +
            '                     <i class="fa fa-file-alt"></i>\n' +
            '                     <div class="details">\n' +
            '                         <span class="name">' + name + '·上传完成</span>\n' +
            '                         <span class="size">' +fileSize + '</span>\n' +
            '                     </div>\n' +
            '                 </div>\n' +
            '                 <i class="fa fa-check"></i>\n' +
            '             </li>';
             //这里是插入，选择afterbegin方式
            uploadedArea.insertAdjacentHTML("afterbegin",uploadedHTML);
        }

    });
    let formData = new FormData(form);
    xhr.send(formData);

}
