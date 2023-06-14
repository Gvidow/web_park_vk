function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

async function vote(vote, like_counter, dislike_counter) {
    const request = new Request(
        $(this).data("url"),
        {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            body: `${$(this).data("object")}_id=${$(this).data("id")}&vote=${vote}`,
        }
    );
    fetch(request).then(
        response_row => response_row.json().then(
            response_json => {
            console.log("click");
            if (response_json.status === "error") {
                console.log(`error: ${response_json.message}`);
            } else {
                like_counter.html(response_json.count_likes);
                dislike_counter.html(response_json.count_dislikes);
            }
        })
    );
}

$(".button-like").on("click", function (event) {
    vote.bind(this)("%2B", $(this).next(), $(this).closest("div").next().children("span"));
});

$(".button-dislike").on("click", function (event) {
    vote.bind(this)("-", $(this).closest("div").prev().children("span"), $(this).next());
});
