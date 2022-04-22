# encoding: utf-8

from flask import render_template
from ckan.model import Package, Group, User


class BaseController():

    def index():
        result = {}
        result['Number of Datasets'] = BaseController.get_dataset_count()
        result['Number of Organizations'], result['Number of Groups'] = BaseController.get_org_group_count()
        result['Number of Users'] = BaseController.get_user_count()
        
               


        return render_template('stats_page.html', result=result)
    

    @staticmethod
    def get_dataset_count():
        count = 0
        all_datasets = Package.search_by_name('')
        for dataset in all_datasets:
            if dataset.state == 'active':
                count += 1
        return count
    


    @staticmethod
    def get_org_group_count():
        org_count = 0
        group_count = 0
        all_groups = Group.all()
        for g in all_groups:
            if g.state != 'active':
                continue
            elif g.is_organization:
                org_count += 1
            else:
                group_count += 1
        
        return [org_count, group_count]
    


    @staticmethod
    def get_user_count():
        count = 0
        all_users = User.all()
        for user in all_users:
            if user.state == 'active' and not user.sysadmin:
                count += 1
        return count