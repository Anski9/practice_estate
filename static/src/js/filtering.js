odoo.define('practice_estate.filtering', ['@web/views/list/list_renderer'], function (require) {
    "use strict";

    console.log("filtering.js loaded");

    const { registry } = require('@web/core/registry');
    const ListRenderer = require('@web/views/list/list_renderer');

    class CustomListRenderer extends ListRenderer {
        async willStart(){
            await super.willStart();
        }

        setup() {
            this._super.apply(this, arguments);
        }
    
        _updateDomain() {
            if (this.props.domain) {
                this.trigger_up('reload');
            }
        }
        _onStateChange(event) {
            if (event.target && event.target.name === "state") {
                this._updateDomain();
            }
        }

    }
    registry.category('view_renderers').add('list', CustomListRenderer);
});