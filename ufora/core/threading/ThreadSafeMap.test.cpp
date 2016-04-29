/***************************************************************************
   Copyright 2015 Ufora Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
****************************************************************************/
#include "ThreadSafeMap.hpp"
#include "../UnitTest.hpp"

using namespace std;

BOOST_AUTO_TEST_CASE( test_ThreadSafeMap )
{
    ThreadSafeMap<std::string, int> m;

    //verify we can't update 'null'
    BOOST_CHECK(m.testAndSet("key", null() << 0, null() << 1) == false);
    BOOST_CHECK(!m.contains("key"));

    //make a good update
    BOOST_CHECK(m.testAndSet("key", null(), null() << 0) == true);
    BOOST_CHECK(m.contains("key"));
    BOOST_CHECK(*m.get("key") == 0);

    //verify we can't update with the wrong value
    BOOST_CHECK(m.testAndSet("key", null() << 1, null() << 0) == false);
    BOOST_CHECK(m.contains("key"));
    BOOST_CHECK(*m.get("key") == 0);

    //verify we can update with the right value
    BOOST_CHECK(m.testAndSet("key", null() << 0, null() << 0) == true);
    BOOST_CHECK(m.contains("key"));
    BOOST_CHECK(*m.get("key") == 0);

    //verify we can't update assuming 'null'
    BOOST_CHECK(m.testAndSet("key", null(), null() << 0) == false);
    BOOST_CHECK(m.contains("key"));
    BOOST_CHECK(*m.get("key") == 0);

    //verify we can update to null
    BOOST_CHECK(m.testAndSet("key", null() << 0, null()) == true);
    BOOST_CHECK(!m.contains("key"));

}
