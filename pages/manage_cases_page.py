#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import MozTrapBasePage
from pages.regions.filter import Filter
from pages.page import PageRegion


class MozTrapManageCasesPage(MozTrapBasePage):

    _page_title = 'Manage-Cases'

    _delete_case_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem[data-title="%(case_name)s"] .action-delete')
    _case_status_locator = (By.CSS_SELECTOR, '#managecases .itemlist .listitem[data-title="%(case_name)s"] .status-action')
    _test_case_item_locator = (By.CSS_SELECTOR, '.listitem.active')

    @property
    def filter_form(self):
        return Filter(self.testsetup)

    def go_to_manage_cases_page(self):
        self.selenium.get(self.base_url + '/manage/cases/')
        self.is_the_current_page

    def delete_case(self, name='Test Case'):
        _delete_locator = (self._delete_case_locator[0], self._delete_case_locator[1] % {'case_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def activate_case(self, name='Test Case'):
        _case_status_locator = (self._case_status_locator[0], self._case_status_locator[1] % {'case_name': name})

        self.selenium.find_element(*_case_status_locator).click()
        self.wait_for_ajax()

    @property
    def test_cases(self):
        return [self.TestCaseItem(self.testsetup, web_element)
                for web_element in self.find_elements(*self._test_case_item_locator)]

    class TestCaseItem(PageRegion):

        _case_title_locator = (By.CSS_SELECTOR, '.title')

        @property
        def name(self):
            return self.find_element(*self._case_title_locator).text
