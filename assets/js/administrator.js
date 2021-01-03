
// open or close sidebar
function open_sidebar() {
    document.getElementById("mainsidebar").style.marginRight = "17%";
    document.getElementById("mySidebar").style.width = "17%";
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("openNav").style.display = 'none';
}
function close_sidebar() {
    document.getElementById("mainsidebar").style.marginRight = "0%";
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("openNav").style.display = "inline-block";
}

// administrator
$(function(){
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $(window).resize(function(e) {
    if($(window).width()<=768){
        $("#wrapper").removeClass("toggled");
    }else{
        $("#wrapper").addClass("toggled");
    }
    });
});

// close Alert Massage
setTimeout(function () {
    $('.removeAlertMsg').slideUp()
}, 5000);
