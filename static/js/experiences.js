const experienceSection = document.querySelector("#experience");
const experienceUrl = experienceSection.dataset.apiUrl;
const experienceList = document.querySelector("#experience-list");
const experienceCard = document.querySelector("#experience-card");
const searchForm = document.querySelector("#experience-search");
const searchInput = searchForm.elements.namedItem("title");
const formDialog = document.querySelector("#experience-form-dialog");
const experienceForm = document.querySelector("#experience-form");
const deleteDialog = document.querySelector("#experience-delete-dialog");
const deleteForm = document.querySelector("#experience-delete-form");
const toast = document.querySelector("#experience-toast");
let searchRequest;
let toastTimer;
let editingExperience;
let initialFields;
let deletingExperience;

function showError(message) {
    toast.textContent = message;
    toast.showPopover();
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.hidePopover(), 5000);
}

async function requestExperience(url, {method = "GET", data, signal} = {}) {
    const headers = {"Accept": "application/json"};

    if (method !== "GET") {
        const cookie = document.cookie.split("; ").find(value => value.startsWith("csrftoken="));
        headers["X-CSRFToken"] = cookie ? decodeURIComponent(cookie.slice("csrftoken=".length)) : "";
    }

    if (data !== undefined) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(url, {method, headers, body: JSON.stringify(data), signal});
    if (response.status === 204) {
        return;
    }

    const payload = await response.json().catch(() => null);
    if (!response.ok || payload === null) {
        const message = payload && (payload.detail || Object.values(payload).flat().join(" "));
        throw new Error(message || "Permintaan gagal (" + response.status + ").");
    }
    return payload;
}

function safeUrl(value) {
    try {
        const url = new URL(value);
        return ["http:", "https:"].includes(url.protocol) ? url.href : "";
    } catch {
        return "";
    }
}

function openExperienceForm(experience) {
    editingExperience = experience;
    experienceForm.reset();
    if (experience) {
        for (const field of new FormData(experienceForm).keys()) {
            experienceForm.elements.namedItem(field).value = experience[field] ?? "";
        }
        experienceForm.elements.namedItem("link").value = safeUrl(experience.link);
        experienceForm.elements.namedItem("thumbnail").value = safeUrl(experience.thumbnail);
    }
    initialFields = new FormData(experienceForm);
    document.querySelector("#experience-form-title").textContent = experience ? "Edit Experience" : "Tambah Pengalaman";
    formDialog.showModal();
}

function renderExperience(experience) {
    const card = experienceCard.content.firstElementChild.cloneNode(true);
    card.querySelector("h2").textContent = experience.title;
    card.querySelector(".experience-position").textContent = experience.position;
    card.querySelector(".experience-category").textContent = experience.skillset;
    card.querySelector(".experience-description").textContent = experience.description;
    card.querySelector(".star-count").textContent = experience.star_count;

    const thumbnail = safeUrl(experience.thumbnail);
    if (thumbnail) {
        const image = card.querySelector("img");
        image.src = thumbnail;
        image.alt = "Gambar " + experience.title;
        image.classList.remove("hide");
    }

    const link = safeUrl(experience.link);
    if (link) {
        const anchor = card.querySelector(".experience-link");
        anchor.href = link;
        anchor.classList.remove("hide");
    }

    const star = card.querySelector(".button-star");
    if (star) {
        star.querySelector(".star-label").textContent = experience.is_starred ? "Unstar" : "Star";
        star.classList.toggle("is-starred", experience.is_starred);
        star.setAttribute("aria-pressed", experience.is_starred);
        star.addEventListener("click", async () => {
            star.disabled = true;
            try {
                await requestExperience(experienceUrl + experience.id + "/star/", {method: "POST"});
                await loadExperiences();
            } catch (error) {
                showError(error.message);
            } finally {
                star.disabled = false;
            }
        });
    }

    card.querySelector(".edit-button")?.addEventListener("click", () => openExperienceForm(experience));
    card.querySelector(".delete-experience")?.addEventListener("click", () => {
        deletingExperience = experience;
        document.querySelector("#experience-delete-name").textContent = experience.title;
        deleteDialog.showModal();
    });
    return card;
}

async function loadExperiences() {
    searchRequest?.abort();
    searchRequest = new AbortController();
    const title = searchInput.value.trim();
    const query = title ? "?" + new URLSearchParams({title}) : "";

    try {
        const experiences = await requestExperience(experienceUrl + query, {signal: searchRequest.signal});
        if (experiences.length) {
            experienceList.replaceChildren(...experiences.map(renderExperience));
        } else {
            const empty = document.createElement("p");
            empty.className = "empty-state";
            empty.textContent = title ? "Tidak ada pengalaman dengan nama tersebut." : "Belum ada pengalaman yang ditambahkan.";
            experienceList.replaceChildren(empty);
        }
    } catch (error) {
        if (error.name !== "AbortError") {
            showError(error.message);
        }
    }
}

async function submitExperience(form, dialog, url, options) {
    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true;
    try {
        await requestExperience(url, options);
        dialog.close();
        await loadExperiences();
    } catch (error) {
        showError(error.message);
    } finally {
        submit.disabled = false;
    }
}

for (const dialog of [formDialog, deleteDialog]) {
    if (dialog) {
        const submit = dialog.querySelector('[type="submit"]');
        dialog.querySelector("[data-close]").addEventListener("click", () => {
            if (!submit.disabled) {
                dialog.close();
            }
        });
        dialog.addEventListener("cancel", event => {
            if (submit.disabled) {
                event.preventDefault();
            }
        });
    }
}

document.querySelector("#add-experience")?.addEventListener("click", () => openExperienceForm());

experienceForm?.addEventListener("submit", event => {
    event.preventDefault();
    const fields = Array.from(new FormData(experienceForm));
    if (editingExperience) {
        const changes = fields.filter(([field, value]) => value !== initialFields.get(field));
        submitExperience(experienceForm, formDialog, experienceUrl + editingExperience.id + "/", {
            method: "PATCH", data: Object.fromEntries(changes),
        });
    } else {
        submitExperience(experienceForm, formDialog, experienceUrl, {
            method: "POST", data: Object.fromEntries(fields),
        });
    }
});

deleteForm?.addEventListener("submit", event => {
    event.preventDefault();
    submitExperience(deleteForm, deleteDialog, experienceUrl + deletingExperience.id + "/", {method: "DELETE"});
});

searchForm.addEventListener("submit", event => {
    event.preventDefault();
    const pageUrl = new URL(window.location.href);
    const title = searchInput.value.trim();
    if (title) {
        pageUrl.searchParams.set("title", title);
    } else {
        pageUrl.searchParams.delete("title");
    }
    history.replaceState(null, "", pageUrl);
    loadExperiences();
});

loadExperiences();
