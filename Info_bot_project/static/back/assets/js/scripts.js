(function (window, undefined) {
    'use strict';

    // typo reporting

    let isTypoReportModalOpen = !1;
    $("body").keydown(function (e) {
        if ((e.keyCode === 10 || e.keyCode === 13) && e.ctrlKey) {
            if (window.getSelection().toString().length > 0 && !isTypoReportModalOpen) {
                isTypoReportModalOpen = !0;
                let selection = window.getSelection().toString();
                $("#typo-found").modal("show");
                $("#typo-found-selection").text(selection);
                $("#typo-found-input-hidden").val(selection);
            }
        }
    });
    $("#typo-found").on("hidden.bs.modal", function () {
        isTypoReportModalOpen = !1;
    });
    $("#typo-found").on("submit", (e) => {
        e.preventDefault();
        let fd = new FormData(e.target);
        let object = {};
        fd.forEach(function (value, key) {
            object[key] = value;
        });
        let json = JSON.stringify(object);
        let url = window.location.origin + "/error/";
        $.ajax({
            url: url,
            method: "post",
            headers: {"X-CSRFToken": json.csrfmiddlewaretoken},
            data: object,
            success: (e) => {
                $("#typo-found").modal("hide");
                $("#typo-found-success").modal("show");
            },
            error: (e) => {
                $("#typo-found-fail").css("display", "block");
            },
        });
    });

// Confirm delations


// Get the modal
    var modal = document.getElementById("myModal");

// Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close-x")[0];

    var no = document.getElementsByClassName("No")[0];


// confirm deletion
    const deleteButtons = document.querySelectorAll(".removeButton");
    for (let i = 0; i < deleteButtons.length; i++) {
        deleteButtons[i].addEventListener("click", function (evt) {
            evt.preventDefault();
            const id = deleteButtons[i].dataset.id;
            showDeletePopup(id);
        });
    }

    /**
     * @param id is id of tour that you wanna delete
     */


    function showDeletePopup(id) {
        function removeCharacter(str_to_remove, str) {
            let reg = new RegExp(str_to_remove);
            return str.replace(reg, '')
        }

        let url = document.URL
        url = url.split('?')[0]
        url = url.replace('list/', '')
        let deleteURL = url + "delete/";
        deleteURL = removeCharacter("#", deleteURL);

        const deletePopupWindow = document.querySelector("#myModal");
        const modalDeleteLink = document.querySelector("#modalDeleteButton");

        deletePopupWindow.style.display = "block";
        modalDeleteLink.setAttribute("href", deleteURL + id + "/");
    }


// When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };

    no.onclick = function () {
        modal.style.display = "none";
    };
// When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };


// confirm cancelation


// Get the button that opens the modal
    var btn = document.getElementById("cancelBtn");


// When the user clicks the button, open the modal

    btn.onclick = function () {
        modal.style.display = "block";
    };

// When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };

    no.onclick = function () {
        modal.style.display = "none";
    };
// When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };


})(window);
