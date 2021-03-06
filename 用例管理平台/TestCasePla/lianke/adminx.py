import collections

import xadmin

from import_export import fields, resources
from .models import Projectlianke, TestCaselianke


class ProjectliankeAdmin(object):
    # 显示的列
    list_display = ['projectVersion']
    # 搜索的字段
    search_fields = ['projectVersion']
    # 过滤
    list_filter = ['projectVersion']


class TestCaseliankeResource(resources.ModelResource):

    #  导入时外键字段的转换,需要将数据源中实际输入的值转换为对应的外键id。
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        dict = []
        for row in dataset.dict:
            tmp  = collections.OrderedDict()
            projectName = row["project"]
            for item in row:
                if item == "project":
                    try:
                        getID = Projectlianke.objects.get(projectVersion=projectName).id
                        tmp[item] = getID
                    except Exception as e:
                        print(e)
                        newPro = Projectlianke()
                        newPro.projectVersion = projectName
                        newPro.save()
                        getNewProID = Projectlianke.objects.get(projectVersion=projectName).id
                        tmp[item] = getNewProID
                else:
                    tmp[item] = row[item]
            dict.append(tmp)
        dataset.dict = dict


    class Meta:
        model = TestCaselianke
        fields = ('testId','xuqiu','process', 'testMethod','testDate', 'people','status', 'info', 'project') # 添加导入、导出的字段
        #fields = ('序号', '需求', '测试用例', '测试方法', '测试日期', '测试人员', '测试状态', '备注')  # 添加导入、导出的字段

        import_id_fields = ('testId') # 将testID 作为默认的、必要的ID字段

    def get_instance(self, instance_loader, row):
     return False


class TestCaseliankeAdmin(object):
    # 显示的列
    list_display = ['testId', 'xuqiu', 'process', 'testMethod', 'testDate', 'people', 'status', 'info', 'project']
    # 搜索的字段
    search_fields = ['xuqiu', 'process', 'people', 'status', 'info', 'project']
    # 过滤
    list_filter = ['xuqiu', 'people', 'status', 'testDate', 'project', 'addTime']

    list_editable = ['xuqiu', 'process', 'status', 'info', 'project']

    list_per_page = 100

    ordering = ['testId']

    import_export_args = {'import_resource_class': TestCaseliankeResource}


xadmin.site.register(Projectlianke, ProjectliankeAdmin)
xadmin.site.register(TestCaselianke, TestCaseliankeAdmin)




