##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    internal_notes = fields.Text('Internal Notes')

    @api.multi
    def get_report(self):
        """
        Para ser usado tmb, por ejemplo, desde qweb en website_portal
        """
        return self.env['ir.actions.report'].get_report(self)

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        # if we print caming from other model then active id and active model
        # is wrong and it raise an error with custom filename
        self = self.with_context(
            active_model=self._name, active_id=self.id, active_ids=self.ids)

        return self.get_report().report_action(self)

    @api.multi
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        if self.company_id.internal_notes:
            vals.update({
                'internal_notes': self.internal_notes})
        if 'comment' in vals and not self.company_id.external_notes:
            vals.pop('comment')
        return vals
