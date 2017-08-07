#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'steve'

import json
import sys
sys.path.append("..")
from interface_test_automation.initialization import ParametrizedTestCase

#### 后台操作-编辑测试数据（登录、机构、套餐、检查项）
class editData(ParametrizedTestCase):

    def editData(self):
        #### 根据被测接口的实际情况，合理的添加HTTP头
        header = {'Host': '172.16.10.100:17021',
                  'Accept': 'application/json, text/javascript, */*; q=0.01',
                  'Accept-Encoding': 'gzip, deflate',
                  'Content-Type': 'application/json; charset=utf8',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest'}
        self.http.set_header(header)
        self.data = json.loads(self.test_data.request_param)
        self.name = self.data['name']
        if self.test_data.request_name == 'edit-org':
            self.db2_cursor.execute('SELECT id FROM organization WHERE name = %s', (self.name,))
            org_id = self.db2_cursor.fetchone()[0]
            id_dict = {'id': str(org_id)}
            data_dict = json.loads(self.test_data.request_param)
            data_dict.update(id_dict)
            data = json.dumps(data_dict)
        elif self.test_data.request_name == 'edit-package':
            self.db2_cursor.execute('SELECT id FROM package WHERE name = %s', (self.name,))
            package_id = self.db2_cursor.fetchone()[0]
            id_dict = {'id': package_id}
            data_dict = json.loads(self.test_data.request_param)
            data_dict.update(id_dict)
            data = json.dumps(data_dict)
        elif self.test_data.request_name == 'edit-examine-project':
            self.examineName = self.data['examineProjectName']
            self.db2_cursor.execute('SELECT id FROM examine_project WHERE examine_project_name = %s', (self.examineName,))
            examine_project_id = self.db2_cursor.fetchone()[0]
            id_dict = {'id': examine_project_id}
            data_dict = json.loads(self.test_data.request_param)
            data_dict.update(id_dict)
            data = json.dumps(data_dict)
        data = data.encode('utf-8')
        response = self.http.post(self.test_data.request_url, data)
        print (response)
        self.UpdateRecordWithoutResponse(response)
        self.BaseDataAssert(response)
        self.UpdateRecordWithResponse()