import UploadForm from "./modules/uploads.js";

let all_forms = [];

window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        all_forms.push(new UploadForm(form));
    })
})