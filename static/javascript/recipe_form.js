document.addEventListener("DOMContentLoaded", function () {

    console.log("JS_LOADED");

    const container = document.getElementById("ingredient-list");
    const template = document.getElementById("ingredient-row-template");
    const addBtn = document.getElementById("add-ingredient");
    const form = document.getElementById("recipe-form");
    console.log("FORM ELEMENT:", form);
    const jsonField = document.getElementById("ingredients-json");

    const modalEl = document.getElementById("ingredientModal");
    const modal = modalEl ? new bootstrap.Modal(modalEl) : null;

    const modalName = document.getElementById("modal-ingredient-name");
    const modalProtein = document.getElementById("modal-protein");
    const modalCarbs = document.getElementById("modal-carbs");
    const modalFat = document.getElementById("modal-fat");
    const saveBtn = document.getElementById("save-ingredient");

    let activeRow = null;

    // -------------------------
    // ADD ROW
    // -------------------------
    function addRow(data = null) {

        const node = template.content.cloneNode(true);
        container.appendChild(node);

        const row = container.lastElementChild;
        bindRow(row);

        if (data) {
            const id = data.ingredient_id ? String(data.ingredient_id) : null;

            row.querySelector(".ingredient-search").value = data.name || "";
            row.querySelector(".ingredient-id").value = id || "";
            row.querySelector(".quantity").value = data.quantity || "";
            row.querySelector(".unit").value = "g";
            row.querySelector(".note").value = data.note || "";

        }
    }

    // init
    if (window.EXISTING_INGREDIENTS?.length) {
        window.EXISTING_INGREDIENTS.forEach(i => addRow(i));
    } else {
        addRow();
    }

    if (addBtn) {
        addBtn.addEventListener("click", () => addRow());
    }

    // -------------------------
    // MODAL SAVE
    // -------------------------
    if (saveBtn && modal) {
        saveBtn.addEventListener("click", async function (e) {
            e.preventDefault();
            const name = modalName.value.trim();
            if (!name) return;

            const res = await fetch(createIngredientUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    name,
                    protein: modalProtein.value || 0,
                    carbs: modalCarbs.value || 0,
                    fat: modalFat.value || 0
                })
            });

            const data = await res.json();

            if (activeRow) {
                const search = activeRow.querySelector(".ingredient-search");
                const idField = activeRow.querySelector(".ingredient-id");

                search.value = data.name;
                idField.value = String(data.id);

            }

            modal.hide();
        });
    }

    // -------------------------
    // ROW BINDING
    // -------------------------
    function bindRow(row) {

        const search = row.querySelector(".ingredient-search");
        const idField = row.querySelector(".ingredient-id");

        // -------------------------
        // AUTOCOMPLETE
        // -------------------------
        let debounceTimer = null;

        search.addEventListener("input", function () {

            clearTimeout(debounceTimer);

            debounceTimer = setTimeout(async () => {

                const q = search.value.trim();

                idField.value = "";

                if (q.length < 2) return;

                try {
                    const res = await fetch(`${autocompleteUrl}?q=${encodeURIComponent(q)}`);
                    const data = await res.json();

                    showDropdown(search, data.results, idField);

                } catch (err) {
                    console.error("Autocomplete error:", err);
                }

            }, 200);
        });

        // -------------------------
        // REMOVE ROW
        // -------------------------
        row.querySelector(".remove-row").addEventListener("click", function () {

            const id = idField.value;

            if (row.parentNode) {
                row.remove();
            }
        });

        // -------------------------
        // OPEN MODAL
        // -------------------------
        row.querySelector(".create-ingredient").addEventListener("click", function () {

            activeRow = row;

            if (modalName) modalName.value = search.value || "";
            if (modalProtein) modalProtein.value = "";
            if (modalCarbs) modalCarbs.value = "";
            if (modalFat) modalFat.value = "";

            modal?.show();
        });
    }

    // -------------------------
    // DROPDOWN
    // -------------------------
    function showDropdown(input, results, hiddenId) {

        if (!input || !input.parentNode) return;

        document.querySelectorAll(".autocomplete-box").forEach(el => {
            el.remove();
        });

        const box = document.createElement("div");
        box.className = "autocomplete-box list-group position-absolute w-100 bg-white border";
        box.style.zIndex = "9999";

        results.forEach(r => {

            const id = String(r.id);


            const item = document.createElement("button");
            item.type = "button";
            item.className = "list-group-item list-group-item-action";
            item.textContent = r.text;

            item.onclick = function () {

                input.value = r.text;
                hiddenId.value = id;

                box.remove();
            };

            box.appendChild(item);
        });

        input.parentNode.appendChild(box);
    }

    // -------------------------
    // FORM SUBMIT (SINGLE SOURCE OF TRUTH)
    // -------------------------
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        console.log("🔥 JS SUBMIT HANDLER TRIGGERED");
        console.log("GLOBAL SUBMIT CAUGHT:", e.target);

        if (typeof tinymce !== "undefined") {
            tinymce.triggerSave();
        }

        const rows = document.querySelectorAll(".ingredient-row");
        const data = [];

        rows.forEach(row => {
            const id = row.querySelector(".ingredient-id")?.value;
            const quantityRaw = row.querySelector(".quantity")?.value;
            const unit = row.querySelector(".unit")?.value;
            const note = row.querySelector(".note")?.value;

            if (!id) return;

            const quantity = quantityRaw && !isNaN(parseFloat(quantityRaw))
                ? parseFloat(quantityRaw)
                : null;

            data.push({
                ingredient_id: parseInt(id),
                quantity,
                unit: unit || null,
                note: note || null
            });
        });

        const json = JSON.stringify(data);

        console.log("FINAL JSON SENT:", json);

        jsonField.value = json;

        setTimeout(() => {
            form.submit();
        }, true);
    });
});