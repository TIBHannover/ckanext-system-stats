# encoding: utf-8

def check_plugin_enabled(plugin_name):
    plugins = toolkit.config.get("ckan.plugins")
    if plugin_name in plugins:
        return True
    return False



from math import fabs
from flask import render_template
import ckan.plugins.toolkit as toolkit
from ckan.model import Package, Group, User
if check_plugin_enabled("semantic_media_wiki"):
    from ckanext.semantic_media_wiki.libs.media_wiki import Helper as machineHelper

if check_plugin_enabled("sample_link"):
    from ckanext.semantic_media_wiki.libs.sample_link import SampleLinkHelper
 


class BaseController():

    def index():
        result = {}
        result['Number of Datasets'] = BaseController.get_dataset_count()
        result['Number of Organizations'], result['Number of Groups'] = BaseController.get_org_group_count()
        result['Number of Users'] = BaseController.get_user_count()
        result['Number of machines resource'], result['Number of machines dataset'] = BaseController.get_linked_machines_count()
        result['Number of samples resource'], result['Number of samples dataset'] = BaseController.get_linked_samples_count()
               


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
    


    @staticmethod
    def get_linked_machines_count():
        count = 0
        dataset_count = 0
        dataset_found = False
        all_datasets = Package.search_by_name('')
        for dataset in all_datasets:
            dataset_found = False
            if dataset.state == 'active':
                for res in dataset.resources:
                    if res.state == 'active':
                        links = machineHelper.get_machine_link(res.id)
                        if len(links.keys()) != 0:
                            count += 1
                            if not dataset_found:
                                dataset_count += 1
                                dataset_found = True
        return [count, dataset_count]



    @staticmethod
    def get_linked_samples_count():
        count = 0
        dataset_count = 0
        dataset_found = False
        all_datasets = Package.search_by_name('')
        for dataset in all_datasets:
            dataset_found = False
            if dataset.state == 'active':
                for res in dataset.resources:
                    if res.state == 'active':
                        links = SampleLinkHelper.get_sample_link(res.id)
                        if len(links.keys()) != 0:
                            count += 1
                            if not dataset_found:
                                dataset_count += 1
                                dataset_found = True
        return [count, dataset_count]

