/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CommentEditor = publicWidget.Widget.extend({
    selector: 'textarea#comment',

    start: function () {
        if (typeof $.fn.summernote !== 'undefined') {
            this.$el.summernote({
                height: 200,
                toolbar: [
                    ['style', ['bold', 'italic', 'underline', 'clear']],
                    ['para', ['ul', 'ol']],
                    ['insert', ['link', 'picture', 'video']],
                    ['view', ['codeview']]
                ],
            });
        } else {
            console.warn("Summernote not loaded properly");
        }
        return this._super.apply(this, arguments);
    },
});
