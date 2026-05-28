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

    function updateMacros() {
        let protein = 0;
        let carbs = 0;
        let fat = 0;

        ingredientItems.forEach(item => {
            const baseQty = parseFloat(item.dataset.baseQty);
            const unit = item.dataset.unit;

            const p = parseFloat(item.dataset.protein);
            const c = parseFloat(item.dataset.carbs);
            const f = parseFloat(item.dataset.fat);

            const grams = (baseQty / baseServings) * currentServings;

            const factor = grams / 100;

            protein += p * factor;
            carbs += c * factor;
            fat += f * factor;
        });

        document.getElementById("protein").textContent = protein.toFixed(1);
        document.getElementById("carbs").textContent = carbs.toFixed(1);
        document.getElementById("fat").textContent = fat.toFixed(1);

        document.getElementById("calories").textContent =
            ((protein * 4) + (carbs * 4) + (fat * 9)).toFixed(0);
    }

    function setServings(newValue) {
        currentServings = Math.max(1, newValue);
        display.textContent = currentServings;

        updateIngredients();
        updateMacros();
    }

    increaseBtn.addEventListener("click", () => {
        setServings(currentServings + 1);
    });

    decreaseBtn.addEventListener("click", () => {
        setServings(currentServings - 1);
    });
});