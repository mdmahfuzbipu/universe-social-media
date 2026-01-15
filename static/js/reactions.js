document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".reaction-bar").forEach((bar) => {
    bar.querySelectorAll(".reaction-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const postId = bar.dataset.postId;
        const reaction = btn.dataset.reaction;

        fetch(`/interactions/react/${postId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `reaction=${reaction}`,
        })
          .then((res) => res.json())
          .then((data) => {
            bar.querySelectorAll(".reaction-btn").forEach((b) => {
              const r = b.dataset.reaction;
              const countSpan = b.querySelector(".reaction-count");

              countSpan.textContent = data.counts[r] || 0;

              if (data.user_reaction === r) {
                b.classList.add("bg-gray-200", "font-semibold");
              } else {
                b.classList.remove("bg-gray-200", "font-semibold");
              }
            });
          });
      });
    });
  });
});

function getCookie(name) {
  let value = null;
  if (document.cookie) {
    document.cookie.split(";").forEach((c) => {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        value = decodeURIComponent(c.substring(name.length + 1));
      }
    });
  }
  return value;
}
