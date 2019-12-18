# Copyright 2019 Camptocamp
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import api, fields, models
from odoo.exceptions import UserError
import discogs_client


class DiscogsImport(models.TransientModel):
    _name = 'discogs.import'

    discogs_id = fields.Integer(required=True)

    @api.multi
    def execute_import(self):
        self.ensure_one()
        # TODO: Get token from configuration
        client = discogs_client(
            'OdooDiscogsManager/1.0',
            user_token='<token>',
        )

        try:
            release = client.release(self.discogs_id)
        except discogs_client.exceptions.HTTPError:
            raise UserError(
                'Not Found', 'The Discogs ID you provided does not exist!'
            )

        tmpl_obj = self.env['product.template']
        partner_obj = self.env['res.partner']
        
        if release.master:
            res = tmpl_obj.search([('discogs_id', '=', release.master.id)])
            if not res:
                art_ids = [art.id for art in release.artists]
                # template values
                tmpl_vals = {
                    'name': release.master.title,
                    'discogs_id': release.master.id,
                    'artist_ids': None,  # TODO: check if artists need to be created or linked
                    'attribute_line_ids': None  # TODO: check if attribute already exist, create it if not
                }
                res = tmpl_obj.create(tmpl_vals)
                pass
            # variant values
        else:
            # create master template with release values
            # create variant with template
            pass
