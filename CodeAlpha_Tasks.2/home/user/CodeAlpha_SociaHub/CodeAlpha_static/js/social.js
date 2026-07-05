console.log("Social JS Loaded!");
document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".like-btn").forEach(btn => {

        btn.addEventListener("click", async function (e) {
            e.preventDefault();
            console.log("Like button clicked");

            let url = this.dataset.url;
            let postId = this.dataset.id;

            try {
                let response = await fetch(url, {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                if (!response.ok) return;

                let data = await response.json(); 
                console.log(data);

                let countSpan = this.querySelector("span");
                let globalCounter = document.getElementById("like-count-" + postId);

                if (countSpan) {
                    countSpan.innerText = data.likes;
                }

                if (globalCounter) {
                    globalCounter.innerText = data.likes;
                }

                if (data.liked) {
                    this.classList.add("liked");
                } else {
                    this.classList.remove("liked");
                }

            } catch (error) {
                console.log(error);
            }

        });

    });

    document.querySelectorAll(".ajax-comment-form").forEach(form => {

        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            let url = this.dataset.url;
            let postId = this.dataset.post;
            let input = this.querySelector("input[name='content']");
            let content = input.value.trim();

            if (!content) return;

            try {
                let formData = new FormData();
                formData.append("content", content);

                let response = await fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                if (!response.ok) return;

                let data = await response.json();

                let commentBox = document.getElementById("comment-list-" + postId);

                if (commentBox) {

                    let newComment = document.createElement("div");
                    newComment.classList.add("comment-item");

                    newComment.innerHTML = `
                        <div>
                            <strong>@${data.author}</strong>
                            <p>${data.content}</p>
                            <small>${data.created_at}</small>
                        </div>
                    `;

                    commentBox.prepend(newComment);
                }

                input.value = "";

            } catch (error) {
                console.log(error);
            }

        });

    });

});