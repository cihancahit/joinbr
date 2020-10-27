$(function () {
    var dropZoneId = "drop-zone";
    var buttonId = "clickHere";
    var mouseOverClass = "mouse-over";

    var dropZone = $("#" + dropZoneId);
    var ooleft = dropZone.offset().left;
    var ooright = dropZone.outerWidth() + ooleft;
    var ootop = dropZone.offset().top;
    var oobottom = dropZone.outerHeight() + ootop;
    var inputFile = dropZone.find("input");
    document.getElementById(dropZoneId).addEventListener("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.addClass(mouseOverClass);
        var x = e.pageX;
        var y = e.pageY;

        if (!(x < ooleft || x > ooright || y < ootop || y > oobottom)) {
            inputFile.offset({
                top: y - 15,
                left: x - 100
            });
        } else {
            inputFile.offset({
                top: -400,
                left: -400
            });
        }

    }, true);

    if (buttonId != "") {
        var clickZone = $("#" + buttonId);

        var oleft = clickZone.offset().left;
        var oright = clickZone.outerWidth() + oleft;
        var otop = clickZone.offset().top;
        var obottom = clickZone.outerHeight() + otop;

        $("#" + buttonId).mousemove(function (e) {
            var x = e.pageX;
            var y = e.pageY;
            if (!(x < oleft || x > oright || y < otop || y > obottom)) {
                inputFile.offset({
                    top: y - 15,
                    left: x - 160
                });
            } else {
                inputFile.offset({
                    top: -400,
                    left: -400
                });
            }
        });
    }

    document.getElementById(dropZoneId).addEventListener("drop", function (e) {
        $("#" + dropZoneId).removeClass(mouseOverClass);
    }, true);

    inputFile.on('change', function (e) {
        $('#filename').html("");
        var fileNum = this.files.length,
            initial = 0,
            counter = 0;
        for (initial; initial < fileNum; initial++) {
            counter = counter + 1;
            $('#filename').append('<span class="fa-stack fa-lg"><i class="fa fa-file fa-stack-1x "></i><strong class="fa-stack-1x" style="color:#FFF; font-size:12px; margin-top:2px;">'+ counter + '</strong></span> ' + this.files[initial].name + '<br>');
        }
    });
	
});


//event cover photo pen icon click

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#ep-ce-cover-image').attr('src', e.target.result);
            $('#ep-ce-cover-image').hide();
            $('#ep-ce-cover-image').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#ep-ce-cover-image-inp").change(function() {
    readURL(this);
});


//event cover photo pen icon click

function readURLProfileImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#ep-profile-image').attr('src', e.target.result);
            $('#ep-profile-image').hide();
            $('#ep-profile-image').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#ep-edit-profile-pic").change(function() {
    readURLProfileImage(this);
});