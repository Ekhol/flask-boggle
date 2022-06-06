class Boggle {

    constructor(boardId, sec = 60) {
        this.sec = sec;
        this.showTimer();

        this.score = 0;
        this.timer = setInterval(this.tick.bind(this), 1000);
        this.words = new Set();
        this.board = $("#" + boardId);
        $(".new-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.message(`${word} was already taken!`, "err");
            return;
        }

        const res = await axios.get("/check-word", { params: { word: word } });
        if (res.data.result === "not-word") {
            this.message(`${word} is not a valid word!`, "err");
        }
        else if (res.data.result === "not-on-board") {
            this.message(`${word} is not found on the board!`, "err");
        }
        else {
            this.showWord(word);
            this.words.add(word);
            this.message(`${word} found!`, "ok");
            this.score += word.length;
            this.showScore();
        }
    }

    showWord(word) {
        $(".add-word", this.board).append($("<li>", { text: word }));
    }

    showScore() {
        $(".score", this.board).text(this.score);
    }

    message(msg, status) {
        $(".message", this.board).text(msg).removeClass().addClass(`msg ${status}`);
    }

    showTimer() {
        $(".timer", this.board).text(this.sec);
    }

    async tick() {
        this.sec -= 1;
        this.showTimer();

        if (this.sec === 0) {
            clearInterval(this.timer);
            await this.gScore();
        }
    }

    async gScore() {
        $(".new-word", this.board).hide();
        const res = await axios.post("/post-score", { score: this.score });
        if (res.data.brokenRecord) {
            this.message(`New Record: ${this.score}! Congratulations!`, "ok");
        }
        else {
            this.message(`Your Score: ${this.score}`, "ok")
        }
    }
}