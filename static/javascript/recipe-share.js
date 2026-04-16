// recipe-share.js

document.addEventListener("DOMContentLoaded", function () {
    const shareContainer = document.querySelector(".share-buttons");

    if (!shareContainer) return;

    const url = shareContainer.dataset.url;
    const title = shareContainer.dataset.title;

    // -------------------------
    // COPY LINK
    // -------------------------
    const copyBtn = document.getElementById("copy-link");

    if (copyBtn) {
        copyBtn.addEventListener("click", async function () {
            try {
                await navigator.clipboard.writeText(url);

                const originalText = copyBtn.innerText;
                copyBtn.innerText = "Copied!";

            } catch (err) {
                console.error("Copy failed:", err);
                alert("Failed to copy link.");
            }
        });
    }

    // -------------------------
    // NATIVE SHARE (mobile)
    // -------------------------
    const nativeBtn = document.getElementById("native-share");

    if (nativeBtn) {
        if (navigator.share) {
            nativeBtn.addEventListener("click", async function () {
                try {
                    await navigator.share({
                        title: title,
                        url: url
                    });
                } catch (err) {
                    console.warn("Native share canceled or failed:", err);
                }
            });
        } else {
            // Hide button if not supported
            nativeBtn.style.display = "none";
        }
    }

    document.querySelectorAll(".share-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const type = btn.classList[1]; // e.g. "facebook", "twitter"
            console.log("Shared via:", type);
        });
    });
});