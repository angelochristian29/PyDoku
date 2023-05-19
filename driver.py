# coding: utf-8     # <- This is an encoding declaration  REQUIRED
#NAME:  Menu.py
"""
Driver for the App
"""

"""
AUTHOR: Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin


   Unpublished-rights reserved under the copyright laws of the United States.

   This data and information is proprietary to, and a valuable trade secret
   of, Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin. It is given 
   in confidence by Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin. 
   Its use, duplication, or disclosure is subject to
   the restrictions set forth in the License Agreement under which it has been
   distributed.

      Unpublished Copyright © 2022  Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin
      All Rights Reserved
"""

"""
Imports
"""
import Menu

def main():
    Menu.menu_loop()

if __name__ == "__main__":
    print("Driver.py: Module is executed")
    main()
else:
    print("Driver.py: Module is imported")