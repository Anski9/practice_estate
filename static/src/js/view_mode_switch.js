odoo.define('practice_estate.view_mode_switch', ['web.FormController'], function (require) {
    "use strict";


    const FormController = require('web.FormController');

    console.log("JavaScript ladattu");

    FormController.include({
        events: _.extend({}, FormController.prototype.events, {
            'change select[name="custom_view_mode"]': '_onCustomViewModeChange',
        }),

        _onCustomViewModeChange: function (event) {
            console.log("custom_view_mode muuttui");

            const viewMode = $(event.target).val();
            console.log("Valittu näkymä:", viewMode);
            
            const resId = this.model.get(this.handle, {raw:true}).res_id;
            console.log("Tietueen ID:", resId);
        
        //_onFieldChanged: function (event) {
        //    this._super.apply(this, arguments);

            // if (event.data.changes.custom_view_mode) {
            //     const viewMode = event.data.changes.custom_view_mode;
            //     const resId = this.model.get(this.handle, {raw:true}).res_id;

            let action;
            if (viewMode === 'info') {
                console.log("Info-näkymä");
                action = {
                    type: 'ir.actions.act_window',
                    res_model: 'practice.estate.property.type',
                    view_mode: 'form',
                    views: [[false, 'form']],
                    res_id: resId,
                    target: 'current',
                };
                action.view_id = this.env.ref('practice_estate.practice_estate_property_type_form_view_info').id;
            }
            else {
                console.log("Questions-näkymä");
                action = {
                    type: 'ir.actions.act_window',
                    res_model: 'practice.estate.property.type',
                    view_mode: 'form',
                    views: [[false, 'form']],
                    res_id: resId,
                    target: 'current'
                };
                action.view_id = this.env.ref('practice_estate.practice_estate_property_type_form_view').id;
            }
            console.log("Action määritetty:", action);

            this.do_action(action).then(() => {
                console.log("Action suoritettu");
            }).catch((error) => {
                console.error("Action epäonnistui", error);
            });
        },
    });
});
