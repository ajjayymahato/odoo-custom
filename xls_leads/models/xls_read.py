from __future__ import print_function
import json
import traceback
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from odoo import fields,models,api
import pygsheets

import logging

_logger = logging.getLogger(__name__)



class ReadXls(models.TransientModel):
    _name = 'cron.xls'

    @api.model
    def cron_test(self):
        print("checking")
        print("Executing")

        # secret_dict = {
        #         "type": self.env['ir.config_parameter'].sudo().get_param('xls_leads.type'),
        #         "project_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.project_id'),
        #         "private_key_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.private_key_id'),
        #         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCttvzf2yUJVMYC\nujnCj6+lTfAu7NoFhpIynd9D6dNvMH4AXsr/aTrmA1mPh6tXxIjrP5urpJYQ95NL\n0K9bBXB3p+c4QuklMKmFYT59WxwKX5/g0+vE0VwzAU9IA2HpSzEdNWoprluN44yW\npo6EDlYsmHCW40C6ccya1pHukt1rjyyJMiztMp3bnlc5GanAQ2c4UGabP4owRZsP\nwDp2tyyfd3gr+xUuuuM9eMSGiLyj8i6WqUypA5s9OW4JAIVUnamZDzoejlHeTC8a\nbh+FT65nqFUYacamaLdkExxLLsBa6nonLDA3zNpPuQsf7GLsxXxiXaAcM3emxLj4\nUz52xA9dAgMBAAECggEAFAIiITSQEQGTJwhFE9xR6lPOSNFeEUndN/hIGX3qrQFk\nWe2RKxb3Qjv7ilUhjqPj81ipuPzljgG+FPrt36mCOT39G1VVnkN7GxJGzNB8K9O0\nygQOwWYt3PAXLh+5nNHcz9Txq+hZwj+F12pKuvodwdgzC6YUNAVcgC8bsuN2nmc4\nDmWod7gTszJ0mekhRQ5QDEfqF2d+c4aLjLg1mj119fRLIEyZIgijA+NMJwrnbNFx\nmXok4zF0edLFZwZFBzud/34FoZYEWDXyqtpwoKdEwo+00+6YvNrBFzArz+4DB6Mw\nfmEBdaxyssdMBLcX2jSyDx8tNJuQKr05bVqbR0uV3wKBgQDjRQni8DmrakC5ZZ6v\ndXnmG8lXiOMe+XRqlDl/0Ry+wuLvWict7+W8n4w4C/xsANstSfaZdyi2z8mWkthd\nPt+4v26vuEtJrcy6jHDDnBlXvFfohffevragX3yeT36RDGIhV4978B4IeWjjVTzh\n8YlBLw4Ju3mK27CihIq91Et2lwKBgQDDrMq1NiZlAxbG5og/uYwq1Luc7FuCDffD\nl7M2nw5BdECG1SBzFd9OcrT6sBABFY3cDDgfUXOImIiBpigE5ifYsxmgX0DqKvXA\nZKUU26IacZOg5Y3HBu5Fr4FyzhjG6hJjtkdDaHbDnpev3xBpLjkv3MVxyrt+Hx8A\nm+cA70p8KwKBgQDcsrxpDtNR7Lqxz0cMKE6Z8L3TLXExMRmmLg6wWsdJUEPEH44Q\ng/ha9aza+HjGAQbWsg6w9RAqhxnCCRPnaRkkdXHtXlBuWkKHnb4blsjddF8BxKby\nPc1na5K+wX+tJ5NbwYXq20CvBgefS7T1zPJ2xFUjilT7TV/4UjHRKgmmPQKBgBGD\no9k4cZNVBXLkK4nYp80loW1YUpB/g4/EQkw/TF1bdHMdHHxwlr5E0iImJCiUr0/k\n4Bkdh0PQs1c3chmOKD7jOQX7wKm1Eq4X1Bbb2dSYGeiq41fPLQCbxvBpthoH1YGL\nTTGhZg/4YAdj5eokMwYvspSO2t1dF79MNQ8GXBplAoGADaGQ1WdpmIblQr3zD6G7\n+T2qJYNdWaEHVIM65EqcEgggHrTke6NFqYUlr08rKFSh7T86JFqMvjl/5poSu9A2\nLPRazSjRa2tHTJAJnxL/666AgHAN95XxgWwligKiocYn4RUQS113c2R6/cLaJUV6\nijreAzCmc6dLVqO7mQvmVK8=\n-----END PRIVATE KEY-----\n",
        #         "client_email": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_email'),
        #         "client_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_id'),
        #         "auth_uri": self.env['ir.config_parameter'].sudo().get_param('xls_leads.auth_uri'),
        #         "token_uri": self.env['ir.config_parameter'].sudo().get_param('xls_leads.token_uri'),
        #         "auth_provider_x509_cert_url": self.env['ir.config_parameter'].sudo().get_param('xls_leads.auth_provider_x509_cert_url'),
        #         "client_x509_cert_url": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_x509_cert_url')
        #     }
        # SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
        # s1 = json.dumps(secret_dict)
        # service_account_info = json.loads(s1)
        # my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        # client = pygsheets.authorize(custom_credentials=my_credentials)

        client = pygsheets.authorize(service_account_file='custom_addons/xls_leads/models/keys.json')
        sheet1 = client.open_by_url('https://docs.google.com/spreadsheets/d/1joEMBnP87NFMrB0N11C0SzqvKYmn0CxKYv4hvQh2yUA')
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False,
                                         returnas='matrix')
        end_row = len(cells)
        indices = {
            'TIMESTAMP': 0,
            'NAME': 1,
            'COMPANY': 2,
            'REQUIREMENT': 3,
            'DESIGNATION': 4,
            'BRANCH': 5,
            'NAME_NUMBER': 6,
            'NUMBER': 7,
            'STATUS': 8,
            'ID': 9

        }
        leads = [{
            'created_at': new_lst[indices['TIMESTAMP']],
            'name': new_lst[indices['NAME']],
            'company': new_lst[indices['COMPANY']],
            'requirement': new_lst[indices['REQUIREMENT']],
            'designation': new_lst[indices['DESIGNATION']],
            'branch': new_lst[indices['BRANCH']],
            'name_number': new_lst[indices['NAME_NUMBER']],
            'number': new_lst[indices['NUMBER']],
            'status': new_lst[indices['STATUS']],
            'id': new_lst[indices['ID']]

        } for new_lst in cells[2:]]
        print(leads)
        #worksheet.delete_rows(8, number=5) //TO DELETE ROWS
        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
            except:
                tb =traceback.format_exc()
                _logger.error(tb)
                pass


