Getting battery cycle count of MacBook with CUI
===============================================

:date: 2015-03-27 22:14
:author: Akihiro Uchida
:tags: osx
:category: memo
:slug: battery-cycle-count-for-macbook
:lang: en
:translation: true

The battery cycle count is a indicator of the MacBook battery quality.
`Mac notebooks: Determining battery cycle count <https://support.apple.com/en-us/HT201585>`_
shows how to get battery cycle count with ``/Applications/Utilities/System Information.app`` and
the cycle count limits table for each generations of MacBook.

Getting cycle count by opening Application is annoying for me,
therefore I wrote an shellscript gettingt cycle count.

With `system_profiler(8) <https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/system_profiler.8.html>`_
command, we could get values in `System Information.app`.

To get cycle count quickly, use the following one-liner.

.. code-block:: bash

   $ system_profiler SPPowerDataType -detailLevel mini | awk -F: '/Cycle Count/ { print $2 }'

Getting cycle count more tidily, one can use xml format and parsing xml with ``xpath``, like the following

.. code-block:: bash

   $ system_profiler SPPowerDataType -detailLevel mini -xml | xpath '/plist/array/dict/key[.="_items"]/following-sibling::*[1]/dict/key[.="sppower_battery_health_info"]/following-sibling::*[1]/key[.="sppower_battery_cycle_count"]/following-sibling::*[1]/text()' 2>/dev/null

However this is too complicated, one can use ``plutil`` command to simplify plist xml extraction.

.. code-block:: bash

   $ system_profiler SPPowerDataType -detailLevel mini -xml | plutil -extract '0._items.0.sppower_battery_health_info.sppower_battery_cycle_count' xml1 -o - - | xpath '/plist/integer/text()' 2>/dev/null

With the ``plutil`` command, we could handle plist xml simply as if we use json and jq.

To note abount my environment, MacBook Pro (Retina, 13-inch, Late 2013),
the cycle count reach 396 times after 276 days, therefore cycle count would reach
1000, max cycle count, in abount 2-years.

