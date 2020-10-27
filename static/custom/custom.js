function validForm(e) {
    var t, n, a = !0;
    for (t = document.getElementsByClassName("step")[e].getElementsByTagName("input"), n = 0; n < t.length; n++) "" == t[n].value && (t[n].className += " invalid", a = !1);
    return a
}

$(window).on("load", function () {
    $(".loader").fadeOut(), $("#preloader").delay(350).fadeOut("slow")
}), $(document).ready(function () {
    $(".your-class").slick({
        slidesToShow: 3,
        dots: !0,
        slidesToScroll: 1,
        autoplay: !0,
        prevArrow: $(".prev-arrow"),
        nextArrow: $(".next-arrow")
    })
}), $(document).ready(function () {
    $("#slider").slick({
        slidesToScroll: 1,
        autoplay: !0,
        arrows: !0,
        prevArrow: $(".prev-arrow"),
        nextArrow: $(".next-arrow")
    })
}), $(document).ready(function () {
    $(".cat-slider").slick({
        slidesToShow: 5,
        slidesToScroll: 2,
        autoplay: !0,
        centerMode: !0,
        responsive: [{breakpoint: 1024, settings: {slidesToShow: 3, slidesToScroll: 3, infinite: !0}}, {
            breakpoint: 600,
            settings: {slidesToShow: 2, slidesToScroll: 2}
        }, {breakpoint: 480, settings: {slidesToShow: 1, slidesToScroll: 1}}]
    })
}), $(document).ready(function () {
    $(".top-org-slider").slick({
        slidesToShow: 5,
        slidesToScroll: 2,
        autoplay: !0,
        centerMode: !0,
        responsive: [{breakpoint: 1024, settings: {slidesToShow: 3, slidesToScroll: 3}}, {
            breakpoint: 600,
            settings: {slidesToShow: 2, slidesToScroll: 2}
        }, {breakpoint: 480, settings: {slidesToShow: 1, slidesToScroll: 1}}]
    })
}), $(function () {
    $("#login-form-link").click(function (e) {
        $("#login-form").delay(100).fadeIn(100), $("#register-form").fadeOut(100), $("#register-form-link").removeClass("active"), $(this).addClass("active"), e.preventDefault()
    }), $("#register-form-link").click(function (e) {
        $("#register-form").delay(100).fadeIn(100), $("#login-form").fadeOut(100), $("#login-form-link").removeClass("active"), $(this).addClass("active"), e.preventDefault()
    })
});
const steps = $(".event-form").children().css({class: "row"});
var current_step;

function search() {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    });
    var t = document.getElementById("se_event_name").value, n = document.getElementById("se_event_loc").value,
        a = document.getElementById("se_event_date").value;
    $.ajax({
        url: "/events/searchevent/",
        data: {event_name: t, event_loc: n, event_date: a},
        dataType: "json",
        type: "POST",
        success: function (e) {
            for (var n in e = JSON.parse(e), console.log(e), event_html = "", e) {
                const o = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                t = e[n].fields.name, event_id = e[n].pk, event_info = e[n].fields.info;
                var a = new Date(e[n].fields.start_event_dt);
                event_category = e[n].fields.category, event_img = e[n].fields.event_img, event_html = event_html + '<div class="col-md-4 col-sm-12 mt-5 event-card filter ' + event_category + '">    <div class="card mx-sm-1 shadow">       <a href="">          <img class="card-img-top event-card-img" src="/media/' + event_img + '" alt="Card image cap">     </a>    <div class="card-body" style="position: relative">       <div class="shadow text-white  event-date text-center font-weight-bold"><span class="sp-month">' + o[a.getMonth()] + '</span><span class="sp-dt">' + a.getDate() + "-" + a.getFullYear() + '</span></div>    <h5 class="card-title text-center pt-3">' + t + '</h5>   <p class="card-text text-center">' + event_info + '</p>  <div class="card-event-icons d-flex flex-grow-1 justify-content-end">     <span style="color: #0097fe;" class="fa fa-share-alt" aria-hidden="true"></span>    <span style="color: #e85858;" class="fa fa-heart" aria-hidden="true"></span> </div></div><div class="card shadow text-white buy-ticket text-uppercase px-4"\n                                 onclick="location.href=\'/events/' + event_slug + "';\"><p>See More</p>\n                            </div></div></div>"
            }
            document.getElementById("event-container").innerHTML = event_html
        }
    })
}

function create_post() {
    console.log("create post is working!");
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    });
    var t = $("#id_event_img").prop("files")[0], n = new FormData;
    n.append("name", $("#name").val()), n.append("category", $("#category").val()), n.append("organizer", $("#organizer").val()), n.append("speaker", $("#speaker").val()), n.append("start_dt", $("#start_dt").val()), n.append("end_dt", $("#end_dt").val()), n.append("lang", $("#lang").val()), n.append("ticket_type", $("#option:checked").val()), n.append("price", $("#price").val()), n.append("quantity", $("#quantity").val()), n.append("location", $("#location").val()), n.append("description", $("#description").val()), n.append("file", t), $.ajax({
        url: "/events/postevent/",
        type: "POST",
        dataType: "json",
        processData: !1,
        data: n,
        contentType: !1,
        success: function (e) {
            $("#quantity").val(""), console.log(e), console.log("success")
        },
        error: function (e, t, n) {
            $("#results").html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + t + " <a href='#' class='close'>&times;</a></div>"), console.log(e.status + ": " + e.responseText)
        }
    })
}

$(document).on("change", "input:text", function () {
    $(this).removeClass("invalid")
}), $(".next-btn").on("click", e => {
    const t = parseInt($(e.target).attr("data-step"));
    next_step = t + 1, validForm(t - 1) && ($(".green-line").removeClass("green-line-1"), $(".green-line").removeClass("green-line-2"), $(".green-line").removeClass("green-line-3"), $(".green-line").addClass("green-line-" + next_step.toString()), t === steps.length - 3 ? ($(".next-btn").hide(), $(".create-btn").addClass("d-flex"), $(".step").removeClass("active-step"), $(`.step-${t + 1}`).addClass("active-step")) : ($(".step").removeClass("active-step"), $(`.step-${current_step = t + 1}`).addClass("active-step")))
}), $(".create-btn").on("click", e => {
    const t = parseInt($(e.target).attr("data-step"));
    validForm(1) && (next_step = t + 1, $(".green-line").removeClass("green-line-1"), $(".green-line").removeClass("green-line-2"), $(".green-line").removeClass("green-line-3"), $(".green-line").addClass("green-line-3"), $(".next-btn").hide(), $(".create-btn").hide(), $(".create-btn").removeClass("d-flex"), $(".step-2").removeClass("active-step"), $(".step-3").addClass("active-step"), create_post())
}), $(".previous-btn").on("click", e => {
    const t = $(".event-form").children().css({class: "row"}), n = parseInt($(".active-step").attr("data-step"));
    console.log(n), n === t.length ? (console.log(n + " last"), $(".next-btn").show(), $(".create-btn").addClass("d-none"), $(".create-btn").removeClass("d-flex"), $(".step").removeClass("active-step"), $(`.step-${n - 1}`).addClass("active-step")) : 1 === n ? $("#ce-modal").modal("hide") : 3 === n ? ($(".next-btn").hide(), $(".create-btn").addClass("d-flex"), $(".create-btn").removeClass("d-none"), $(".step").removeClass("active-step"), $(`.step-${n - 1}`).addClass("active-step")) : ($(".step").removeClass("active-step"), $(`.step-${n - 1}`).addClass("active-step"), $(".next-btn").show(), $(".create-btn").hide(), $(".create-btn").addClass("d-none"), $(".create-btn").removeClass("d-flex"))
}), $("#ce-modal").on("hidden.bs.modal", function () {
    if (3 === parseInt($(".active-step").attr("data-step"))) {
        $(this).find("input,textarea,select").val("").end().find("input[type=checkbox], input[type=radio]").prop("checked", "").end(), document.querySelector(".file-info").innerHTML = "", $(".fee-btn").removeClass("active"), $(".green-line").removeClass("green-line-1"), $(".green-line").removeClass("green-line-2"), $(".green-line").removeClass("green-line-3"), $(".step").removeClass("active-step"), $(".step-1").addClass("active-step")
    }
}), $(document).ready(function () {
    function e() {
        console.log("1");
        var e = document.getElementById("id_donation_price").value;
        console.log(e);
        var t = document.getElementById("id_quantiy").value;
        console.log(t), document.getElementById("total").innerHTML = e * t
    }

    var t = document.getElementById("id_donation_price"), n = document.getElementById("id_quantiy");
    t && t.addEventListener("change", e), n && n.addEventListener("change", e)
}), $(document).ready(function () {
    $(".event-container").slick({
        slidesToShow: 3,
        dots: !0,
        slidesToScroll: 1,
        autoplay: !0,
        prevArrow: $(".prev-arrow"),
        nextArrow: $(".next-arrow")
    })
}), $(document).ready(function () {
    $("#slider").not(".slick-initialized").slick({
        slidesToScroll: 1,
        autoplay: !1,
        arrows: !0,
        prevArrow: $(".prev-arrow"),
        nextArrow: $(".next-arrow")
    })
});
const uploadButton = document.querySelector(".browse-btn"), fileInfo = document.querySelector(".file-info"),
    realInput = document.getElementById("id_event_img");
$(".browse-btn").click(function () {
    realInput.click()
}), realInput.addEventListener("change", () => {
    const e = realInput.value.split(/\\|\//).pop(), t = e.length > 20 ? e.substr(e.length - 20) : e;
    fileInfo.innerHTML = t
});
const enableCity = () => {
    console.log("enablecity started");
    const e = document.getElementById("country").value;
    console.log("country->" + e), "" === e ? (console.log("country is empty"), document.getElementById("city").value = "", document.getElementById("city").disabled = !0) : (console.log("country is not empty"), document.getElementById("city").value = "", document.getElementById("city").disabled = !1)
};
var inp_country = document.getElementById("country"), inp_city = document.getElementById("city");


// Search based URL

function CompanyOnSubmitForm() {

   var location = document.getElementById("location").value;
   var market = document.getElementById("market").value;

   location = location.split(' ').join('-');
   market = market.split(' ').join('-');

   if (market == "Industry") {
       market = ''
   }

   if (market !== '' && location == '') {
       document.companysearch.action = "/companies/market/" + market
   }
   else if (location !== '' && market == '') {
       document.companysearch.action = "/companies/location/" + location
   }
   else if (location !== '' && market !== '') {
       document.companysearch.action = "/companies/" + market + "/" + location
   }
   else {
        document.companysearch.action = "/companies/search"
    }
}

function ExpertOnSubmitForm() {
    var e = document.getElementById("country").value, t = document.getElementById("city").value,
        n = document.getElementById("skills").value, a = document.getElementById("language").value;
    document.getElementById("location").value;
    return e = e.split(" ").join("-"), t = t.split(" ").join("-"), n = n.split(" ").join("-"), a = a.split(" ").join("-"), "" == t && "" !== e && "" == n && "" == a ? document.myform2.action = "/experts/country/" + e : "" !== a && "" !== n && "" !== t && "" !== e ? document.myform2.action = "/experts/" + n + "/" + a + "/" + e + "/" + t : "" !== t && "" !== e && "" == n && "" == a ? document.myform2.action = "/experts/country/" + e + "/" + t : "" == t && "" !== e && "" !== n && "" !== a ? document.myform2.action = "/experts/" + n + "/language/" + a + "/" + e : "" == t && "" !== e && "" !== n && "" == a ? document.myform2.action = "/experts/skills/" + n + "/" + e : "" == t && "" !== e && "" == n && "" !== a ? document.myform2.action = "/experts/language/" + a + "/" + e : "" == t && "" == e && "" !== n && "" !== a ? document.myform2.action = "/experts/" + n + "/" + a : "" == t && "" == e && "" !== n && "" == a ? document.myform2.action = "/experts/" + n : "" == t && "" == e && "" == n && "" !== a ? document.myform2.action = "/experts/language/" + a : "" !== t && "" !== e ? "" == n && "" !== a ? document.myform2.action = "/experts/language/" + a + "/" + e + "/" + t : "" !== n && "" == a && (document.myform2.action = "/experts/" + n + "/" + e + "/" + t) : document.myform2.action = "/experts/search", !0
}

function EventOnSubmitForm() {
    var e = document.getElementById("country").value;
    if (document.getElementById("city")) var t = document.getElementById("city").value; else t = "";
    var n = document.getElementById("event_category"), a = n.options[n.selectedIndex].value,
        o = document.getElementById("date").value;
    return "Industry" == a && (a = ""), e = e.split(" ").join("-"), t = t.split(" ").join("-"), a = a.split(" ").join("-"), o = o.split(" ").join("-"), "" == t && "" !== e && "" == a && "" == o ? document.event_search.action = "/events/country/" + e : "" !== o && "" !== a && "" !== t && "" !== e ? document.event_search.action = "/events/" + a + "/" + o + "/" + e + "/" + t : "" !== t && "" !== e && "" == a && "" == o ? document.event_search.action = "/events/country/" + e + "/" + t : "" == t && "" !== e && "" !== a && "" !== o ? document.event_search.action = "/events/" + a + "/date/" + o + "/" + e : "" == t && "" !== e && "" !== a && "" == o ? document.event_search.action = "/events/category/" + a + "/" + e : "" == t && "" !== e && "" == a && "" !== o ? document.event_search.action = "/events/date/" + o + "/" + e : "" == t && "" == e && "" !== a && "" !== o ? document.event_search.action = "/events/" + a + "/" + o : "" == t && "" == e && "" !== a && "" == o ? document.event_search.action = "/events/search/" + a : "" == t && "" == e && "" == a && "" !== o ? document.event_search.action = "/events/date/" + o : "" !== t && "" !== e ? "" == a && "" !== o ? document.event_search.action = "/events/date/" + o + "/" + e + "/" + t : "" !== a && "" == o && (document.event_search.action = "/events/" + a + "/" + e + "/" + t) : document.event_search.action = "/events/search", !0
}

inp_country && inp_city && ("" === inp_country.value && (inp_city.disabled = !0), inp_country.addEventListener("keydown", enableCity), inp_country.addEventListener("onfocusout", enableCity)), $(document).ready(function () {
    if ($(window).width() > 992) {
        var e = $("#mainNav").height();
        $(window).on("scroll", {previousTop: 0}, function () {
            var t = $(window).scrollTop();
            t < this.previousTop ? t > 0 && $("#mainNav").hasClass("is-fixed") ? $("#mainNav").addClass("is-visible") : $("#mainNav").removeClass("is-visible is-fixed") : t > this.previousTop && t > 640 && ($("#mainNav").removeClass("is-visible"), t > e && !$("#mainNav").hasClass("is-fixed") && $("#mainNav").addClass("is-fixed")), this.previousTop = t
        })
    }
}), $("[data-toggle=popover]").popover();
const aeuploadButton = document.querySelector(".ae-profile-pic-btn"),
    aefileInfo = document.querySelector(".ae-file-info"), aerealInput = document.getElementById("ae-profile-pic");
$(aeuploadButton).click(function (e) {
    e.preventDefault()
}), $(aeuploadButton).click(function () {
    aerealInput.click()
}), aerealInput && aerealInput.addEventListener("change", () => {
    const e = aerealInput.value.split(/\\|\//).pop(), t = e.length > 20 ? e.substr(e.length - 20) : e;
    aefileInfo.innerHTML = t
});
const acuploadButton = document.querySelector(".ac-logo-btn"), acfileInfo = document.querySelector(".ac-file-info"),
    acrealInput = document.getElementById("ac-logo");
$(acuploadButton).click(function (e) {
    e.preventDefault()
}), $(acuploadButton).click(function () {
    acrealInput.click()
}), acrealInput && acrealInput.addEventListener("change", () => {
    const e = acrealInput.value.split(/\\|\//).pop(), t = e.length > 20 ? e.substr(e.length - 20) : e;
    acfileInfo.innerHTML = t
});
var shareBtn = document.querySelector(".share-button");
shareBtn && shareBtn.addEventListener("click", function (e) {
    var t = document.createElement("input");
    t.setAttribute("type", "hidden"), text = window.location.href, document.body.appendChild(t), t.value = text, t.select(), document.execCommand("copy"), e.preventDefault
}), $(document).ready(function () {
    function e() {
        var e = document.getElementById("id_donation_price").innerHTML, t = document.getElementById("id_quantiy").value,
            n = document.getElementById("total"), a = document.getElementById("total1");
        n.innerHTML = e * t + "$", a.innerHTML = "Total Prices: " + e * t + "$"
    }

    var t = document.getElementById("id_donation_price"), n = document.getElementById("id_quantiy");
    t && t.addEventListener("change", e), n && n.addEventListener("change", e)
}), $("#btnaddexpert").click(function () {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    });
    var t = $("#ae-profile-pic").prop("files")[0], n = new FormData;
    n.append("name", $("#ae-name").val()), n.append("btitle", $("#ae-btitle").val()), n.append("website", $("#ae-website").val()), n.append("facebook", $("#ae-facebook").val()), n.append("linkedin", $("#ae-linkedin").val()), n.append("twitter", $("#ae-twitter").val()), n.append("company", $("#ae-company").val()), n.append("country", $("#ae-country").val()), n.append("city", $("#ae-city").val()), n.append("industry", $("#ae-industry").val()), n.append("contact", $("#ae-contact").val()), n.append("age", $("#ae-age").val()), n.append("bio", $("#ae-bio").val()), n.append("expertise", $("#ae-expertise").val()), n.append("file", t), $.ajax({
        url: "/experts/add_expert/",
        type: "POST",
        dataType: "json",
        processData: !1,
        data: n,
        contentType: !1,
        success: function (e) {
            new Noty({
                type: "success",
                layout: "center",
                text: "Expert Added Successfully",
                closeWith: ["click", "button"],
                animation: {open: "animated fadeInDown", close: "animated fadeOutUp"}
            }).show()
        },
        error: function (e, t, n) {
            new Noty({
                type: "error",
                layout: "center",
                text: "Oops! We have encountered an error: " + n,
                closeWith: ["click", "button"],
                animation: {open: "animated fadeInDown", close: "animated fadeOutUp"}
            }).show()
        }
    })
}), $(document).ready(function () {
    $("#company_name").autocomplete({
        source: "/companies/ac/search/c/name",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    }), $("#skills").autocomplete({
        source: "/experts/ac/search/e/skills",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    }), $("#language").autocomplete({
        source: "/experts/ac/search/e/lang",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    }), $("#market").autocomplete({
        source: "/companies/ac/search/c/market",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    }), $("#country").autocomplete({
        source: "/companies/ac/search/c/country",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    }), $("#city").autocomplete({
        source: function (e, t) {
            $.getJSON("/companies/ac/search/c/city", {country: $("#country").val(), city: $("#city").val()}, t)
        }, minLength: 2, messages: {
            noResults: "", results: function () {
            }
        }, select: function (e, t) {
        }
    })
}), $(document).ready(function () {
    $("#expert_name").autocomplete({
        source: "/experts/ac/search/e/name",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    })
}), $(document).ready(function () {
    $("#industry").autocomplete({
        source: "/experts/ac/search/e/industry",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    })
}), $(document).ready(function () {
    $("#company").autocomplete({
        source: "/experts/ac/search/e/company",
        minLength: 2,
        messages: {
            noResults: "", results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $(".ui-autocomplete").css("z-index", 99)
            }, 0)
        }
    })
});
var myDataService = {
    rate: function (e) {
        return {
            then: function (e) {
                setTimeout(function () {
                    e(5 * Math.random())
                }, 1e3)
            }
        }
    }
};
if ($("#event_filter_date").change(function () {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    }), $.ajax({
        url: "/events/filtereventd/",
        data: {event_date: this.value},
        dataType: "json",
        type: "POST",
        success: function (e) {
            for (var t in e = JSON.parse(e), console.log(e), event_html = "", e) {
                const a = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                event_name = e[t].fields.name, event_slug = e[t].fields.slug, event_id = e[t].pk, event_info = e[t].fields.info;
                var n = new Date(e[t].fields.start_event_dt);
                event_category = e[t].fields.category, event_img = e[t].fields.event_img, event_html = event_html + '<div class="col-md-4 col-lg-3 col-sm-6 mt-5 event-card filter d-flex align-items-stretch ' + event_category + '">    <div class="card mx-sm-1 shadow" style="width: 100%;">       <a href="/events/' + event_slug + '">          <img class="card-img-top event-card-img" src="/media/' + event_img + '" alt="Card image cap"><div class="overlay">            </div>     </a>    <div class="card-body" style="position: relative">       <div class="shadow text-white  event-date text-center font-weight-bold"><span class="sp-month">' + a[n.getMonth()] + '</span><span class="sp-dt">' + n.getDate() + "-" + n.getFullYear() + '</span></div>    <h5 class="card-title text-center pt-3" data-toggle="tooltip" data-placement="top" title="' + event_name + '">' + event_name + '</h5>  <div class="card-event-icons d-flex flex-grow-1 justify-content-between">     <span style="color: #0097fe;" class="fa fa-share-alt" aria-hidden="true"></span>    <span style="color: #e85858;" class="fa fa-heart" aria-hidden="true"></span> </div></div><div class="card shadow text-white buy-ticket text-uppercase px-4"\n                                 onclick="location.href=\'/events/' + event_slug + "';\"><p>See More</p>\n                            </div></div></div>"
            }
            document.getElementById("event-container").innerHTML = event_html
        }
    })
}), $("#event_filter_cat").change(function () {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    }), $.ajax({
        url: "/events/filtereventc/",
        data: {event_cat: this.value},
        dataType: "json",
        type: "POST",
        success: function (e) {
            for (var t in e = JSON.parse(e), console.log(e), event_html = "", e) {
                const a = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                event_name = e[t].fields.name, event_slug = e[t].fields.slug, event_id = e[t].pk, event_info = e[t].fields.info;
                var n = new Date(e[t].fields.start_event_dt);
                event_category = e[t].fields.category, event_img = e[t].fields.event_img, event_html = event_html + '<div class="col-md-4 col-lg-3 col-sm-6 mt-5 event-card filter d-flex align-items-stretch ' + event_category + '">    <div class="card mx-sm-1 shadow" style="width: 100%;">       <a href="/events/' + event_slug + '">          <img class="card-img-top event-card-img" src="/media/' + event_img + '" alt="Card image cap"><div class="overlay">            </div>     </a>    <div class="card-body" style="position: relative">       <div class="shadow text-white  event-date text-center font-weight-bold"><span class="sp-month">' + a[n.getMonth()] + '</span><span class="sp-dt">' + n.getDate() + "-" + n.getFullYear() + '</span></div>    <h5 class="card-title text-center pt-3" data-toggle="tooltip" data-placement="top" title="' + event_name + '">' + event_name + '</h5>  <div class="card-event-icons d-flex flex-grow-1 justify-content-between">     <span style="color: #0097fe;" class="fa fa-share-alt" aria-hidden="true"></span>    <span style="color: #e85858;" class="fa fa-heart" aria-hidden="true"></span> </div></div><div class="card shadow text-white buy-ticket text-uppercase px-4"\n                                 onclick="location.href=\'/events/' + event_slug + "';\"><p>See More</p>\n                            </div></div></div>"
            }
            document.getElementById("event-container").innerHTML = event_html
        }
    })
}), $("#event_filter_price").change(function () {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    }), $.ajax({
        url: "/events/filtereventp/",
        data: {event_price: this.value},
        dataType: "json",
        type: "POST",
        success: function (e) {
            for (var t in e = JSON.parse(e), console.log(e), event_html = "", e) {
                const a = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                event_name = e[t].fields.name, event_slug = e[t].fields.slug, event_id = e[t].pk, event_info = e[t].fields.info;
                var n = new Date(e[t].fields.start_event_dt);
                event_category = e[t].fields.category, event_img = e[t].fields.event_img, event_html = event_html + '<div class="col-md-4 col-lg-3 col-sm-6 mt-5 event-card filter d-flex align-items-stretch ' + event_category + '">    <div class="card mx-sm-1 shadow" style="width: 100%;">       <a href="/events/' + event_slug + '">          <img class="card-img-top event-card-img" src="/media/' + event_img + '" alt="Card image cap"><div class="overlay">            </div>     </a>    <div class="card-body" style="position: relative">       <div class="shadow text-white  event-date text-center font-weight-bold"><span class="sp-month">' + a[n.getMonth()] + '</span><span class="sp-dt">' + n.getDate() + "-" + n.getFullYear() + '</span></div>    <h5 class="card-title text-center pt-3" data-toggle="tooltip" data-placement="top" title="' + event_name + '">' + event_name + '</h5>  <div class="card-event-icons d-flex flex-grow-1 justify-content-between">     <span style="color: #0097fe;" class="fa fa-share-alt" aria-hidden="true"></span>    <span style="color: #e85858;" class="fa fa-heart" aria-hidden="true"></span> </div></div><div class="card shadow text-white buy-ticket text-uppercase px-4"\n                                 onclick="location.href=\'/events/' + event_slug + "';\"><p>See More</p>\n                            </div></div></div>"
            }
            document.getElementById("event-container").innerHTML = event_html
        }
    })
}), document.getElementById("pnAdvancerLeft")) {
    var SETTINGS = {navBarTravelling: !1, navBarTravelDirection: "", navBarTravelDistance: 150},
        colours = {0: "#09c75b"};
    document.documentElement.classList.remove("no-js"), document.documentElement.classList.add("js");
    var pnAdvancerLeft = document.getElementById("pnAdvancerLeft"),
        pnAdvancerRight = document.getElementById("pnAdvancerRight"),
        pnIndicator = document.getElementById("pnIndicator"), pnProductNav = document.getElementById("pnProductNav"),
        pnProductNavContents = document.getElementById("pnProductNavContents");
    pnProductNav.setAttribute("data-overflowing", determineOverflow(pnProductNavContents, pnProductNav)), moveIndicator(pnProductNav.querySelector('[aria-selected="true"]'), colours[0]);
    var last_known_scroll_position = 0, ticking = !1;

    function doSomething(e) {
        pnProductNav.setAttribute("data-overflowing", determineOverflow(pnProductNavContents, pnProductNav))
    }

    function moveIndicator(e, t) {
        var n = e.getBoundingClientRect(), a = pnProductNavContents.getBoundingClientRect().left, o = n.left - a,
            s = pnProductNavContents.scrollLeft;
        pnIndicator.style.transform = "translateX(" + (o + s) + "px) scaleX(" + .01 * n.width + ")", t && (pnIndicator.style.backgroundColor = t)
    }

    function determineOverflow(e, t) {
        var n = t.getBoundingClientRect(), a = Math.floor(n.right), o = Math.floor(n.left),
            s = e.getBoundingClientRect(), r = Math.floor(s.right), i = Math.floor(s.left);
        return o > i && a < r ? "both" : i < o ? "left" : r > a ? "right" : "none"
    }

    pnProductNav.addEventListener("scroll", function () {
        last_known_scroll_position = window.scrollY, ticking || window.requestAnimationFrame(function () {
            doSomething(last_known_scroll_position), ticking = !1
        }), ticking = !0
    }), pnAdvancerLeft.addEventListener("click", function () {
        if (!0 !== SETTINGS.navBarTravelling) {
            if ("left" === determineOverflow(pnProductNavContents, pnProductNav) || "both" === determineOverflow(pnProductNavContents, pnProductNav)) {
                var e = pnProductNav.scrollLeft;
                e < 2 * SETTINGS.navBarTravelDistance ? pnProductNavContents.style.transform = "translateX(" + e + "px)" : pnProductNavContents.style.transform = "translateX(" + SETTINGS.navBarTravelDistance + "px)", pnProductNavContents.classList.remove("pn-ProductNav_Contents-no-transition"), SETTINGS.navBarTravelDirection = "left", SETTINGS.navBarTravelling = !0
            }
            pnProductNav.setAttribute("data-overflowing", determineOverflow(pnProductNavContents, pnProductNav))
        }
    }), pnAdvancerRight.addEventListener("click", function () {
        if (!0 !== SETTINGS.navBarTravelling) {
            if ("right" === determineOverflow(pnProductNavContents, pnProductNav) || "both" === determineOverflow(pnProductNavContents, pnProductNav)) {
                var e = pnProductNavContents.getBoundingClientRect().right,
                    t = pnProductNav.getBoundingClientRect().right, n = Math.floor(e - t);
                n < 2 * SETTINGS.navBarTravelDistance ? pnProductNavContents.style.transform = "translateX(-" + n + "px)" : pnProductNavContents.style.transform = "translateX(-" + SETTINGS.navBarTravelDistance + "px)", pnProductNavContents.classList.remove("pn-ProductNav_Contents-no-transition"), SETTINGS.navBarTravelDirection = "right", SETTINGS.navBarTravelling = !0
            }
            pnProductNav.setAttribute("data-overflowing", determineOverflow(pnProductNavContents, pnProductNav))
        }
    }), pnProductNavContents.addEventListener("transitionend", function () {
        var e = window.getComputedStyle(pnProductNavContents, null),
            t = e.getPropertyValue("-webkit-transform") || e.getPropertyValue("transform"),
            n = Math.abs(parseInt(t.split(",")[4]) || 0);
        pnProductNavContents.style.transform = "none", pnProductNavContents.classList.add("pn-ProductNav_Contents-no-transition"), "left" === SETTINGS.navBarTravelDirection ? pnProductNav.scrollLeft = pnProductNav.scrollLeft - n : pnProductNav.scrollLeft = pnProductNav.scrollLeft + n, SETTINGS.navBarTravelling = !1
    }, !1), pnProductNavContents.addEventListener("click", function (e) {
        var t = [].slice.call(document.querySelectorAll(".pn-ProductNav_Link"));
        t.forEach(function (e) {
            e.setAttribute("aria-selected", "false")
        }), e.target.setAttribute("aria-selected", "true"), moveIndicator(e.target, colours[t.indexOf(e.target)])
    }), function (e, t) {
        "function" == typeof define && define.amd ? define(["exports"], t) : "undefined" != typeof exports ? t(exports) : t(e.dragscroll = {})
    }(this, function (e) {
        var t, n, a = window, o = document, s = [], r = function (e, r) {
            for (e = 0; e < s.length;) (r = (r = s[e++]).container || r).removeEventListener("mousedown", r.md, 0), a.removeEventListener("mouseup", r.mu, 0), a.removeEventListener("mousemove", r.mm, 0);
            for (s = [].slice.call(o.getElementsByClassName("dragscroll")), e = 0; e < s.length;) !function (e, s, r, i, l, c) {
                (c = e.container || e).addEventListener("mousedown", c.md = function (t) {
                    e.hasAttribute("nochilddrag") && o.elementFromPoint(t.pageX, t.pageY) != c || (i = 1, s = t.clientX, r = t.clientY, t.preventDefault())
                }, 0), a.addEventListener("mouseup", c.mu = function () {
                    i = 0
                }, 0), a.addEventListener("mousemove", c.mm = function (a) {
                    i && ((l = e.scroller || e).scrollLeft -= t = -s + (s = a.clientX), l.scrollTop -= n = -r + (r = a.clientY), e == o.body && ((l = o.documentElement).scrollLeft -= t, l.scrollTop -= n))
                }, 0)
            }(s[e++])
        };
        "complete" == o.readyState ? r() : a.addEventListener("load", r, 0), e.reset = r
    })
}
if (document.getElementsByClassName("sticky")[0]) {
    const e = $(".sticky");
    $("#com-rew-form");
    let t = e.offset().top, n = 0;
    window.addEventListener("scroll", a => {
        let o = $(this).scrollTop();
        t <= window.scrollY ? (e.addClass("sticky-active"), e.removeClass("sticky-active1")) : (console.log("else >"), e.removeClass("sticky-active")), o < n && t <= window.scrollY && (console.log("st<last_scroll"), console.log("st:", o), console.log("last_scroll:", n), e.addClass("sticky-active1")), n = o
    })
}

function toggleText(e, t) {
    e.html(t)
}

function copyURL() {
    var e = document.getElementById("exd-sr-input-url");
    e.select(), e.setSelectionRange(0, 99999), document.execCommand("copy")
}

$(".i-accordion").on("show.bs.collapse", function (e) {
    $(e.target).siblings(".panel-heading").find(".panel-title i").toggleClass("fa-chevron-down fa-chevron-up")
}), $(".i-accordion").on("hide.bs.collapse", function (e) {
    $(e.target).siblings(".panel-heading").find(".panel-title i").toggleClass("fa-chevron-up fa-chevron-down")
}), $(".accordion-3").on("show.bs.collapse", function (e) {
    $(e.target).siblings(".panel-heading").find(".panel-title i").toggleClass("fa-minus fa-plus")
}), $(".accordion-3").on("hide.bs.collapse", function (e) {
    $(e.target).siblings(".panel-heading").find(".panel-title i").toggleClass("fa-plus fa-minus")
}), $(document).ready(function () {
    function e(e, t) {
        "f" == t ? e.css("backgroundColor", "#09c75b") : e.css("backgroundColor", "#c2c2c2")
    }

    $(".company-follow").click(function (e) {
        e.preventDefault();
        var t = $(this);
        console.log(t);
        var n = t.attr("data-href");
        n && $.ajax({
            url: n, method: "GET", data: {}, success: function (e) {
                console.log(e.followed), 1 == e.followed ? toggleText(t, "Unfollow") : toggleText(t, "Follow")
            }, error: function (e) {
                console.log(e), console.log("error")
            }
        })
    }), $(".expert-follow").click(function (e) {
        console.log("1"), e.preventDefault();
        var t = $(this);
        console.log(t);
        var n = t.attr("data-href");
        console.log(n), n && $.ajax({
            url: n, method: "GET", data: {}, success: function (e) {
                console.log(e), 1 == e.followed ? toggleText(t, "UnFollow") : toggleText(t, "Follow")
            }, error: function (e) {
                console.log(e), console.log("error")
            }, statusCode: {
                403: function () {
                    $("#modalLogin").modal()
                }
            }
        })
    }), $(".ed-event-follow").click(function (e) {
        console.log("1"), e.preventDefault();
        var t = $(this);
        console.log(t);
        var n = t.attr("data-href");
        console.log(n), n && $.ajax({
            url: n, method: "GET", data: {}, success: function (e) {
                console.log(e), 1 == e.followed ? toggleText(t, "UnFollow") : toggleText(t, "Follow")
            }, error: function (e) {
                console.log(e), console.log("error")
            }, statusCode: {
                403: function () {
                    $("#modalLogin").modal()
                }
            }
        })
    }), $(document).on("click", ".event-follow", function (t) {
        t.preventDefault();
        var n = $(this);
        n.removeClass("event-follow-animate");
        var a = n.attr("data-href");
        a && $.ajax({
            url: a, method: "GET", data: {}, success: function (t) {
                1 == t.followed ? e(n, "f") : e(n, "u")
            }, error: function (e) {
                console.log(e), console.log("error")
            }, statusCode: {
                403: function () {
                    $("#modalLogin").modal()
                }
            }
        })
    }), $(".h-expert-follow").click(function (t) {
        t.preventDefault();
        var n = $(this);
        n.removeClass("h-expert-follow-animate");
        var a = n.attr("data-href");
        a && $.ajax({
            url: a, method: "GET", data: {}, success: function (t) {
                1 == t.followed ? e(n, "f") : e(n, "u")
            }, error: function (e) {
                console.log(e), console.log("error")
            }, statusCode: {
                403: function () {
                    $("#modalLogin").modal()
                }
            }
        })
    })
}), $(document).ready(function () {
    const e = $(".esf-form3-cont");
    e.hide(1e3), $(".esf-filter").on("click", () => {
        e.is(":visible") ? e.hide(1e3) : e.show(1e3)
    });
    const t = $(".skill-ghost");
    t.hide(1e3), $(".exd-sr-skill-rm").on("click", () => {
        t.is(":visible") ? (t.fadeOut(1e3), $(".exd-sr-skill-rm").text("see all Skills")) : (t.fadeIn(1e3), $(".exd-sr-skill-rm").text("see less Skill"))
    }), $(".e-list-slider").slick({
        infinite: !0,
        slidesToShow: 2,
        slidesToScroll: 2,
        autoplay: !1,
        centerMode: !1,
        variableWidth: !1,
        responsive: [{breakpoint: 1024, settings: {slidesToShow: 2, slidesToScroll: 2, infinite: !0}}, {
            breakpoint: 600,
            settings: {slidesToShow: 2, slidesToScroll: 2, centerMode: !1, variableWidth: !1}
        }, {breakpoint: 480, settings: {slidesToShow: 1, slidesToScroll: 1, centerMode: !1, variableWidth: !1}}]
    })
}), $("#exdeventfilter").change(function () {
    var e = $(this).val();
    "all" === e ? $(".exd-e-past").show() : $(".events-container").find('[data-event-type*="' + e + '"]').show()
}), $("#expert-paginate-by").change(function () {
    let e = document.getElementById("expert-paginate-by"), t = e.options[e.selectedIndex].text,
        n = $(".sr-filters .active a").attr("data-filter"),
        a = "?sort=" + $("#ex-sortby").val() + "&paginate_by=" + t + "&filter=" + n;
    window.location = a
}), $("#event-paginate-by").change(function () {
    let e = document.getElementById("event-paginate-by"), t = e.options[e.selectedIndex].text,
        n = $(".sr-filters .active a").attr("data-filter"),
        a = "allevents?sort=" + $("#ev-sortby").val() + "&paginate_by=" + t + "&filter=" + n;
    window.location = a
}), $(document).ready(function () {
    $(".exd-slider").owlCarousel({
        autoplay: !0,
        lazyLoad: !0,
        loop: !0,
        margin: 30,
        stagePadding: 75,
        dots: !1,
        nav: !0,
        responsiveClass: !0,
        autoHeight: !0,
        autoplayTimeout: 7e3,
        smartSpeed: 800,
        responsive: {0: {items: 1}, 600: {items: 3}, 1024: {items: 4}, 1366: {items: 4}}
    })
}), $(document).ready(function () {
    $("#btnExreadmore").on("click", e => {
        const t = $("#dots"), n = $("#more"), a = $("#btnExreadmore");
        e.preventDefault(), t.is(":visible") ? (t.hide(), a.text("Read less"), n.show(1e3)) : (t.show(), a.text("Read more"), n.hide(500))
    })
}), $(".nav-slider-con").hover(function () {
    $(this).find(".overlay").addClass("overlay-active-h")
}, function () {
    $(this).find(".overlay").removeClass("overlay-active-h")
}), $(".h-c-item-link").hover(function () {
    $(this).find(".overlay").addClass("overlay-active-h")
}, function () {
    $(this).find(".overlay").removeClass("overlay-active-h")
}), document.getElementById("reviews-list") && $("#exdeviewsort").change(function () {
    var e = $("#reviews-list"), t = $(".exd-r-review"), n = $(this).val();
    "latest" == n ? (t.each(function () {
        var e = $(this).attr("data-cdate"), t = new Date(e).getTime();
        $(this).attr("data-cdate", t)
    }), t.sort(function (e, t) {
        return (e = parseFloat($(e).attr("data-cdate"))) > (t = parseFloat($(t).attr("data-cdate"))) ? 1 : -1
    }).each(function () {
        e.prepend(this)
    })) : "sortby-r-asc" == n ? t.sort(function (e, t) {
        return (e = parseFloat($(e).attr("data-rating"))) < (t = parseFloat($(t).attr("data-rating"))) ? 1 : -1
    }).each(function () {
        e.prepend(this)
    }) : "sortby-r-desc" == n ? t.sort(function (e, t) {
        return (e = parseFloat($(e).attr("data-rating"))) > (t = parseFloat($(t).attr("data-rating"))) ? 1 : -1
    }).each(function () {
        e.prepend(this)
    }) : "withoutr" == n && t.each(function () {
        "0" == $(this).attr("data-rating") ? $(this).show() : $(this).hide()
    })
}), document.getElementById("search-result-cont") && $("#ex-sortby").change(function () {
    let e = "?sort=" + $("#ex-sortby").val() + "&paginate_by=" + $("#expert-paginate-by").val() + "&filter=" + $(".sr-filters .active a").attr("data-filter");
    window.location.href = window.location.href.replace(/[\?#].*|$/, e)
}), document.getElementById("search-result-cont") && $("#ev-sortby").change(function () {
    let e = "?sort=" + $("#ev-sortby").val() + "&paginate_by=" + $("#event-paginate-by").val() + "&filter=" + $(".sr-filters .active a").attr("data-filter");
    window.location.href = window.location.href.replace(/[\?#].*|$/, e)
}), $(document).on("submit", "#r-post-form", function (e) {
    var t = new FormData;
    let n = $("#r-id").val(), a = $("#c-id").val();
    t.append("r-title", $("#r-title").val()), t.append("r-company-position", $("#r-company-position").val()), t.append("stars", $("#stars").val()), t.append("r-review", $("#r-review").val()), t.append("r-tag", $("#r-tag").val()), $("#anon").is(":checked") && t.append("anon", $("#anon").val());
    var o = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "/review/submit-review/" + a + "/" + n,
        type: "POST",
        dataType: "json",
        processData: !1,
        data: t,
        contentType: !1,
        headers: {"X-CSRFToken": o},
        success: function (e) {
            for (var t in console.log(e), $("#r-post-form")[0].reset(), e_r_html = "", e) {
                r_id = e[t].id, r_cdate = new Date(e[t].creation_date), r_rating = e[t].score, r_title = e[t].content_title, r_username = e[t].username, r_content = e[t].content, r_anon = e[t].anon, r_position = e[t].position, r_flag = e[t].rating_flag, r_tag = e[t].tags, r_u_img_link = e[t].user.img, r_u_country = e[t].user.country, r_u_slug = e[t].user.slug, r_flag ? data_rating_new = r_rating : data_rating_new = 0, r_anon ? (html_anon = "Anonymous User from w" + r_u_country, html_img_link = "http://via.placeholder.com/106x106") : (html_anon = '<a href="users/' + r_u_slug + '">' + r_username + "</a>", html_img_link = r_u_img_link), r_rating_buttons = "", r_rating_class1 = "", r_rating_class2 = "", r_rating_class3 = "", r_rating_class4 = "", r_rating_class5 = "", r_flag ? (r_rating < 1 ? r_rating_class1 = "icon-unc-bg" : r_rating_class1 = "icon-c-bg", r_rating < 2 ? r_rating_class2 = "icon-unc-bg" : r_rating_class2 = "icon-c-bg", r_rating < 3 ? r_rating_class3 = "icon-unc-bg" : r_rating_class3 = "icon-c-bg", r_rating < 4 ? r_rating_class4 = "icon-unc-bg" : r_rating_class4 = "icon-c-bg", r_rating < 5 ? r_rating_class5 = "icon-unc-bg" : r_rating_class5 = "icon-c-bg", r_rating_buttons = r_rating_buttons + '<div class="expert-rating"><button type="button"class="btn btn-star-gray btn-xs ' + r_rating_class1 + '"aria-label="Left Align"><span class="fa fa-star btn-star"aria-hidden="true"></span></button><button type="button"class="btn btn-star-gray btn-xs ' + r_rating_class2 + '"aria-label="Left Align"><span class="fa fa-star btn-star"aria-hidden="true"></span></button><button type="button"class="btn btn-star-gray btn-xs ' + r_rating_class3 + '"aria-label="Left Align"><span class="fa fa-star btn-star"aria-hidden="true"></span></button><button type="button"class="btn btn-star-gray btn-xs ' + r_rating_class4 + '"aria-label="Left Align"><span class="fa fa-star btn-star"aria-hidden="true"></span></button><button type="button"class="btn btn-star-gray btn-xs ' + r_rating_class5 + '"aria-label="Left Align"><span class="fa fa-star btn-star"aria-hidden="true"></span></button></div>') : r_rating_buttons = "";
                var n = r_cdate.getFullYear(), a = r_cdate.getMonth() + 1, o = r_cdate.getDate(),
                    s = n + "-" + a + "-" + o + " " + r_cdate.getHours() + ":" + r_cdate.getMinutes();
                e_r_html = e_r_html + '<div class="row exd-r-review" id="rev' + r_id + '"data-cdate="' + s + '"data-rating="' + data_rating_new + '"><div class="col-md-2 col-12"><img class="exd-rr-profile-pic"src="' + html_img_link + '"><div class="exd-rr-info2"><div><h5 class="exd-rr-title">' + r_title + '</h5><p class="exd-rr-name-btitle"><span>' + html_anon + "</span>- " + r_position + "</p></div><div><p>" + s + '</p></div></div></div><div class="col-md-7 col-12"><div class="exd-rr-info"><h5 class="exd-rr-title">' + r_title + '</h5><p class="exd-rr-name-btitle"><span>' + html_anon + "</span>- " + r_position + '</p></div><div class="exd-rr-content"><p>' + r_content + '</p></div></div><div class="col-md-3 col-12"><div class="exd-rr-date"><p>' + (o + "-" + a + "-" + n) + '</p></div><div class="exd-rr-ss">' + r_rating_buttons + '<div class="review-label-speaker"><p>' + r_tag + "</p></div></div></div></div>"
            }
            $("#reviews-list").prepend(e_r_html)
        },
        error: function (e, t, n) {
            console.log(e.status + ": " + e.responseText)
        }
    }), e.preventDefault()
}), $(document).on("submit", "#r-event-form", function (e) {
    var t = new FormData;
    let n = $("#r-id").val();
    t.append("r-title", $("#r-title").val()), t.append("r-company-position", $("#r-company-position").val()), t.append("stars", $("#stars").val()), t.append("r-review", $("#r-review").val()), t.append("r-tag", $("#r-tag").val()), $("#anon").is(":checked") && t.append("anon", $("#anon").val());
    var a = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "/review/submit-review/event/" + n,
        type: "POST",
        dataType: "json",
        processData: !1,
        data: t,
        contentType: !1,
        headers: {"X-CSRFToken": a},
        success: function (e) {
            console.log(e)
        },
        error: function (e, t, n) {
            console.log(e.status + ": " + e.responseText)
        }
    }), e.preventDefault()
});
const ghost_exp = $(".exp-more");
ghost_exp.hide(1e3), $(".h-ex-load-more").on("click", () => {
    ghost_exp.is(":visible") ? (ghost_exp.fadeOut(1e3), $(".h-ex-load-more").text("Load More Experts")) : (ghost_exp.fadeIn(1e3), $(".h-ex-load-more").text("See Less Expert"))
});
const ghost_ev = $(".ev-more");
ghost_ev.hide(1e3), $(".h-ev-load-more").on("click", () => {
    ghost_ev.is(":visible") ? (ghost_ev.fadeOut(1e3), $(".h-ev-load-more").text("Load More Events")) : (ghost_ev.css("display", "flex").hide().fadeIn(1e3), $(".h-ev-load-more").text("See Less Event"))
});
const ghost_ven = $(".ven-more");
ghost_ven.hide(1e3), $(".h-ven-load-more").on("click", () => {
    ghost_ven.is(":visible") ? (ghost_ven.fadeOut(1e3), $(".h-ven-load-more").text("Load More Venues")) : (ghost_ven.css("display", "flex").hide().fadeIn(1e3), $(".h-ven-load-more").text("See Less Venue"))
});
const ghost_st = $(".st-more");

function getCookie(e) {
    for (var t = e + "=", n = decodeURIComponent(document.cookie).split(";"), a = 0; a < n.length; a++) {
        for (var o = n[a]; " " == o.charAt(0);) o = o.substring(1);
        if (0 == o.indexOf(t)) return o.substring(t.length, o.length)
    }
    return ""
}

function openForm() {
    $("#myForm").slideDown(), $.cookie("tdisplay", 1, {path: "/"})
}

function closeForm() {
    $("#myForm").slideUp(), $.cookie("tdisplay", 0, {path: "/"})
}

function share(e) {
    console.log(e);
    let t = "#sh" + e;
    $(t).is(":visible") ? $(t).fadeOut(1e3) : $(t).hide().fadeIn(1e3)
}

ghost_st.hide(1e3), $(".h-st-load-more").on("click", () => {
    ghost_st.is(":visible") ? (ghost_st.fadeOut(1e3), $(".h-st-load-more").text("Load More Start Up")) : (ghost_st.css("display", "flex").hide().fadeIn(1e3), $(".h-st-load-more").text("See Less Start Up"))
}), window.matchMedia("(max-width: 768px)").matches && ($(".slick-fe").slick({
    slidesToScroll: 1,
    autoplay: !0,
    slidesToShow: 1,
    speed: 1e3,
    dots: !0,
    prevArrow: '<button class="slide-arrow prev-arrow">&lt;</button>',
    nextArrow: '<button class="slide-arrow next-arrow">&gt;</button>'
}), $(".slick-ex").slick({
    slidesToScroll: 1,
    autoplay: !1,
    slidesToShow: 1,
    speed: 1e3,
    dots: !0,
    prevArrow: '<button class="slide-arrow prev-arrow">&lt;</button>',
    nextArrow: '<button class="slide-arrow next-arrow">&gt;</button>'
}), $(".slick-cat-org").slick({
    slidesToScroll: 1,
    autoplay: !1,
    slidesToShow: 1,
    speed: 1e3,
    dots: !0,
    prevArrow: '<button class="slide-arrow prev-arrow">&lt;</button>',
    nextArrow: '<button class="slide-arrow next-arrow">&gt;</button>'
})), $(document).ready(function () {
    $(".ed-slider1").slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: !0,
        centerPadding: 20,
        centerMode: !0,
        prevArrow: '<button class="slide-arrow prev-arrow">&lt;</button>',
        nextArrow: '<button class="slide-arrow next-arrow">&gt;</button>',
        responsive: [{breakpoint: 1024, settings: {slidesToShow: 3, slidesToScroll: 3}}, {
            breakpoint: 600,
            settings: {slidesToShow: 2, slidesToScroll: 2}
        }, {breakpoint: 480, settings: {slidesToShow: 1, slidesToScroll: 1}}]
    })
}), $(document).ready(function () {
    1 == $.cookie("tdisplay") ? $("#myForm").slideDown() : $("#myForm").slideUp()
}), $(document).on("click", ".h-ex-filter-btn", function (e) {
    e.preventDefault();
    let t = $(this).attr("data-filter"), n = "col-12 col-md-4 col-lg-4 mt-4 card-deck";
    if (n = "home" == $(this).attr("data-source") ? "col-12 col-md-4 col-lg-4 mt-4 card-deck" : "col-12 col-md-6 col-lg-6 mt-4", "anon" == t) $("#event-container").html('<div class="d-flex justify-content-center p-5 mt-3 rounded shadow for-you-login-con"><h4 class="text-muted text-center m-0">Please <a class="for-you-login" href="/users/login/" >sign in</a> to See Personalized Events</h4></div>'), $("#event-container").removeClass("justify-content-between"), $("#event-container").addClass("justify-content-center"); else {
        if ($("#event-container").removeClass("justify-content-center"), $("#event-container").addClass("justify-content-between"), "free" == t) var a = {price: "free"}; else if ("for-you" == t) a = {special: "for-you"}; else if ("*" == t) a = {all: t}; else a = {dates: t};
        var o = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/events/api/events/search",
            type: "POST",
            dataType: "json",
            processData: !1,
            data: JSON.stringify(a),
            contentType: "application/json;charset=utf-8",
            headers: {"X-CSRFToken": o},
            success: function (e) {
                console.log(e), e_r_html = "";
                const t = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
                for (var a in e) {
                    e_id = e[a].id, e_name = e[a].name, e_cdate = new Date(e[a].start_event_dt), e_img_link = e[a].event_img;
                    var o = e_cdate.getMonth(), s = e_cdate.getDate();
                    s < 10 && (s = "0" + s), e_link = e[a].slug, e_city = e[a].city, loc = e[a].location, e_location = loc, follower_list = e[a].follower_list, follower_list ? html_follow_style = 'style="color: #fff; background-color: #09c75b"' : html_follow_style = 'style="color: #fff; background-color: #c2c2c2"', e_r_html = e_r_html + '<div class="' + n + '"><div class="card-h-e card"><div><a href="events/' + e_link + '"><img class="card-img-top" src="' + e_img_link + '"></a></div><div class="card-block"><figure class="profile shadow"><span class="profile-avatar">' + t[o] + " " + s + '</span></figure><div class="card-text text-right"><a> cat </a></div><a href="' + e_link + '"class="card-title mt-3 h5 v-link">' + e_name + '</a><div class="meta"><p>' + e_city + "," + e_location + '</p></div></div><div class="card-footer"><a href="events/' + e_link + '" class="card-att-event">Attend this event</a><button class="c-icon" data-href="event_follow_url"><i class="fa  fa-heart event-follow "data-href="/api/events/' + e_link + '/follow"' + html_follow_style + '></i></button><button class="c-icon btn-share" id="' + e_id + '" onclick="share(this.id)"><i style="color:#fff"class="fa fa-share"></i></button></div></div><div id="sh' + e_id + '" class="shadow soc-share-con" style="display: none"><div className="btn-group soc-share"><button className="btn btn-default disabled">Share:</button><a className="btn btn-default" target="_blank" title="On Facebook"href="https://www.facebook.com/sharer.php?u=' + window.location.href + '"><i className="fa fa-facebook fa-lg fb"></i></a><a className="btn btn-default" target="_blank" title="On Twitter"href="https://twitter.com/share?url=' + window.location.href + '"><i className="fa fa-twitter fa-lg tw"></i></a><a className="btn btn-default" target="_blank" title="On LinkedIn"href="https://www.linkedin.com/shareArticle?mini=true&amp;url=' + window.location.href + '"><i className="fa fa-linkedin fa-lg linkin"></i></a><a className="btn btn-default" target="_blank" title="On VK.com"href="https://vk.com/share.php?url=' + window.location.href + '"><i className="fa fa-vk fa-lg vk"></i></a><a className="btn btn-default" target="_blank" title="Pin It"href="https://www.pinterest.com/pin/create/button/?url=' + window.location.href + '"><i className="fa fa-pinterest fa-lg pinterest"></i></a></div></div></div>'
                }
                $("#event-container").html(e_r_html)
            },
            error: function (e, t, n) {
                console.log(e.status + ": " + e.responseText)
            }
        })
    }
    e.preventDefault()
});
var lih = $(".h-ev-filters li");
lih.click(function () {
    lih.removeClass("active"), $(this).addClass("active")
});
var liex = $(".sr-filters li");

function makeid(e) {
    for (var t = "", n = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", a = n.length, o = 0; o < e; o++) t += n.charAt(Math.floor(Math.random() * a));
    return t
}

liex.click(function () {
    liex.removeClass("active"), $(this).addClass("active")
}), $(document).on("click", ".aev-filter-btn", function (e) {
    e.preventDefault();
    let t = $(this).attr("data-filter"), n = "col-12 col-md-4 col-lg-4 mt-4 card-deck";
    if (n = "home" == $(this).attr("data-source") ? "col-12 col-md-4 col-lg-4 mt-4 card-deck" : "col-12 col-md-6 col-lg-6 mt-4", "anon" == t) $("#event-container").html('<div class="d-flex justify-content-center p-5 mt-3 rounded shadow for-you-login-con"><h4 class="text-muted text-center m-0">Please <a class="for-you-login" href="/users/login/" >sign in</a> to See Personalized Events</h4></div>'), $("#event-container").removeClass("justify-content-between"), $("#event-container").addClass("justify-content-center"); else {
        let e = document.getElementById("event-paginate-by"), n = e.options[e.selectedIndex].text, a = t,
            o = "allevents?sort=" + $("#ev-sortby").val() + "&paginate_by=" + n + "&filter=" + a;
        window.location = o
    }
    e.preventDefault()
}), $(document).on("click", ".aex-filter-btn", function (e) {
    e.preventDefault();
    let t = $(this).attr("data-filter"), n = document.getElementById("expert-paginate-by"),
        a = n.options[n.selectedIndex].text, o = t,
        s = "experts?sort=" + $("#ex-sortby").val() + "&paginate_by=" + a + "&filter=" + o;
    window.location = s, e.preventDefault()
}), $(document).on("click", '[data-toggle="lightbox"]', function (e) {
    e.preventDefault(), $(this).ekkoLightbox()
}), $(".submit-btn").click(function () {
    var e = $(".email").val();
    if (!/^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/.test(e)) return $(".email").css("border-color", "red"), !1
}), screen.width < 768 ? $(".profile-sidebar").addClass("active") : $(".profile-sidebar").removeClass("active"), $("#com-primary-address").popover(), $("#com-primary-address").popover({trigger: "hover"}), $(document).ready(function () {
    $(".rel-com-slider").slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: !1,
        centerPadding: 10,
        centerMode: !0,
        responsive: [{breakpoint: 1024, settings: {slidesToShow: 3, slidesToScroll: 3}}, {
            breakpoint: 600,
            settings: {slidesToShow: 2, slidesToScroll: 2}
        }, {breakpoint: 480, settings: {slidesToShow: 1, slidesToScroll: 1}}]
    })
}), $("#btnaddcompany").click(function () {
    var e = function (e) {
        var t = null;
        if (document.cookie && "" !== document.cookie) for (var n = document.cookie.split(";"), a = 0; a < n.length; a++) {
            var o = jQuery.trim(n[a]);
            if (o.substring(0, e.length + 1) === e + "=") {
                t = decodeURIComponent(o.substring(e.length + 1));
                break
            }
        }
        return t
    }("csrftoken");
    $.ajaxSetup({
        beforeSend: function (t, n) {
            var a;
            a = n.type, /^(GET|HEAD|OPTIONS|TRACE)$/.test(a) || this.crossDomain || t.setRequestHeader("X-CSRFToken", e)
        }
    });
    var t = $("#ac-logo").prop("files")[0], n = new FormData;
    n.append("name", $("#ac-name").val()), n.append("address", $("#ac-address").val()), n.append("linkedin", $("#ac-linkedin").val()), n.append("twitter", $("#ac-twitter").val()), n.append("website", $("#ac-website").val()), n.append("facebook", $("#ac-facebook").val()), n.append("info", $("#ac-info").val()), n.append("ctype", $("#ac-type").val()), n.append("founded", $("#ac-founded").val()), n.append("size", $("#ac-size").val()), n.append("file", t);
    let a = "notstartup";
    !0 === $("#ac-startup").checked && (a = $("#ac-startup").val()), n.append("startup", a), $.ajax({
        url: "/companies/add_company/",
        type: "POST",
        dataType: "json",
        processData: !1,
        data: n,
        contentType: !1,
        success: function (e) {
            new Noty({
                type: "success",
                layout: "center",
                text: "Company Successufly Registered",
                closeWith: ["click", "button"],
                animation: {open: "animated fadeInDown", close: "animated fadeOutUp"}
            }).show()
        },
        error: function (e, t, n) {
            new Noty({
                type: "error",
                layout: "center",
                text: "Oops! We have encountered an error: " + n,
                closeWith: ["click", "button"],
                animation: {open: "animated fadeInDown", close: "animated fadeOutUp"}
            }).show()
        }
    })
}), $("#company-paginate-by").change(function () {
    let e = document.getElementById("company-paginate-by"), t = e.options[e.selectedIndex].text,
        n = "/companies?sort=" + $("#com-sortby").val() + "&paginate_by=" + t;
    window.location = n
}), document.getElementById("search-result-cont") && $("#com-sortby").change(function () {
    let e = "?sort=" + $("#com-sortby").val() + "&paginate_by=" + $("#company-paginate-by").val();
    window.location.href = window.location.href.replace(/[\?#].*|$/, e)
});

// lazy load
/*!
 * Lazy Load - jQuery plugin for lazy loading images
 *
 * Copyright (c) 2007-2015 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.appelsiini.net/projects/lazyload
 *
 * Version:  1.9.7
 *
 */

(function($, window, document, undefined) {
    var $window = $(window);

    $.fn.lazyload = function(options) {
        var elements = this;
        var $container;
        var settings = {
            threshold       : 0,
            failure_limit   : 0,
            event           : "scroll",
            effect          : "show",
            container       : window,
            data_attribute  : "original",
            skip_invisible  : false,
            appear          : null,
            load            : null,
            placeholder     : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC"
        };

        function update() {
            var counter = 0;

            elements.each(function() {
                var $this = $(this);
                if (settings.skip_invisible && !$this.is(":visible")) {
                    return;
                }
                if ($.abovethetop(this, settings) ||
                    $.leftofbegin(this, settings)) {
                        /* Nothing. */
                } else if (!$.belowthefold(this, settings) &&
                    !$.rightoffold(this, settings)) {
                        $this.trigger("appear");
                        /* if we found an image we'll load, reset the counter */
                        counter = 0;
                } else {
                    if (++counter > settings.failure_limit) {
                        return false;
                    }
                }
            });

        }

        if(options) {
            /* Maintain BC for a couple of versions. */
            if (undefined !== options.failurelimit) {
                options.failure_limit = options.failurelimit;
                delete options.failurelimit;
            }
            if (undefined !== options.effectspeed) {
                options.effect_speed = options.effectspeed;
                delete options.effectspeed;
            }

            $.extend(settings, options);
        }

        /* Cache container as jQuery as object. */
        $container = (settings.container === undefined ||
                      settings.container === window) ? $window : $(settings.container);

        /* Fire one scroll event per scroll. Not one scroll event per image. */
        if (0 === settings.event.indexOf("scroll")) {
            $container.bind(settings.event, function() {
                return update();
            });
        }

        this.each(function() {
            var self = this;
            var $self = $(self);

            self.loaded = false;

            /* If no src attribute given use data:uri. */
            if ($self.attr("src") === undefined || $self.attr("src") === false) {
                if ($self.is("img")) {
                    $self.attr("src", settings.placeholder);
                }
            }

            /* When appear is triggered load original image. */
            $self.one("appear", function() {
                if (!this.loaded) {
                    if (settings.appear) {
                        var elements_left = elements.length;
                        settings.appear.call(self, elements_left, settings);
                    }
                    $("<img />")
                        .bind("load", function() {

                            var original = $self.attr("data-" + settings.data_attribute);
                            $self.hide();
                            if ($self.is("img")) {
                                $self.attr("src", original);
                            } else {
                                $self.css("background-image", "url('" + original + "')");
                            }
                            $self[settings.effect](settings.effect_speed);

                            self.loaded = true;

                            /* Remove image from array so it is not looped next time. */
                            var temp = $.grep(elements, function(element) {
                                return !element.loaded;
                            });
                            elements = $(temp);

                            if (settings.load) {
                                var elements_left = elements.length;
                                settings.load.call(self, elements_left, settings);
                            }
                        })
                        .attr("src", $self.attr("data-" + settings.data_attribute));
                }
            });

            /* When wanted event is triggered load original image */
            /* by triggering appear.                              */
            if (0 !== settings.event.indexOf("scroll")) {
                $self.bind(settings.event, function() {
                    if (!self.loaded) {
                        $self.trigger("appear");
                    }
                });
            }
        });

        /* Check if something appears when window is resized. */
        $window.bind("resize", function() {
            update();
        });

        /* With IOS5 force loading images when navigating with back button. */
        /* Non optimal workaround. */
        if ((/(?:iphone|ipod|ipad).*os 5/gi).test(navigator.appVersion)) {
            $window.bind("pageshow", function(event) {
                if (event.originalEvent && event.originalEvent.persisted) {
                    elements.each(function() {
                        $(this).trigger("appear");
                    });
                }
            });
        }

        /* Force initial check if images should appear. */
        $(document).ready(function() {
            update();
        });

        return this;
    };

    /* Convenience methods in jQuery namespace.           */
    /* Use as  $.belowthefold(element, {threshold : 100, container : window}) */

    $.belowthefold = function(element, settings) {
        var fold;

        if (settings.container === undefined || settings.container === window) {
            fold = (window.innerHeight ? window.innerHeight : $window.height()) + $window.scrollTop();
        } else {
            fold = $(settings.container).offset().top + $(settings.container).height();
        }

        return fold <= $(element).offset().top - settings.threshold;
    };

    $.rightoffold = function(element, settings) {
        var fold;

        if (settings.container === undefined || settings.container === window) {
            fold = $window.width() + $window.scrollLeft();
        } else {
            fold = $(settings.container).offset().left + $(settings.container).width();
        }

        return fold <= $(element).offset().left - settings.threshold;
    };

    $.abovethetop = function(element, settings) {
        var fold;

        if (settings.container === undefined || settings.container === window) {
            fold = $window.scrollTop();
        } else {
            fold = $(settings.container).offset().top;
        }

        return fold >= $(element).offset().top + settings.threshold  + $(element).height();
    };

    $.leftofbegin = function(element, settings) {
        var fold;

        if (settings.container === undefined || settings.container === window) {
            fold = $window.scrollLeft();
        } else {
            fold = $(settings.container).offset().left;
        }

        return fold >= $(element).offset().left + settings.threshold + $(element).width();
    };

    $.inviewport = function(element, settings) {
         return !$.rightoffold(element, settings) && !$.leftofbegin(element, settings) &&
                !$.belowthefold(element, settings) && !$.abovethetop(element, settings);
     };

    /* Custom selectors for your convenience.   */
    /* Use as $("img:below-the-fold").something() or */
    /* $("img").filter(":below-the-fold").something() which is faster */

    $.extend($.expr[":"], {
        "below-the-fold" : function(a) { return $.belowthefold(a, {threshold : 0}); },
        "above-the-top"  : function(a) { return !$.belowthefold(a, {threshold : 0}); },
        "right-of-screen": function(a) { return $.rightoffold(a, {threshold : 0}); },
        "left-of-screen" : function(a) { return !$.rightoffold(a, {threshold : 0}); },
        "in-viewport"    : function(a) { return $.inviewport(a, {threshold : 0}); },
        /* Maintain BC for couple of versions. */
        "above-the-fold" : function(a) { return !$.belowthefold(a, {threshold : 0}); },
        "right-of-fold"  : function(a) { return $.rightoffold(a, {threshold : 0}); },
        "left-of-fold"   : function(a) { return !$.rightoffold(a, {threshold : 0}); }
    });

})(jQuery, window, document);
$(document).ready(function(){
  $('img.lazy').lazyload({
    effect: "fadeIn"
  });
});