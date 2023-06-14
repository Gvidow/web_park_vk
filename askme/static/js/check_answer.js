$(".correct").on("click", function (event) {
    const request = new Request(
        $(this).data("url"),
        {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            body: `answer_id=${$(this).data("id")}`,
        }
    );
    fetch(request).then(
        response_row => response_row.json().then(
            response_json => {
                console.log("click correct");
                if (response_json.status === "error") {
                    console.log(`error: ${response_json.message}`);
                } else {
                    $(this).prop("checked", response_json.correct);
                }
            }
    ));
    return false;
});