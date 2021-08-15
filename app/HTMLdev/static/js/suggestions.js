const searchWrapper = document.querySelector(".search-input");
const InputBox = document.querySelector("input");
const suggBox = document.querySelector(".autocom-box");


$(document).ready(function(){
  $("#input_box").on("input", function (e){
      text_in_livebox = $("#input_box").val();
      if (text_in_livebox) {
          $.ajax({
              method: "POST",
              url: "livesearch",
              data: {text: text_in_livebox},
              success: function (res) {
                  //res 是数组
                  var data = "<ul>";
                  $.each(res, function (index, value) {
                      data += "<li>" +"<span id='content'>"+ value.title + "</span>" +
                          "<span id='create_time'>"+ value.create_time +"</span>"
                          + "</li>";
                  });
                  data += "</ul>";

                  $("#datalist").html(data);
                  searchWrapper.classList.add(("active"));

                  //注意是All
                  let allList = suggBox.querySelectorAll("li");
                  for (let i = 0; i < allList.length; ++i) {
                      //添加点击属性
                      //第二个是函数名
                      allList[i].setAttribute("onclick", "select(this)");
                  }
              }
          })
      }else {
          //用户未输入，不展示候选框
            searchWrapper.classList.remove(("active"));
      }
  });

});
//添加active响应，当输入框激活时，启用候选框可见

function select(element) {
    let selectUserData = element.querySelector("#content").textContent;
    // console.log(selectUserData);
    InputBox.value = selectUserData;//填充到输入框里
}


