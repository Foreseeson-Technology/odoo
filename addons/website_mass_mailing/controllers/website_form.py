# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import _
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm


class WebsiteNewsletterForm(WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        self._log_hr_applicant_job_id_state('website_mass_mailing._handle_website_form entry', model_name=model_name, kwargs=kwargs)
        if model_name == 'mailing.contact':
            list_ids = kwargs.get('list_ids')
            if not list_ids:
                return json.dumps({'error': _('Mailing List(s) not found!')})
            list_ids = [int(x) for x in list_ids.split(',')]
            private_list_ids = request.env['mailing.list'].sudo().search([
                ('id', 'in', list_ids), ('is_public', '=', False)])
            if private_list_ids:
                return json.dumps({
                    'error': _('You cannot subscribe to the following list anymore : %s',
                               ', '.join(private_list_ids.mapped('name')))
                })
        self._log_hr_applicant_job_id_state('website_mass_mailing._handle_website_form before super', model_name=model_name, kwargs=kwargs)
        return super()._handle_website_form(model_name, **kwargs)
