// Invoke Functions Call on Document Loaded
document.addEventListener("DOMContentLoaded", function () {
  hljs.highlightAll();
});

/*let alertWrapper = document.querySelector(".alert");
 let alertClose = document.querySelector(".alert__close"); */
let alertWrapperList = document.querySelectorAll(".alert");
let alertCloseList = document.querySelectorAll(".alert__close");

/* if (alertWrapper) {
  console.log("Alert Clicked!");
  alertClose.addEventListener("click", () => {
    console.log("Clicked!");
    alertWrapper.style.display = "none";
  });
}
 */

if (alertWrapperList) {
  console.log("Alert Clicked!");

  alertCloseList.forEach((item, index) => {
    item.addEventListener("click", () => {
      console.log("Clicked!");
      alertWrapperList[index].style.display = "none";
      //to delete all alert messages follow the code below.
      //alertWrapperList.forEach((item) => (item.style.display = "none"));
    });
  });
}
