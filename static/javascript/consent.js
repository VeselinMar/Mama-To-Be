(function () {
    "use strict";

    const STORAGE_KEY = "mom-to-be-consent";
    const CONSENT_VERSION = 1;

    const DEFAULT_CONSENT = {
        necessary: true,
        analytics: false,
        external_media: false
    };

    let consent = null;

    /*
     * ------------------------------------------------------------
     * Consent storage
     * ------------------------------------------------------------
     */

    function getStoredConsent() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);

            if (!stored) {
                return null;
            }

            const parsed = JSON.parse(stored);

            if (
                !parsed ||
                parsed.version !== CONSENT_VERSION ||
                !parsed.preferences
            ) {
                return null;
            }

            return {
                version: CONSENT_VERSION,
                preferences: {
                    ...DEFAULT_CONSENT,
                    ...parsed.preferences,
                    necessary: true
                },
                timestamp: parsed.timestamp || null
            };
        } catch (error) {
            console.warn("Unable to read consent preferences.", error);
            return null;
        }
    }


    function saveConsent(preferences) {
        const data = {
            version: CONSENT_VERSION,
            preferences: {
                ...DEFAULT_CONSENT,
                ...preferences,
                necessary: true
            },
            timestamp: new Date().toISOString()
        };

        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (error) {
            console.warn("Unable to save consent preferences.", error);
        }

        consent = data;

        document.dispatchEvent(
            new CustomEvent("consent:updated", {
                detail: data.preferences
            })
        );
    }


    function hasConsent(category) {
        if (!consent) {
            return category === "necessary";
        }

        return consent.preferences[category] === true;
    }


    /*
     * ------------------------------------------------------------
     * Bootstrap modal helpers
     * ------------------------------------------------------------
     */

    function getModalElement(id) {
        return document.getElementById(id);
    }


    function getModalInstance(id) {
        const element = getModalElement(id);

        if (!element || typeof bootstrap === "undefined") {
            return null;
        }

        return bootstrap.Modal.getOrCreateInstance(element);
    }


    function showModal(id) {
        const modal = getModalInstance(id);

        if (modal) {
            modal.show();
        }
    }


    function hideModal(id) {
        const modal = getModalInstance(id);

        if (modal) {
            modal.hide();
        }
    }


    /*
     * ------------------------------------------------------------
     * Initial consent modal
     * ------------------------------------------------------------
     */

    function showInitialModal() {
        showModal("consentModal");
    }


    /*
     * ------------------------------------------------------------
     * Preferences modal
     * ------------------------------------------------------------
     */

    function populatePreferencesModal() {
        const analyticsToggle = document.getElementById(
            "consentAnalytics"
        );

        const externalMediaToggle = document.getElementById(
            "consentExternalMedia"
        );

        if (analyticsToggle) {
            analyticsToggle.checked = hasConsent("analytics");
        }

        if (externalMediaToggle) {
            externalMediaToggle.checked = hasConsent("external_media");
        }
    }


    function showPreferencesModal() {
        populatePreferencesModal();
        showModal("consentPreferencesModal");
    }


    /*
     * ------------------------------------------------------------
     * Consent actions
     * ------------------------------------------------------------
     */

    function acceptAll() {
        saveConsent({
            necessary: true,
            analytics: true,
            external_media: true
        });

        hideModal("consentModal");
        hideModal("consentPreferencesModal");
    }


    function rejectOptional() {
        saveConsent({
            necessary: true,
            analytics: false,
            external_media: false
        });

        hideModal("consentModal");
        hideModal("consentPreferencesModal");
    }


    function savePreferences() {
        const analyticsToggle = document.getElementById(
            "consentAnalytics"
        );

        const externalMediaToggle = document.getElementById(
            "consentExternalMedia"
        );

        saveConsent({
            necessary: true,
            analytics: analyticsToggle
                ? analyticsToggle.checked
                : false,
            external_media: externalMediaToggle
                ? externalMediaToggle.checked
                : false
        });

        hideModal("consentModal");
        hideModal("consentPreferencesModal");
    }


    /*
     * ------------------------------------------------------------
     * Public API
     * ------------------------------------------------------------
     *
     * Other scripts can use:
     *
     * window.MomToBeConsent.has("analytics")
     * window.MomToBeConsent.has("external_media")
     * window.MomToBeConsent.openPreferences()
     */

    window.MomToBeConsent = {
        has: hasConsent,
        get: function () {
            return consent;
        },
        openPreferences: showPreferencesModal,
        acceptAll: acceptAll,
        rejectOptional: rejectOptional,
        savePreferences: savePreferences
    };


    /*
     * ------------------------------------------------------------
     * Initialisation
     * ------------------------------------------------------------
     */

    function init() {
        consent = getStoredConsent();

        /*
         * No existing choice:
         * show the consent modal.
         */
        if (!consent) {
            showInitialModal();
        }

        /*
         * Existing choice:
         * make sure the preferences modal reflects it.
         */
        if (consent) {
            populatePreferencesModal();
        }


        /*
         * Initial modal buttons
         */

        const acceptAllButton = document.getElementById(
            "consentAcceptAll"
        );

        const rejectButton = document.getElementById(
            "consentRejectOptional"
        );

        const manageButton = document.getElementById(
            "consentManagePreferences"
        );

        if (acceptAllButton) {
            acceptAllButton.addEventListener("click", acceptAll);
        }

        if (rejectButton) {
            rejectButton.addEventListener("click", rejectOptional);
        }

        if (manageButton) {
            manageButton.addEventListener(
                "click",
                function () {
                    hideModal("consentModal");
                    showPreferencesModal();
                }
            );
        }


        /*
         * Preferences modal buttons
         */

        const saveButton = document.getElementById(
            "consentSavePreferences"
        );

        const preferencesAcceptAllButton =
            document.getElementById(
                "consentPreferencesAcceptAll"
            );

        const preferencesRejectButton =
            document.getElementById(
                "consentPreferencesRejectOptional"
            );

        if (saveButton) {
            saveButton.addEventListener(
                "click",
                savePreferences
            );
        }

        if (preferencesAcceptAllButton) {
            preferencesAcceptAllButton.addEventListener(
                "click",
                acceptAll
            );
        }

        if (preferencesRejectButton) {
            preferencesRejectButton.addEventListener(
                "click",
                rejectOptional
            );
        }


        /*
         * Persistent "Privacy Preferences" button
         */

        const preferencesLinks = document.querySelectorAll(
            "[data-open-consent-preferences]"
        );

        preferencesLinks.forEach(function (element) {
            element.addEventListener("click", function (event) {
                event.preventDefault();
                showPreferencesModal();
            });
        });
    }


    /*
     * Wait until Bootstrap and the DOM are available.
     */

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

})();