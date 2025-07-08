/**
 * So a given Form has three buttons.
 * - Upload Photos          (1)
 * - Snap a Picture Now     (2)
 * - Submit                 (3)
 *
 * On Load of (1) and (2)...
 * - Back up the original text
 * On Change of (1) or (2)...
 * - Files added:
 *   - Change text to X photo(s) selected
 *   - Mark (3) as Active
 * - Files Removed:
 *   - Change text to original
 *   - If (1) and (2) have no files...
 *     - Mark (3) inactive
 */

class UploadForm {
    /**
     *
     * @param {HTMLFormElement} form_parent
     */
    constructor(form_parent) {
        this.form = form_parent;
        this.original_text = new Map();

        [this.upload_button, this.selfie_button].forEach(btn => {
            this.original_text[btn.id] = this.label_for_button(btn).innerHTML;
            btn.addEventListener('change', this.file_event_handler.bind(this));
        });

        this.cancel_button.addEventListener('click', this.reset_form.bind(this));
    }

    get upload_button() {
        return this.form.querySelector('input[name="uploaded"]')
    }

    get selfie_button() {
        return this.form.querySelector('input[name="selfie"]')
    }

    get submit_button() {
        return this.form.querySelector('button[type="submit"]')
    }

    get cancel_button() {
        return this.form.querySelector('button[type="reset"]')
    }

    /**
     * Returns the label tied to a given button
     * @param {HTMLInputElement} btn
     * @returns {Element}
     */
    label_for_button(btn) {
        return document.querySelector(`label[for="${btn.id}"]`);
    }

    /**
     *
     * @param {Event} e
     */
    file_event_handler(e) {
        // Get the list of files that (may) be on this event
        const files = e.target?.files;
        // Also get the label that's really associated with this button
        const label = this.label_for_button(e.target);
        console.log(e.target);

        if (files && files.length) {
            label.innerText = `${`${files.length > 1 ? files.length+' ' : ''}`}Photo${files.length > 1 ? 's' : ''} Ready!`;
        } else {
            label.innerHTML = this.original_text[e.target.id];
        }

        this.update_submit_state();
    }

    update_submit_state() {
        const selfie_files = this.selfie_button.files;
        const uploaded_files = this.upload_button.files;

        if (selfie_files && selfie_files.length) {
            this.submit_button.disabled = false;
        } else if (uploaded_files && uploaded_files.length) {
            this.submit_button.disabled = false;
        } else {
            this.submit_button.disabled = true;
        }

        if (this.submit_button.disabled) {
            console.log("Adding d-none");
            this.cancel_button.classList.add('d-none');
        } else {
            console.log("Removing d-none");
            this.cancel_button.classList.remove('d-none');
        }
    }

    reset_form() {
        [this.upload_button, this.selfie_button].forEach(btn => {
            this.label_for_button(btn).innerHTML = this.original_text[btn.id];
        });
        this.form.reset();
        this.update_submit_state();
    }
}

export default UploadForm