get_html = (answer_id, avatar, text) => { return `
<div id="answer-${answer_id}" class="answer" style="height: auto">
    <div class="row">
        <div class="col-3">
            <div class="answer-avatar">
                <img src="${avatar}" alt="avatar">
            </div>

            <div class="div-valuation">

                <div class="valuation like">
                    <button class="button-like" data-id="${answer_id}" data-object="answer"
                        data-url="/vote_up/answer/">
                            <img src="/static/img/like.svg">
                    </button>
                    <span>0</span>
                </div>

                <div class="valuation dislike">
                    <button class="button-dislike" data-id="${answer_id}" data-object="answer"
                        data-url="/vote_up/answer/">
                            <img src="/static/img/dislike.svg">
                    </button>
                    <span>0</span>
                </div>
            </div>

        </div>
        <div class="col-8">
            <div style="min-height: 140px">
                ${text}
            </div>
            <div class="row">
                <p><input class="correct" type="checkbox" name="correct" value="true"
                        data-id="${answer_id}"
                        data-url="/correct">Correct!</p>
            </div>
        </div>
    </div>
</div>
`;
}

function add_listener_new_answer(answer_id) {
    const vote_div = $(`#answer-${answer_id}`).children("div").children("div").children("div").next();
    vote_div.children("div").children(".button-like").on("click", click_like);
    vote_div.children("div").next().children(".button-dislike").on("click", click_dislike);
}

const conf = $("#centrifugo-conf");
const address = conf.data("address");
const token = conf.data("token");
const chan_id = conf.data("chan");

let centrifuge = new Centrifuge(address);
centrifuge.setToken(token);
centrifuge.subscribe(chan_id, (message) => {
    $("#list-answers").append(get_html(message.data.id, message.data.avatar_url, message.data.text));
    add_listener_new_answer(message.data.id);
    console.log("new message");
    console.log(message);
});
centrifuge.connect();