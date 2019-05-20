from openerp import models, api, fields, _
import mercadopago


class account_invoice(models.Model):
	_inherit = "account.invoice"

	mercadopago_url = fields.Char('MercadoPago URL',compute='compute_mercadopago_url')

	@api.multi
	def action_invoice_mercadopago(self):
	        """ Open a window to compose an email, with the edi invoice template
        	    message loaded by default
	        """
        	assert len(self) == 1, 'This option should only be used for a single id at a time.'
	        template = self.env.ref('boton_mercadopago.email_template_mercadopago_invoice', False)
		if not template:
			template_id = False
		else:
			template_id = template.id
        	compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
	        ctx = dict(
        	    default_model='account.invoice',
	            default_res_id=self.id,
        	    default_use_template=bool(template),
	            default_template_id=template_id,
        	    default_composition_mode='comment',
	            mark_invoice_as_sent=True,
        	)
	        return {
        	    'name': _('Compose Email'),
	            'type': 'ir.actions.act_window',
        	    'view_type': 'form',
	            'view_mode': 'form',
        	    'res_model': 'mail.compose.message',
	            'views': [(compose_form.id, 'form')],
        	    'view_id': compose_form.id,
	            'target': 'new',
        	    'context': ctx,
	        }


	@api.one
	def compute_mercadopago_url(self):
		if self.state == 'open':
			preference = {'items':[{
				'title': self.name,
				'quantity': 1,
				'currency_id': 'ARS',
				'unit_price': self.amount_total	
				}]}
			computed_url = None
			mercadopago_client_obj = self.env['ir.config_parameter'].search([('key','=','mercadopago_client')])
			if mercadopago_client_obj:
				mercadopago_key_obj = self.env['ir.config_parameter'].search([('key','=','mercadopago_key')])
				if mercadopago_key_obj:
					mercadopago_client = mercadopago_client_obj.value
					mercadopago_key = mercadopago_key_obj.value
					mp = mercadopago.MP(mercadopago_client,mercadopago_key)
					preferenceResult = mp.create_preference(preference)
					url = preferenceResult['response']['init_point']
					computed_url = url		
			if not computed_url:
			        self.mercadopago_url = 'N/A'
			else:
				self.mercadopago_url = computed_url
