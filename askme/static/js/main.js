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

async function vote(vote, btn_like, btn_dislike) {
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
                btn_like.next().html(response_json.count_likes);
                btn_dislike.next().html(response_json.count_dislikes);
                console.log(response_json.valuation)
                if (response_json.valuation === "like") {
                    btn_like.css({"background": "#cccccc"})
                    btn_dislike.css({"background": "none"})
                } else if (response_json.valuation === "dislike") {
                    btn_like.css({"background": "none"})
                    btn_dislike.css({"background": "#cccccc"})
                } else {
                    btn_like.css({"background": "none"})
                    btn_dislike.css({"background": "none"})
                }
            }
        })
    );
}

function click_like(event) {
    vote.bind(this)("%2B", $(this), $(this).closest("div").next().children("button"));
}

function click_dislike(event) {
    vote.bind(this)("-", $(this).closest("div").prev().children("button"), $(this));
}

$(".button-like").on("click", click_like);

$(".button-dislike").on("click", click_dislike);
