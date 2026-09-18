document.addEventListener("DOMContentLoaded", () => {
    const decreaseBtn = document.getElementById("servings-decrease");
    const increaseBtn = document.getElementById("servings-increase");
    const display = document.getElementById("servings-value");

    const ingredientList = document.querySelector(".ingredient-list");

    if (!decreaseBtn || !increaseBtn || !display || !ingredientList) {
        return;
    }

    const ingredientItems = document.querySelectorAll(".ingredient-item");

    const baseServings = parseInt(
        ingredientList.dataset.baseServings || "1",
        10
    );

    let currentServings = parseInt(display.textContent || "1", 10);

    function updateIngredients() {
        ingredientItems.forEach(item => {
            const baseQty = parseFloat(item.dataset.baseQty);
            const qtyEl = item.querySelector(".qty-value");

            if (!Number.isFinite(baseQty) || !qtyEl) {
                return;
            }

            const newQty =
                (baseQty / baseServings) * currentServings;

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
            const baseGrams = parseFloat(item.dataset.baseGrams);

            const p = parseFloat(item.dataset.protein) || 0;
            const c = parseFloat(item.dataset.carbs) || 0;
            const f = parseFloat(item.dataset.fat) || 0;

            if (!Number.isFinite(baseGrams) || baseGrams <= 0) {
                return;
            }

            // Nutrition is calculated from the original recipe quantity.
            // Ingredient nutrition is stored per 100 g.
            const factor = baseGrams / 100;

            protein += p * factor;
            carbs += c * factor;
            fat += f * factor;
        });

        // Convert whole-recipe nutrition to nutrition per serving.
        protein /= baseServings;
        carbs /= baseServings;
        fat /= baseServings;

        document.getElementById("protein").textContent =
            protein.toFixed(1);

        document.getElementById("carbs").textContent =
            carbs.toFixed(1);

        document.getElementById("fat").textContent =
            fat.toFixed(1);

        const calories =
            (protein * 4) +
            (carbs * 4) +
            (fat * 9);

        document.getElementById("calories").textContent =
            calories.toFixed(0);
    }

    function setServings(newValue) {
        currentServings = Math.max(1, newValue);

        display.textContent = currentServings;

        updateIngredients();
        updateMacros();
    }

    // Synchronize nutrition and ingredients on initial page load.
    updateIngredients();
    updateMacros();

    increaseBtn.addEventListener("click", () => {
        setServings(currentServings + 1);
    });

    decreaseBtn.addEventListener("click", () => {
        setServings(currentServings - 1);
    });
});