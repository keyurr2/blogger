
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author : Keyur M. Rathod
# Email : keyur.rathod1993@gmail.com
# Contact Number : +919722843263
##################################################################################

"""Simple command-line utility for Blogger.

Command-line application that 
  1) retrieves the users blogs and posts,
  2) Delete post for user
  3) Update existing post
  4) Create new post for particular User. 

How to use : by running script , it will show Username, Blog title, Url for this blog, and all posts
             After that script will ask user for action to delete, update and create new post.

Usage:
  $ python blogger.py
You can also get help on all the command-line flags the program understands
by running:
  $ python blogger.py --help
To get detailed log output run:
  $ python blogger.py --logging_level=DEBUG

"""

from __future__ import print_function

__author__ = 'keyur.rathod1993@gmail.com (Keyur Rathod)'

import sys

from oauth2client import client
from googleapiclient import sample_tools
import time
import os


def main(argv):
  # Authenticate and construct service.
  print ("\n Script started ... ")
  service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')
  try:

      users = service.users()
      # Retrieve this user's profile information
      thisuser = users.get(userId='self').execute()
      print ('\n Disply name for this User is :- %s ' % thisuser['displayName'])
      blogs = service.blogs()

      # Retrieve the list of Blogs this user has write privileges on
      thisusersblogs = blogs.listByUser(userId='self').execute()
      blog_count = 0
      print ("\n List of Blogs")
      for blog in thisusersblogs['items']:
        print ("     => Blog number : %s" % (blog_count))
        print ('          - Blog name :- %s \n          - Url for this Blog is :- %s' % (blog['name'], blog['url']))
        blog_count = blog_count + 1
      
      posts = service.posts()
      
      # List the posts for each blog this user has
      
      for blog in thisusersblogs['items']:
        # print('The posts for %s with BLOG id %s \n' % (blog['name'], blog['id']))
        print('\n Title for all posts of blog - %s(%s) are as follows : \n' % (blog['name'],blog_count-1))
        request = posts.list(blogId=blog['id'])
        i = 0
        while request != None:
          posts_doc = request.execute()
          if 'items' in posts_doc and not (posts_doc['items'] is None):
            post_ids = []
            for post in posts_doc['items']:
              post_ids.append(post['id']) 
              print('     %s). %s\n' % (i, post['title']))
              # print('Title :- %s and Post_Id :- %s and index is %s\n' % (post['title'], post['id'], i))
              i = i + 1
          request = posts.list_next(request, posts_doc)
          if (i % 10 == 0):
            stop = str(raw_input(" Press 1 to view more or Enter to continue ... :\t"))          
            if stop != '1':
              break
            else:
              clear = lambda: os.system('cls')
              clear()
              print (" Screen is cleared ...")

      if blog_count == 1:
        blog_number = 0
      else:            
        blog_number = int(raw_input(" Enter blog number : \n "))  
      input_choice = str(raw_input(" Please enter your choice :- \n  1 for Create Post\n  2 for Select any Post\n  3 for return\n  "))
      print("\n")

#############################################################################################################
      if input_choice == '1':
        print ("  Post will be created")
        title = str(raw_input("     Title for new Post : "))
        content = str(raw_input("     Content for new Post : "))
        print("\n")
        try:
          posts.insert(blogId=thisusersblogs['items'][blog_number]['id'], body={'title':title, 'content':content}).execute()

        except:
          print ("  Oops ... You might have enter wrong choice")          

      elif input_choice == '2':
        print ("     You are going to select a blog")
        post_number = int(raw_input("     Enter Post number : "))  
        print("\n")
        # request = posts.get(blogId=thisusersblogs['items'][blog_number]['id'], postId=posts_doc['items'][i]['id'])
        post = posts_doc['items'][post_number]         
        print ("     Post with Title :- %s is selected" %(post['title']))
        print ("     Content :- %s" %(post['content']))  
        input_choice_post = str(raw_input("     Enter 1 for delete\n     Enter 2 for update\n     Enter 3 for return\n    "))
        ############################################################################################
        if input_choice_post == '1':
          try:
            posts.delete(blogId=thisusersblogs['items'][blog_number]['id'], postId=post['id']).execute()
          except:
            print ("     Oops ... You might have enter wrong choice")
          print("     !!! %s - post deleted\n" %(post['title']))
          message = str(raw_input("Enter to continue ... \n "))
        elif input_choice_post == '2':
          title = str(raw_input("      New Title to update : "))
          content = str(raw_input("     New Content to update : "))
          try:
            posts.update(blogId=thisusersblogs['items'][blog_number]['id'], postId=post['id'], body={'title':title, 'content':content}).execute()
          except:
            print ("     Oops ... You might have enter wrong choice")
          print("     %s - New post created\n" %(title))
          message = str(raw_input("Enter to continue ... \n "))
        elif input_choice_post == '3':
          print ("     You are going back ... \n")
          time.sleep(1)
          pass
        else:
          print ("     !!! Invalid choice ... \n")
          pass          
          ############################################################################################
      elif input_choice == '3':
        print ("  You are going back ... \n")
        time.sleep(1)
        pass        
      else:
        print ("  !!! Invalid choice ... \n")
        pass

      print ("#############################################################################")              
  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')


if __name__ == '__main__':
  while 1:
    main(sys.argv)
