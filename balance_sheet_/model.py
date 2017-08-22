#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning


class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.balance_sheet_.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('balance_sheet_.module_report')
        active_wizard = self.env['ecube.balance.sheet'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['ecube.balance.sheet'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['ecube.balance.sheet'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        state  = record_wizard.state
        form    = record_wizard.form
        to      = record_wizard.to

        records = self.env['ecube.report.structure'].search([('description','=',state)])

        def head_total_(attr):
            current_account = attr
            credit = 0
            debit = 0
            total = 0
            nature = ' '
            partnerd = self.env['account.move'].search([('date','>=',form),('date','<=',to)])
            for x in records.report_link:
                if x.description.name == current_account:
                    for y in x.account_head:
                        account = []
                        for a in partnerd:
                            for b in a.line_ids:
                                if b.account_id.id == y.id:
                                    account.append(b)

                        for z in account:
                            credit = credit + z.credit
                            debit = debit + z.debit

                    nature = x.nature
            if nature == 'debit':
                total = debit - credit
            
            if nature == 'credit':
                total = credit - debit

            return total

        def full_total(attr):
            current_account = attr
            firm_partner = ' '
            credit = 0
            debit = 0
            total = 0
            partnerd = self.env['account.move'].search([('date','>=',form),('date','<=',to)])
            for x in records.report_link:
                if x.description.name == current_account:
                    for y in x.summary:
                        for a in records.report_link:
                            if a.description.name == y.name:
                                for b in a.account_head:
                                    account = []
                                    for c in partnerd:
                                        for d in c.line_ids:
                                            if d.account_id.id == b.id:
                                                account.append(d)

                                    for z in account:
                                        credit = credit + z.credit
                                        debit = debit + z.debit

                    nature = x.nature

            if nature == 'debit':
                total = debit - credit
            
            if nature == 'credit':
                total = credit - debit
            return total

        def grand_total(attr):
            current_account = attr
            credit = 0
            debit = 0
            total = 0
            nature = ' '

            partnerd = self.env['account.move'].search([('date','>=',form),('date','<=',to)])

            for a in records.report_link:

                if a.description.name == current_account:

                    for b in a.summary:

                        for c in records.report_link:

                            if c.description.name == b.name:

                                for d in c.summary:

                                    for e in records.report_link:

                                        if e.description.name == d.name:

                                            for f in e.account_head:

                                                account = []
                                                
                                                for g in partnerd:

                                                    for h in g.line_ids:
                                                    
                                                        if h.account_id.id == f.id:
                                                            account.append(h)

                                                for i in account:
                                                    credit = credit + i.credit
                                                    debit = debit + i.debit

                    nature = a.nature
            if nature == 'debit':
                total = debit - credit
            
            if nature == 'credit':
                total = credit - debit
            return total

        def call_heading():
            if state == 'balance_sheet':
                return "Balance Sheet"
                
            if state == 'profit_loss':
                return "Profit and Loss"
                
            if state == 'cash':
                return "Cash Flow"
            
        docargs = {
            'doc_ids': docids,
            'doc_model': 'ecube.report.structure',
            'docs': records,
            'data': data,
            'full_total': full_total,
            'grand_total': grand_total,
            'head_total_': head_total_,
            'form': form,
            'to': to,
            'call_heading': call_heading

        }

        return report_obj.render('balance_sheet_.module_report', docargs)