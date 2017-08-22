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
from openerp import models, fields, api

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.purchase_approval_doc.purchase_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('purchase_approval_doc.purchase_report')
        records = self.env['purchase.requisition'].browse(docids)
        cash = 0
        credit = 0
        for x in records.purchase_requisition_tree_link:
            if records.purchase_requisition_tree_link:
                print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" + x.p_terms
                if x.p_terms == 'cash':
                    cash = (x.qty_order * x.rate) + cash
                else:
                    credit = (x.qty_order * x.rate) + credit

                    


        
        docargs = {
            'doc_ids': docids,
            'doc_model': 'purchase.requisition',
            'docs': records,
            'cash':cash,
            'credit':credit
            }

        return report_obj.render('purchase_approval_doc.purchase_report', docargs)
