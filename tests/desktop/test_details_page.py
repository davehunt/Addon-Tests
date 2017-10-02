# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import urllib

import pytest
import requests

from pages.desktop.details import Details


class TestDetails:

    @pytest.mark.nondestructive
    def test_that_register_login_link_is_present_in_addon_details_page(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert details_page.header.is_register_link_visible, 'Register link is not visible'
        assert details_page.header.is_login_link_visible, 'Login links is not visible'

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_dropdown_menu_is_present_after_click_on_other_apps(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Other Applications' == details_page.header.menu_name
        details_page.header.hover_over_other_apps_menu()
        assert details_page.header.is_other_apps_dropdown_menu_visible

    @pytest.mark.nondestructive
    def test_that_addon_name_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        # check that the name is not empty
        assert not details_page.title == ''

    @pytest.mark.nondestructive
    def test_that_summary_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        # check that the summary is not empty
        assert re.match('(\w+\s*){3,}', details_page.summary) is not None

    @pytest.mark.nondestructive
    def test_that_about_this_addon_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'About this Add-on' == details_page.about_addon
        assert re.match('(\w+\s*){3,}', details_page.description) is not None

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_version_information_is_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Version Information' == details_page.version_information_heading

        details_page.expand_version_information()
        assert details_page.is_version_information_section_expanded
        assert details_page.is_source_code_license_information_visible
        assert details_page.is_whats_this_license_visible
        assert details_page.is_complete_version_history_visible
        assert details_page.is_version_information_install_button_visible
        # check that the release number matches the version number at the top of the page
        assert 'Version %s' % details_page.version_number == details_page.release_version

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_that_reviews_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Reviews' == details_page.review_title
        assert details_page.has_reviews
        for review in details_page.review_details:
            assert review is not None

    @pytest.mark.nondestructive
    def test_that_tags_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert details_page.are_tags_visible

    @pytest.mark.nondestructive
    def test_part_of_collections_are_displayed(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Part of these Collections' == details_page.part_of_collections_header
        assert len(details_page.part_of_collections) > 0

    @pytest.mark.nondestructive
    def test_website_link(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'MemChaser')
        url = 'https://wiki.mozilla.org/QA/Automation_Services/Projects/Addons/MemChaser'
        assert urllib.quote(url) in details_page.website
        assert requests.head(url).url == url

    @pytest.mark.nondestructive
    def test_that_whats_this_link_for_source_license_links_to_an_answer_in_faq(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        details_page.expand_version_information()
        user_faq_page = details_page.click_whats_this_license()
        assert re.match('(\w+\s*){3,}', user_faq_page.license_question) is not None
        assert re.match('(\w+\s*){3,}', user_faq_page.license_answer) is not None

    @pytest.mark.nondestructive
    def test_author_addons_when_there_are_multiple_authors(self, base_url, selenium):
        addon_with_multiple_authors = 'firebug'
        page = Details(base_url, selenium, addon_with_multiple_authors)
        assert len(page.authors) > 1
        assert 'Other add-ons by these authors' == page.author_addons.heading

    @pytest.mark.nondestructive
    def test_author_addons_when_there_is_only_one_author(self, base_url, selenium):
        addon_with_one_author = 'MemChaser'
        page = Details(base_url, selenium, addon_with_one_author)
        assert len(page.authors) == 1
        assert 'Other add-ons by %s' % page.authors[0] == page.author_addons.heading

    @pytest.mark.nondestructive
    def test_navigating_to_author_addons(self, base_url, selenium):
        addon_page = Details(base_url, selenium, 'firebug')
        for i in range(len(addon_page.author_addons.addons)):
            author_addon_name = addon_page.author_addons.addons[i].name
            addon_page.author_addons.addons[i].click()
            assert author_addon_name in selenium.title
            selenium.back()

    @pytest.mark.nondestructive
    def test_open_close_functionality_for_image_viewer(self, base_url, selenium):
        page = Details(base_url, selenium, 'firebug')
        viewer = page.previews.thumbnails[0].click()
        assert viewer.is_displayed
        viewer.close()
        assert not viewer.is_displayed

    @pytest.mark.nondestructive
    def test_image_viewer_navigation(self, base_url, selenium):
        page = Details(base_url, selenium, 'firebug')
        thumbnails = page.previews.thumbnails
        viewer = thumbnails[0].click()
        assert not viewer.is_previous_displayed
        for i in range(len(thumbnails)):
            assert viewer.images[i].is_displayed
            assert thumbnails[i].title == viewer.caption
            assert thumbnails[i].source.split('/')[-1] == viewer.images[i].source.split('/')[-1]
            viewer.click_next()
        assert not viewer.is_next_displayed
        for i in range(len(thumbnails) - 1, -1, -1):
            assert viewer.images[i].is_displayed
            assert thumbnails[i].title == viewer.caption
            assert thumbnails[i].source.split('/')[-1] == viewer.images[i].source.split('/')[-1]
            viewer.click_previous()
        assert not viewer.is_previous_displayed

    @pytest.mark.nondestructive
    def test_that_review_usernames_are_clickable(self, base_url, selenium):
        addon_name = 'firebug'
        detail_page = Details(base_url, selenium, addon_name)

        for i in range(0, len(detail_page.reviews)):
            username = detail_page.reviews[i].username
            amo_user_page = detail_page.reviews[i].click_username()
            assert username == amo_user_page.username
            Details(base_url, selenium, addon_name)

    @pytest.mark.nondestructive
    def test_that_clicking_info_link_slides_down_page_to_version_info(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        details_page.click_version_info_link()
        assert details_page.version_info_link == details_page.version_information_href
        assert details_page.is_version_information_section_expanded
        assert details_page.is_version_information_section_in_view

    def test_that_add_a_review_button_works(self, base_url, selenium, logged_in):
        details_page = Details(base_url, selenium, 'Firebug')
        review_box = details_page.click_to_write_review()
        assert review_box.is_review_box_visible

    @pytest.mark.nondestructive
    def test_the_developers_comments_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert u'Developer\u2019s Comments' == details_page.devs_comments_title
        details_page.expand_devs_comments()
        assert details_page.is_devs_comments_section_expanded
        assert re.match('(\w+\s*){3,}', details_page.devs_comments_message) is not None

    @pytest.mark.nondestructive
    def test_that_the_development_channel_expands(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Development Channel' == details_page.development_channel_text
        assert '' == details_page.development_channel_content
        details_page.click_development_channel()
        assert details_page.development_channel_content is not None
        details_page.click_development_channel()
        assert '' == details_page.development_channel_content

    @pytest.mark.nondestructive
    def test_click_on_other_collections(self, base_url, selenium):
        details_pg = Details(base_url, selenium, 'Firebug')
        for i in range(0, len(details_pg.part_of_collections)):
            name = details_pg.part_of_collections[i].name
            collection_pg = details_pg.part_of_collections[i].click_collection()
            assert name == collection_pg.collection_name, 'Expected collection name does not match the page header'
            details_pg = Details(base_url, selenium, 'Firebug')

    @pytest.mark.nondestructive
    def test_the_development_channel_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'Firebug')
        assert 'Development Channel' == details_page.development_channel_text
        details_page.click_development_channel()

        # Verify if description present
        assert details_page.development_channel_content is not None
        assert details_page.is_development_channel_install_button_visible

        # Verify experimental version (beta or pre)
        assert re.match('Version\s\d+\.\d+\.\d+[a|b|rc]\d+', details_page.beta_version) is not None

    @pytest.mark.nondestructive
    def test_that_license_link_works(self, base_url, selenium):
        addon_name = 'Firebug'
        details_page = Details(base_url, selenium, addon_name)
        assert 'BSD License' == details_page.license_link_text
        license_link = details_page.license_site
        assert license_link is not None

    @pytest.mark.nondestructive
    def test_that_clicking_user_reviews_slides_down_page_to_reviews_section(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        details_page.click_user_reviews_link()
        assert details_page.is_reviews_section_visible
        assert details_page.is_reviews_section_in_view

    @pytest.mark.action_chains
    @pytest.mark.nondestructive
    def test_that_install_button_is_clickable(self, base_url, selenium):
        details_page = Details(base_url, selenium, 'firebug')
        assert 'active' in details_page.click_and_hold_install_button_returns_class_value()

    @pytest.mark.nondestructive
    def test_what_is_this_in_the_version_information(self, base_url, selenium):
        details_page = Details(base_url, selenium, "Firebug")
        assert 'Version Information' == details_page.version_information_heading
        details_page.expand_version_information()
        assert 'What\'s this?' == details_page.license_faq_text
        license_faq = details_page.click_whats_this_license()
        assert 'Frequently Asked Questions' == license_faq.header_text
