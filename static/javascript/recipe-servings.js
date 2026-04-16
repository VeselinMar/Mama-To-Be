document.addEventListener("DOMContentLoaded", () => {
    const decreaseBtn = document.getElementById("servings-decrease");
    const increaseBtn = document.getElementById("servings-increase");
    const display = document.getElementById("servings-value");

    const ingredientItems = document.querySelectorAll(".ingredient-item");
    const baseServings = parseInt(
        document.querySelector(".ingredient-list")?.dataset.baseServings || "1"
    );

    let currentServings = parseInt(display.textContent);

    function updateIngredients() {
        ingredientItems.forEach(item => {
            const baseQty = parseFloat(item.dataset.baseQty);
            const qtyEl = item.querySelector(".qty-value");

            if (!baseQty || !qtyEl) return;

            const newQty = (baseQty / baseServings) * currentServings;

            qtyEl.textContent = Number.isInteger(newQty)
                ? newQty
                : newQty.toFixed(1);
        });
    }

    function setServings(newValue) {
        currentServings = Math.max(1, newValue);
        display.textContent = currentServings;

        updateIngredients();
    }

    increaseBtn.addEventListener("click", () => {
        setServings(currentServings + 1);
    });

    decreaseBtn.addEventListener("click", () => {
        setServings(currentServings - 1);
    });
});