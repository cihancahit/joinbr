//DOM elements
const DOMstrings = {
    stepsBtnClass: 'multisteps-form__progress-btn',
    stepsBtns: document.querySelectorAll(`.multisteps-form__progress-btn`),
    stepsBar: document.querySelector('.multisteps-form__progress'),
    stepsForm: document.querySelector('.multisteps-form__form'),
    stepsFormTextareas: document.querySelectorAll('.multisteps-form__textarea'),
    stepFormPanelClass: 'multisteps-form__panel',
    stepFormPanels: document.querySelectorAll('.multisteps-form__panel'),
    stepPrevBtnClass: 'js-btn-prev',
    stepNextBtnClass: 'js-btn-next'
};


//remove class from a set of items
const removeClasses = (elemSet, className) => {

    elemSet.forEach(elem => {

        elem.classList.remove(className);

    });

};

//return exect parent node of the element
const findParent = (elem, parentClass) => {

    let currentNode = elem;

    while (!currentNode.classList.contains(parentClass)) {
        currentNode = currentNode.parentNode;
    }

    return currentNode;

};

//get active button step number
const getActiveStep = elem => {
    return Array.from(DOMstrings.stepsBtns).indexOf(elem);
};

//set all steps before clicked (and clicked too) to active
const setActiveStep = activeStepNum => {

    //remove active state from all the state
    removeClasses(DOMstrings.stepsBtns, 'js-active');

    //set picked items to active
    DOMstrings.stepsBtns.forEach((elem, index) => {

        if (index <= activeStepNum) {
            elem.classList.add('js-active');
        }

    });
};

//get active panel
const getActivePanel = () => {

    let activePanel;

    DOMstrings.stepFormPanels.forEach(elem => {

        if (elem.classList.contains('js-active')) {

            activePanel = elem;

        }

    });

    return activePanel;

};

//open active panel (and close unactive panels)
const setActivePanel = activePanelNum => {

    //remove active class from all the panels
    removeClasses(DOMstrings.stepFormPanels, 'js-active');

    //show active panel
    DOMstrings.stepFormPanels.forEach((elem, index) => {
        if (index === activePanelNum) {

            elem.classList.add('js-active');

            setFormHeight(elem);

        }
    });

};

//set form height equal to current panel height
const formHeight = activePanel => {

    const activePanelHeight = activePanel.offsetHeight;

    DOMstrings.stepsForm.style.height = `${activePanelHeight}px`;

};

const setFormHeight = () => {
    const activePanel = getActivePanel();

    formHeight(activePanel);
};

//STEPS BAR CLICK FUNCTION
DOMstrings.stepsBar.addEventListener('click', e => {

    //check if click target is a step button
    const eventTarget = e.target;

    if (!eventTarget.classList.contains(`${DOMstrings.stepsBtnClass}`)) {
        return;
    }

    //get active button step number
    const activeStep = getActiveStep(eventTarget);

    //set all steps before clicked (and clicked too) to active
    setActiveStep(activeStep);

    //open active panel
    setActivePanel(activeStep);
});

//PREV/NEXT BTNS CLICK
DOMstrings.stepsForm.addEventListener('click', e => {

    const eventTarget = e.target;

    //check if we clicked on `PREV` or NEXT` buttons
    if (!(eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`) || eventTarget.classList.contains(`${DOMstrings.stepNextBtnClass}`))) {
        return;
    }

    //find active panel
    const activePanel = findParent(eventTarget, `${DOMstrings.stepFormPanelClass}`);

    let activePanelNum = Array.from(DOMstrings.stepFormPanels).indexOf(activePanel);

    //set active step and active panel onclick
    if (eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`)) {
        activePanelNum--;

    } else {

        activePanelNum++;

    }

    setActiveStep(activePanelNum);
    setActivePanel(activePanelNum);

});

//SETTING PROPER FORM HEIGHT ONLOAD
window.addEventListener('load', setFormHeight, false);

//SETTING PROPER FORM HEIGHT ONRESIZE
window.addEventListener('resize', setFormHeight, false);

// expert profile create event tag list update
function updateTag(new_tag) {
    let ep_ce_tags = $('#ep_ce_tags').val().split(';');
    ep_ce_tags.push(new_tag);
    $('#exp_skills').val(ep_ce_tags.join(';'));
    new_li = '<li id="sev" data-value="' + new_tag + '">' + new_tag + ' <span class="rmTag">x</span></li>';
    new_li2 = '<li id="sev" data-value="' + new_tag + '">' + new_tag + '</li>';
    $('.tagListCe').append(new_li);
    $('.tagListP').append(new_li2);
}

$('.tagListCe').on('click', '.rmTag', function () {
    let tag = $(this).parent().attr('data-value');
    console.log(tag);
    let ep_ce_tags = $('#ep_ce_tags').val().split(';');
    console.log(ep_ce_tags);
    ep_ce_tags.splice($.inArray(tag, ep_ce_tags), 1);
    $('#ep_ce_tags').val(ep_ce_tags.join(';'));
    $(this).parent().remove();
});

//expert profile create event dynamically adding new price&ticket input
function GetDynamicTextBox(name) {
    return '<div class="form-group col-md-6 pl-0">\n' +
        '                                                    <div class="inner-addon left-addon">\n' +
        '                                                        <i class="fa fa-dollar"></i>\n' +
        '                                                        <input type="number" class="form-control jb-input-ce ep-ce-tp"\n' +
        '                                                               autocomplete="off"\n' +
        '                                                               name="ep-ce-pt-' + name + '-price"\n' +
        'id = "' + name + 'p"' +
        '                                                               value="">\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                                <div class="form-group col-md-5 pl-0">\n' +
        '                                                    <input type="text" class="form-control jb-input-w p-2 ep-ce-tt"\n' +
        '                                                           autocomplete="off"\n' +
        'id = "' + name + 't"' +
        '                                                           name="ep-ce-pt-' + name + '-title"\n' +
        '                                                           value="">\n' +
        '                                                </div>'
}

//expert profile create event dynamically adding new price&ticket input
function GetDynamicTextBoxP(name) {
    return '<div class="col-6"><div id="ep-ce-init" class="p-2 pticket-p-meta">\n' +
        '                                                <h6 class="pprice" id="' + name + 'pp">$</h6>\n' +
        '                                                <p class="pinfo" id="' + name + 'tp">&nbsp;</p>\n' +
        '                                            </div></div>'
}
$(function () {
    $(".ep-ce-add-new-input").bind("click", function () {
        let div = $("<div>");
        let new_name = makeid(5);
        let ticket_count = $('.ep-ce-tt').length +1;
        if (ticket_count<5){

        $("#ep-ce-pt-row").append(GetDynamicTextBox(new_name));
        $(".pticket-price").append(GetDynamicTextBoxP(new_name));
        let pt_list = $('#ep-ce-pt-list').val().split(';');
        pt_list.push(new_name);
        $('#ep-ce-pt-list').val(pt_list.join(';'));
        }else {
              $(document).ready(function () {
                        new Noty({
                            type: 'error',
                            layout: 'center',
                            text: 'You can not add more than 5 ticket',
                            closeWith: ['click', 'button'],
                            animation: {
                                open: 'animated fadeInDown', // Animate.css class names
                                close: 'animated fadeOutUp' // Animate.css class names
                            }
                        }).show()
                    })
        }
    });
    $("body").on("click", ".remove", function () {
        $(this).closest("tr").remove();
    });
});

//adding dynamically ticket price and title to preview
$("body").on("keyup", ".ep-ce-tp", function (e) {
    let id = e.target.id;
    let new_id = id + 'p';
    $('#' + new_id).html('$ ' + $(this).val())
});

$("body").on("keyup", ".ep-ce-tt", function (e) {
    let id = e.target.id;
    let new_id = id + 'p';
    console.log(new_id);
    $('#' + new_id).html($(this).val());
});

$("body").on("keyup", "#ep-ce-lrefund", function (e) {
    $('.prefund-link').attr("href", $(this).val());
    $('.prefund-link').html('<span class="fa fa-chain mr-2"></span>' + $(this).val());
});

$("body").on("keyup", "#ep-ce-contactemail", function (e) {
    $('.prefund-email').attr("href", 'mailto:' + $(this).val());
    $('.prefund-email').html('<span class="fa fa-envelope mr-2"></span>' + $(this).val());
});

function noRefund() {
    if ($('#ep-ce-norefund').is(":checked")) {
        $("#prefund-links").hide();
        $('.prefund-title').html('<span class="fa fa-times mr-2"></span>No refund Policy');
    } else {
        $("#prefund-links").show();
        $('.prefund-title').html('<span class="fa fa-check mr-2"></span>With refund Policy');
    }
};

// ep create event update speaker list
function updateSpeakerList(img, name, slug, id) {
    // let skill = $(this).parent().attr('data-value');
    // let exp_skills = $('#exp_skills').val().split(';');
    // exp_skills.push(new_skill);
    // $('#exp_skills').val(exp_skills.join(';'));
    new_coll = ' <div class="col-4 mt-4" id="'+id+'" data-value="'+id+'">\n' +
        '                                                <span class="exp-col-x">x</span>\n' +
        '                                                <div class="exp-coll-block px-1 py-3">\n' +
        '                                                    <div class="row align-items-center">\n' +
        '                                                        <div class="col-2">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-img-link"><img\n' +
        '                                                                    src="' + img + '"\n' +
        '                                                                    alt="' + name + '" class=""></a>\n' +
        '                                                        </div>\n' +
        '                                                        <div class="col-10">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-name h5">' + name + '</a>\n' +
        '                                                        </div>\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                            </div>';
       new_coll1 = ' <div class="col-6 mt-1" id="'+id+'" data-value="'+id+'">\n' +
        '                                                <div class="exp-coll-block px-1 py-2">\n' +
        '                                                    <div class="row align-items-center">\n' +
        '                                                        <div class="col-2">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-img-link"><img\n' +
        '                                                                    src="' + img + '"\n' +
        '                                                                    alt="' + name + '" class=""></a>\n' +
        '                                                        </div>\n' +
        '                                                        <div class="col-10">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-name h5">' + name + '</a>\n' +
        '                                                        </div>\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                            </div>';
    $('#ep-ce-speaker-list').append(new_coll);
    $('#pspeaker-list').append(new_coll1);

}

function updateCompanyList(img, name, slug, id) {
    // let skill = $(this).parent().attr('data-value');
    // let exp_skills = $('#exp_skills').val().split(';');
    // exp_skills.push(new_skill);
    // $('#exp_skills').val(exp_skills.join(';'));
    new_coll = ' <div class="col-4 mt-4">\n' +
        '                                                <span class="exp-col-x">x</span>\n' +
        '                                                <div class="exp-coll-block px-1 py-3">\n' +
        '                                                    <div class="row align-items-center">\n' +
        '                                                        <div class="col-2">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-img-link"><img\n' +
        '                                                                    src="' + img + '"\n' +
        '                                                                    alt="' + name + '" class=""></a>\n' +
        '                                                        </div>\n' +
        '                                                        <div class="col-10">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-name h5">' + name + '</a>\n' +
        '                                                        </div>\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                            </div>';
    $('#ep-ce-sponsor-list').append(new_coll);
}

function updateOrganizerList(img, name, slug, id) {
    new_coll = ' <div class="col-4 mt-4">\n' +
        '                                                <span class="exp-col-x">x</span>\n' +
        '                                                <div class="exp-coll-block px-1 py-3">\n' +
        '                                                    <div class="row align-items-center">\n' +
        '                                                        <div class="col-2">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-img-link"><img\n' +
        '                                                                    src="' + img + '"\n' +
        '                                                                    alt="' + name + '" class=""></a>\n' +
        '                                                        </div>\n' +
        '                                                        <div class="col-10">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-name h5">' + name + '</a>\n' +
        '                                                        </div>\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                            </div>';
    $('#ep-ce-org-list').append(new_coll);
}

function updateHostList(img, name, slug, id) {
    new_coll = ' <div class="col-4 mt-4">\n' +
        '                                                <span class="exp-col-x">x</span>\n' +
        '                                                <div class="exp-coll-block px-1 py-3">\n' +
        '                                                    <div class="row align-items-center">\n' +
        '                                                        <div class="col-2">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-img-link"><img\n' +
        '                                                                    src="' + img + '"\n' +
        '                                                                    alt="' + name + '" class=""></a>\n' +
        '                                                        </div>\n' +
        '                                                        <div class="col-10">\n' +
        '                                                            <a href="' + slug + '" class="exp-coll-name h5">' + name + '</a>\n' +
        '                                                        </div>\n' +
        '                                                    </div>\n' +
        '                                                </div>\n' +
        '                                            </div>';
    $('#ep-ce-host-list').append(new_coll);
}

$(document).ready(function () {
    console.log('salala');
    $("#ep_ce_tag_search").autocomplete({
        source: "/events/ac/search/tag",
        minLength: 2,
        messages: {
            noResults: '',
            results: function () {
            }
        },
        open: function () {
            setTimeout(function () {
                $('.ui-autocomplete').css('z-index', 99);
            }, 0);
        }
        ,
        select: function (e, ui) {
            updateTag(ui.item.value);
        }
    });

    // ep create event search speaker
    $("#ep-ce-search-speaker").autocomplete({
        minLength: 0,
        source: "/experts/ac/search/e/name/col",
        dataType: 'html',
        focus: function (event, ui) {
            $("#ep-ce-search-speaker").val(ui.item.name);
            return false;
        },
        select: function (event, ui) {
            updateSpeakerList(ui.item.img, ui.item.name, ui.item.slug, ui.item.id);
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li>")
            .append('<div><img style="height: 25px; width: 25px; border-radius:50%" src="' + (item.img) + '">  ' + item.name + '</div>')
            .appendTo(ul);
    };

    //ep create event search company
    $("#ep-ce-search-sponsor").autocomplete({
        minLength: 0,
        source: "/companies/ac/search/c/name/profile",
        dataType: 'html',
        focus: function (event, ui) {
            $("#ep-ce-search-sponsor").val(ui.item.name);
            return false;
        },
        select: function (event, ui) {
            // $("#exp_search_coll").val(ui.item.name);
            updateCompanyList(ui.item.img, ui.item.name, ui.item.slug)
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li>")
            .append('<div><img style="height: 25px; width: 25px; border-radius:50%" src="' + (item.img) + '">  ' + item.name + '</div>')
            .appendTo(ul);
    };
    //ep create event search organizer
    $("#ep-ce-search-org").autocomplete({
        minLength: 0,
        source: "/companies/ac/search/c/name/profile",
        dataType: 'html',
        focus: function (event, ui) {
            $("#ep-ce-search-org").val(ui.item.name);
            return false;
        },
        select: function (event, ui) {
            // $("#exp_search_coll").val(ui.item.name);
            updateOrganizerList(ui.item.img, ui.item.name, ui.item.slug)
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li>")
            .append('<div><img style="height: 25px; width: 25px; border-radius:50%" src="' + (item.img) + '">  ' + item.name + '</div>')
            .appendTo(ul);
    };
    // ep create event search hosts
    $("#ep-ce-search-host").autocomplete({
        minLength: 0,
        source: "/companies/ac/search/c/name/profile",
        dataType: 'html',
        focus: function (event, ui) {
            $("#ep-ce-search-host").val(ui.item.name);
            return false;
        },
        select: function (event, ui) {
            updateHostList(ui.item.img, ui.item.name, ui.item.slug)
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li>")
            .append('<div><img style="height: 25px; width: 25px; border-radius:50%" src="' + (item.img) + '">  ' + item.name + '</div>')
            .appendTo(ul);
    };
});


$('#ep-ce-ac-yes').click(function () {
    $('#ep-ce-acs-details').show();
    setFormHeight();
});

$('#ep-ce-ac-no').click(function () {
    $('#ep-ce-acs-details').hide();
    setFormHeight();
});