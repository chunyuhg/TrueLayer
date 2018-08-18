# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 16:57:56 2018

@author: User
"""
import posts
import unittest

class Test_posts_func(unittest.TestCase):
    
    def test_url_validator(self):
        self.assertTrue(posts.url_validator('https://news.ycombinator.com/'))
        self.assertFalse(posts.url_validator('12345'))
        
    def test_get_tag_contens(self):
        page = posts.requests.get('https://news.ycombinator.com/')
        soup = posts.BeautifulSoup(page.text,'html.parser') 
        ranks = posts.get_tag_contens(soup,'span',tag_class='rank')
        self.assertEqual(str(1),ranks)  
    
    def test_is_digital(self):
        self.assertEqual(5,posts.is_digit('5'))
        self.assertEqual(0,posts.is_digit('-4'))
        self.assertEqual(0,posts.is_digit('asd'))
if __name__ == '__main__':
    unittest.main()