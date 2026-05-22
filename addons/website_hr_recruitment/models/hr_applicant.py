# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Applicant(models.Model):

    _inherit = 'hr.applicant'

    def website_form_input_filter(self, request, values):
        _logger.warning(
            "HR applicant job_id debug stage=hr_applicant.website_form_input_filter entry job_id=%r value_type=%s keys=%r",
            values.get('job_id'),
            type(values.get('job_id')).__name__ if values.get('job_id') is not None else None,
            list(values.keys()),
        )
        job_id = values.get('job_id')
        fixed_job_id = None
        if isinstance(job_id, str) and ',' in job_id:
            fixed_job_id = job_id.split(',', 1)[0].strip()
        elif isinstance(job_id, (list, tuple)) and job_id:
            fixed_job_id = str(job_id[0]).split(',', 1)[0].strip()
        if fixed_job_id is not None:
            _logger.warning(
                "HR applicant job_id sanitize stage=hr_applicant.website_form_input_filter raw=%r fixed=%r",
                job_id,
                fixed_job_id,
            )
            values['job_id'] = fixed_job_id

        if 'partner_name' in values:
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter before applicant_job search job_id=%r",
                values.get('job_id'),
            )
            applicant_job = self.env['hr.job'].sudo().search([('id', '=', values['job_id'])]).name if 'job_id' in values else False
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter after applicant_job search job_id=%r applicant_job=%r",
                values.get('job_id'),
                applicant_job,
            )
            name = '%s - %s' % (values['partner_name'], applicant_job) if applicant_job else _("%s's Application", values['partner_name'])
            values.setdefault('name', name)
        if values.get('job_id'):
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter before browse/active check job_id=%r",
                values.get('job_id'),
            )
            job = self.env['hr.job'].browse(values.get('job_id'))
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter browsed job ids=%r exists=%r active=%r",
                job.ids,
                bool(job.exists()),
                job.sudo().active,
            )
            if not job.sudo().active:
                raise UserError(_("The job offer has been closed."))
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter before stage search job_id=%r",
                values.get('job_id'),
            )
            stage = self.env['hr.recruitment.stage'].sudo().search([
                ('fold', '=', False),
                '|', ('job_ids', '=', False), ('job_ids', '=', values['job_id']),
            ], order='sequence asc', limit=1)
            _logger.warning(
                "HR applicant job_id debug stage=hr_applicant.website_form_input_filter after stage search job_id=%r stage_id=%r",
                values.get('job_id'),
                stage.id,
            )
            if stage:
                values['stage_id'] = stage.id
        _logger.warning(
            "HR applicant job_id debug stage=hr_applicant.website_form_input_filter exit job_id=%r keys=%r",
            values.get('job_id'),
            list(values.keys()),
        )
        return values
