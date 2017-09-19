# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page


class Sorter(Page):

    _sort_by_featured_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Featured']")
    _sort_by_most_users_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Most Users']")
    _sort_by_top_rated_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Top Rated']")
    _sort_by_newest_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Newest']")

    _sort_by_name_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Name']")
    _sort_by_weekly_downloads_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Weekly Downloads']")
    _sort_by_recently_updated_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Recently Updated']")
    _sort_by_up_and_coming_locator = (By.XPATH, "//div[@id='sorter']//li/a[normalize-space(text())='Up & Coming']")

    _selected_sort_by_locator = (By.CSS_SELECTOR, '#sorter > ul > li.selected a')

    _hover_more_locator = (By.CSS_SELECTOR, "li.extras > a")
    _updating_locator = (By.CSS_SELECTOR, '.updating')

    def sort_by(self, category):
        click_element = self.selenium.find_element(*getattr(self, '_sort_by_%s_locator' % category.replace(' ', '_').lower()))
        if category.replace(' ', '_').lower() in ["featured", "most_users", "top_rated", "newest"]:
            click_element.click()
        else:
            hover_element = self.selenium.find_element(*self._hover_more_locator)
            ActionChains(self.selenium).move_to_element(hover_element).perform()
            click_element.click()

    @property
    def sorted_by(self):
        return self.selenium.find_element(*self._selected_sort_by_locator).text
